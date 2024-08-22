from subprocess import PIPE, Popen
import time

# Open a cmd terminal in a new console
p = Popen('start cmd.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

# time.sleep(2.)  # wait for the terminal to open
# # Send a command to the terminal
# p.stdin.write('echo Hello, World!\n'.encode('utf-8'))
# p.stdin.flush()
