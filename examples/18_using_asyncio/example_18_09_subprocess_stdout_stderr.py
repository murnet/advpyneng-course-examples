import asyncio


async def ping(ip):
    cmd = f"ping -c 3 -n {ip}".split()
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        # encoding="utf-8",
    )
    stdout, stderr = await proc.communicate()
    if " 0% packet loss" in stdout.decode():
        return True
    else:
        return False


async def ping_ip_list(ip_list):
    coroutines = [ping(ip) for ip in ip_list]
    result = await asyncio.gather(*coroutines)
    return result


if __name__ == "__main__":
    ip_list = ["192.168.139.1", "192.168.100.2", "8.8.8.8"]
    results = asyncio.run(ping_ip_list(ip_list))
    print(results)
