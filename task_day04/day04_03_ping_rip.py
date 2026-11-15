from day04_02_ping_check import ping_check
from day04_01_multicmd import qytang_multicmd
from getpass import getpass
if __name__ == "__main__":
    hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']
    RIP_COMMANDS = [
        'configure terminal',
        'router rip',
        'version 2',
        'network 172.16.0.0',
        'end',
    ]
    password = getpass("SSH密码:")
    for ip in hosts:
        success, rtt = ping_check(ip)
        if success:
            print(f"[{ip}] ping通,开始配置RIP")
            qytang_multicmd(
            ip = ip,
            username = "admin",
            password = password,
            cmd_list = RIP_COMMANDS
            )
            print(f"[{ip}] ping通,RIP命令执行完成")
            print("")

        else:
            print(f"[{ip}] ping不通,跳过SSH")