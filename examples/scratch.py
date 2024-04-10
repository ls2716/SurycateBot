import sys
from subprocess import PIPE, Popen
from threading import Thread
import time

from queue import Queue, Empty


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


p = Popen(['powershell'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True  # thread dies with the program
t.start()

time.sleep(.5)
# Check if queue is empty
if q.empty():
    print('Queue is empty')
else:
    print('Queue is not empty')

while not q.empty():
    output = q.get(timeout=1)
    print(output.decode('utf-8'))

# # Execute a command
p.stdin.write(b'ls\n')
p.stdin.flush()

time.sleep(2)

while not q.empty():
    output = q.get(timeout=1)
    print(output.decode('utf-8'), end='')
