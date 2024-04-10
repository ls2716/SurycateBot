"""Implement shell and shell communication."""
import sys
from subprocess import PIPE, Popen
from threading import Thread
import time

from queue import Queue, Empty


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class Shell(object):
    """Shell object"""

    def __init__(self, command_time=0.5) -> None:
        # Open a powershell process
        self.p = Popen(['powershell'], stdin=PIPE,
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
        self.command_time = command_time
        time.sleep(self.command_time)
        _ = self.get_stdout()

    def send_command(self, command) -> None:
        """Send a command to the shell."""
        command += '\n'
        self.p.stdin.write(command.encode('utf-8'))
        self.p.stdin.flush()
        time.sleep(self.command_time)

    def get_stdout(self, timeout=0.5) -> str:
        """Get the stdout."""
        output = ''
        while not self.q_stdout.empty():
            output += self.q_stdout.get(timeout=0.5).decode('utf-8')
        return output

    def get_stderr(self, timeout=0.5) -> str:
        """Get the stderr."""
        output = ''
        while not self.q_stderr.empty():
            output += self.q_stderr.get(timeout=0.5).decode('utf-8')
        return output

    def close(self) -> None:
        """Close the shell."""
        self.p.terminate()
        self.p.wait()
