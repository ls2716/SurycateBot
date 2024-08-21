import pexpect
import sys
import time
# Start a bash shell
child = pexpect.spawn('/bin/bash', timeout=0.01)

# # Log to console
# child.logfile = sys.stdout.buffer

# Send a command that produces continuous output
child.sendline('ls -l')
# time.sleep(1)

# Continuously read and print the output
while True:
    try:
        line = child.readline()
        # Print each line as it comes in
        print(line.decode('utf-8'), end='\n')
    except pexpect.EOF:
        break  # End of file, exit loop
    except KeyboardInterrupt:
        # Stop tailing on a keyboard interrupt
        child.sendcontrol('c')  # Send Ctrl+C to stop tail
        break
    except pexpect.TIMEOUT:
        pass


# Close bash shell
child.sendline('exit')
child.expect(pexpect.EOF)
