import os
import subprocess

"""
Supports cd, echo, exit, ls, pwd, and probably other things I haven't found
yet.
"""

def execute_command(command):
    try:
        subprocess.run(command.split())
    except Exception:
        print("-test: {}: command not found".format(command))


def shell_cd(path):
    try:
        os.chdir(path)
    except Exception:
        print("cd: no such file or directory: {}".format(path))


while True:
    inp = input("Enter a command: ")
    if inp == "exit":
        break
    if inp[:3] == "cd ":
        shell_cd(inp[3:])
    else:
        execute_command(inp)

exit()
