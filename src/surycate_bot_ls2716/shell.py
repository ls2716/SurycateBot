"""Implement shell and shell communication."""
from subprocess import PIPE, Popen
from threading import Thread
import time
from typing import Tuple
import asyncio
from queue import Queue
import pexpect
import re
import pyte


class PexpectShell(object):
    """Pexpect shell object

    How does the PexpectShell work?
    The purpose of the Pexpect shell is to interact with the shell using the pexpect library.

    The PexpectShell is initialised by creating a child process using the pexpect.spawn() function
    with the 'bash' command as an argument. The child process is stored in the self.child attribute.

    There are following methods to interact with the PexpectShell object:
    - send_command: Sends a command to the shell.
        This method sends a command to the shell using the sendline() method of the self.child object.
        It does not return anything.
    - get_output: Gets the output from the shell.
        This method gets the current output from the shell. It works as follows.
        It uses the expect() method of the self.child object to wait for the shell prompt.
        Either the expect returns a prompt sign \$ or a timeout.
        If the prompt is returned, the output is decoded and returned.
        If the timeout is returned, the output is decoded and returned but there
        is a check that the output does not contain half of the line.
        The output is decoded using the _decode_output() method.
        The timeouted output is cleared using the clear_buffers() method and
        the output is returned with a code 1 to mark a timeout.
    - get_last_lines: Gets the last lines of the output.
        This method returns the last n lines of the output.
    - execute_command: Executes a command.
        This method sends a command to the shell using the send_command() method and
        waits for the output using the get_output() method.
    - close: Closes the shell.

    The shell also aggregates the output so that at any time the output can be retrieved.

    """

    def __init__(self, command_timeout: float = 2.) -> None:
        # Start the child process
        self.child = pexpect.spawn('bash')
        self.command_timeout = command_timeout
        self.terminal_content = ['']
        # Initialise the terminal for rendering the output
        self.screen = pyte.Screen(150, 1)
        self.stream = pyte.ByteStream(self.screen)

    def send_command(self, command: str) -> None:
        """Send a command to the shell.

        Arguments:
        - command (str): The command to be sent to the shell.
        Returns:
        - None
        """
        self.child.sendline(command)

    def get_output(self, timeout=None) -> str:
        """Get output from the shell.

        Arguments:
        - timeout (float): The timeout for the expect method.
        Returns:
        - str: The output from the shell
        """
        if timeout is None:
            timeout = self.command_timeout
        # Expect a prompt or a timeout
        i = self.child.expect(
            [r'\w+\$', pexpect.TIMEOUT], timeout=timeout)
        # Initialise output
        output = b""
        # If the prompt is returned decode both before and after
        if i == 0:
            output = self.child.before + self.child.after
        # If the timeout is returned, wait for the output to be complete
        previous_size = -1  # Set dummy previous size
        # While the size changes after 0.02 seconds read the output again
        while previous_size != len(self.child.before):
            i = self.child.expect(pexpect.TIMEOUT, timeout=0.02)
            previous_size = len(self.child.before)
        # Decode the additional output
        output = output + self.child.before
        output_lines = []
        # Render the output using the pyte library
        # For each line in the output
        # Feed the line to the stream, render the screen
        # and append the line to the output_lines
        for line in output.split(b'\n'):
            self.stream.feed(line)
            output_lines.append(self.screen.display[0].rstrip())
            self.screen.reset()
        # Clear the buffers
        self.child._buffer = self.child.buffer_type()
        self.child._before = self.child.buffer_type()
        # Append the output to the last line of terminal content
        # This will be returned as the output
        returned_output = self.terminal_content[-1] + '\n'.join(output_lines)
        # Append the first line to the last line
        self.terminal_content[-1] += output_lines[0]
        # Append the rest of the lines as elements
        self.terminal_content += output_lines[1:]
        # Add a space at the end of the terminal content if it ends with a prompt
        if returned_output.endswith('$'):
            self.terminal_content[-1] += ' '
            returned_output += ' '
        # Return the output and the status code
        return returned_output

    def get_last_lines(self, n: int) -> str:
        """Get the last n lines of the output.

        Arguments:
        - n (int): The number of lines to return.
        Returns:
        - str: The last n lines of the output.
        """
        return '\n'.join(self.terminal_content[-n:]) if n > 0 else ''

    def close(self) -> None:
        """Close the shell."""
        self.child.close()

    def execute_command(self, command: str, command_time=0.1) -> str:
        """Execute a command.

        Uses the send_command and get_output methods to execute a command and get the output.

        Arguments:
        - command (str): The command to execute.
        - command_time (float): The time to wait before getting the output.
        Returns:
        - str: The output from the command.
        """
        self.send_command(command)
        time.sleep(command_time)
        return self.get_output()
