""" This file is for experimentation with the pexpect library.
"""

# Import the pexpect library
# import pexpect
# Import the replwrap module from the pexpect library
from pexpect import replwrap

# Start the child process
child = replwrap.bash()

# Send a command to the child process
output = child.run_command('ssh lukasz@ls314.com', timeout=5)

# Print the output of the command
print(output)


# Does not work with ssh
