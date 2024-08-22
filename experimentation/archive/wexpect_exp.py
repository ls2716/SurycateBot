import wexpect
prompt = '[A-Z]\:.+>'

child = wexpect.spawn('cmd.exe')
child.expect(prompt)    # Wait for startup prompt

child.sendline('dir')   # List the current directory
child.expect(prompt)

print(child.before)     # Print the list
child.sendline('exit')
