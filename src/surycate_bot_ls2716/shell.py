"""Implement shell and shell communication."""
from subprocess import PIPE, Popen
from threading import Thread
import time
from typing import Tuple
import asyncio
from queue import Queue


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class Shell(object):
    """Shell object"""

    def __init__(self, command_timeout=1, sh=['bash']) -> None:
        # Open a bash process
        self.p = Popen(sh, stdin=PIPE,
                       stdout=PIPE, stderr=PIPE, shell=True)
        # Define stdout queue and stderr queue and start the threads
        self.q_stdout = Queue()
        self.q_stderr = Queue()
        self.t_stdout = Thread(target=enqueue_output,
                               args=(self.p.stdout, self.q_stdout))
        self.t_stderr = Thread(target=enqueue_output,
                               args=(self.p.stderr, self.q_stderr))
        self.t_stdout.daemon = True
        self.t_stderr.daemon = True
        self.t_stdout.start()
        self.t_stderr.start()
        self.command_timeout = command_timeout
        _ = self._get_stdout()
        _ = self._get_stderr()
        self.add_aliases()

    def add_aliases(self) -> None:
        """Expand aliases."""
        self.execute_command('shopt -s expand_aliases')
        self.execute_command('alias ll="ls -alF"')

    def send_command(self, command) -> None:
        """Send a command to the shell."""
        command += '\n'
        self.p.stdin.write(command.encode('utf-8'))
        self.p.stdin.flush()

    def execute_command(self, command: str, timeout: float = None
                        ) -> Tuple[str, str, int]:
        """Execute a command.

        Args:
            command (str): The command to execute.
            timeout (float): The timeout for the command.
        Returns the output, error, and status code.
        """
        if timeout is None:
            timeout = self.command_timeout
        self.send_command(command)
        self.send_command('echo "STATUS_CODE=$?"')
        output = ""
        time_start = time.time()
        while not output.__contains__('STATUS_CODE='):
            output += self._get_stdout()
            time.sleep(0.01)
            if time.time() - time_start > timeout:
                raise TimeoutError("Timeout while waiting for command output.")
        status_code = int(output.split('\n')[-2].split('=')[1])
        error = self._get_stderr()
        return output, error, status_code

    def _get_stdout(self, timeout: float = 0.5) -> str:
        """Get the stdout."""
        output = ''
        while not self.q_stdout.empty():
            output += self.q_stdout.get(timeout=0.5).decode('utf-8')
        return output

    def _get_stderr(self, timeout: float = 0.5) -> str:
        """Get the stderr."""
        output = ''
        while not self.q_stderr.empty():
            output += self.q_stderr.get(timeout=0.5).decode('utf-8')
        return output

    def close(self) -> None:
        """Close the shell."""
        self.p.terminate()
        self.p.wait()


# Some scratch tests
if __name__ == "__main__":
    shell = Shell(sh=['bash'])
    shell.send_command('ll')
    shell.send_command('echo "STATUS_CODE=$?"')
    time.sleep(0.5)
    output = shell.get_stdout()
    status_code = int(output.split('\n')[-2].split('=')[1])
    print(f"Output: {output}")
    print(f"Status code: {status_code}")
    shell.close()
    print("Shell closed.")
