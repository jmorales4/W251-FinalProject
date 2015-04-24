import subprocess, shlex

pid = ""
with open('log.kill', 'r') as l:
        pid = l.readline().split(' ')[5]
        print pid
if pid != "":
        command = shlex.split('kill '+str(pid))
        command = 'kill '+str(pid)
        p = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
        print p.communicate()[0]