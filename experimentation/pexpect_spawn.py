""" This file is for experimentation with the pexpect library.
"""

# Import the pexpect library
import pexpect
import time
import re
import pyte

screen = pyte.Screen(150, 1)
stream = pyte.ByteStream(screen)


def escape_ansi(raw_output):
    ansi_escape = re.compile(
        rb'\x1b\[[0-9;]*[A-Za-z]')  # Notice the 'rb' to handle raw bytes
    clean_output = re.sub(ansi_escape, b'', raw_output)
    ansi_escape = re.compile(
        rb'\x1b\]0;.*\x07')  # Notice the 'rb' to handle raw bytes
    clean_output = re.sub(ansi_escape, b'', clean_output)
    return clean_output


def decode_output(raw_output):
    """Decode the output of the command"""
    clean_output = escape_ansi(raw_output)
    # Decode the output to utf-8
    clean_output = clean_output.decode('utf-8')

    return clean_output


def clear_buffers(child):
    child._buffer = child.buffer_type()
    child._before = child.buffer_type()


def read_output(child):
    i = child.expect(
        [r'\w+\$', pexpect.TIMEOUT], timeout=0.5)
    output = b""
    # If i is 0, the command was successful and we wait for the prompt
    if i == 0:
        output = child.before + child.after
        # The output is timed out - we will check whether we didn't interrupt
        # a line by getting timeoutagain for 0.05s
    previous_size = -1
    while previous_size != len(child.before):
        i = child.expect(pexpect.TIMEOUT, timeout=0.02)
        previous_size = len(child.before)
    # output = output + decode_output(child.before)
    output = output + child.before
    print(repr(output))
    # Clear the buffers
    clear_buffers(child)
    out_lines = []
    # Render the output
    for line in output.split(b'\n'):
        stream.feed(line)
        out_lines.append(screen.display[0].rstrip())
        screen.reset()
    print('Output read')
    return '\n'.join(out_lines)


# Create a new pexpect spawn object
child = pexpect.spawn('bash')

child.sendline('sleep 1')
time.sleep(0.1)
# Get output from the shell
output = read_output(child)

print('---')
print(output)
print('---')
# print(repr(output))
