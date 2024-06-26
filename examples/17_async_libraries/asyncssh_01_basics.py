import asyncio
import asyncssh


async def send_show(device, show):
    host = device["host"]
    print(f"Подключаюсь к {host}")
    ssh = await asyncssh.connect(**device)
    writer, reader, _ = await ssh.open_session()
    # stdin, stdout, stderr = await ssh.open_session()
    await reader.readuntil(">")
    writer.write("enable\n")
    await reader.readuntil("Password")
    writer.write("cisco\n")
    await reader.readuntil("#")
    writer.write("terminal length 0\n")
    await reader.readuntil("#")
    print(f"Отправляю команду {show} на {host}")
    writer.write(f"{show}\n")
    output = await reader.readuntil("#")
    ssh.close()
    print(f"Получили результат от {host}")
    return output



if __name__ == "__main__":
    params = {"username": "cisco", "password": "cisco", "connect_timeout": 5}
    hosts = ["192.168.139.1", "192.168.139.2", "192.168.139.3"]
    devices = [{"host": ip, **params} for ip in hosts]
    r1 = devices[0]

    print(asyncio.run(send_show(r1, "sh ip int br")))
