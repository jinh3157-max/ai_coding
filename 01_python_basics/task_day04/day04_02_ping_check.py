from pythonping import ping

def ping_check(ip, count = 1, timeout = 2):
    result = ping(ip, count = count, timeout = timeout, verbose = False)
    if result.success():
        return True, result.rtt_avg_ms
    else:
        return False, None

if __name__ == "__main__":

     hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']
     for ip in hosts:
        success, rtt = ping_check(ip)
        print(ip, end="   ")
        if success:
            print("可达", end="   ")
            print(rtt, "ms")
        else:
            print("不可达")