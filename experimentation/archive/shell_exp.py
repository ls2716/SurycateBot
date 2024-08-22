from surycate_bot_ls2716.shell import Shell
import time
s = Shell(sh=['bash'])

s.send_command('ssh lukasz@ls314.com "echo Hello, World!"')
time.sleep(1.)
o = s._get_stdout()
e = s._get_stderr()


print(o)
print(e)
# print(c)
