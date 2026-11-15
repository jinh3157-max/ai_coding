import time, paramiko
from getpass import getpass


def qytang_multicmd(ip, username, password, cmd_list, wait_time=2, verbose=True):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname = ip,
        username = username,
        password = password,
        look_for_keys = False,
        allow_agent = False
    )
    chan = ssh.invoke_shell()
    time.sleep(1)
    welcome = chan.recv(65535)
    result = ""

    for command in cmd_list:
        chan.sendall((command + "\n").encode())
        time.sleep(wait_time) 
        output = chan.recv(65535).decode()
        result += output
        if verbose:
            print(output, end="")
    print("")
    ssh.close()

if __name__ == "__main__":
        
    cmd_list = [
    'terminal length 0',
    'show version | include Software,',
    'show running-config | include hostname',
    ]

    qytang_multicmd(
        ip = "10.1.1.1",
        username = "admin",
        password = getpass("SSH Password: "),
        cmd_list = cmd_list
    )