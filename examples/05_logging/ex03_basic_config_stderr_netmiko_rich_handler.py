from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat
import logging

import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException
from netmiko.exceptions import SSHException
from rich.logging import RichHandler


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.INFO)

fmt = logging.Formatter("{asctime} {name} {levelname} {message}", style="{")
lfile = logging.FileHandler("logfile.txt")
lfile.setLevel(logging.DEBUG)
lfile.setFormatter(fmt)

logging.basicConfig(
    level=logging.DEBUG,
    format="{message}",
    style="{",
    datefmt="%X",
    handlers=[RichHandler(), lfile],
    # handlers=[RichHandler(rich_tracebacks=True)],
    # handlers=[RichHandler(show_path=False)], # отключить вывод имени файла и строки
)


def send_show(device_dict, command):
    ip = device_dict["host"]
    logging.info(f"===>  Connection: {ip}")

    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            logging.debug(f"<===  Received:   {ip}")
            logging.debug(f"Получен вывод команды {command} с {ip}")
        return result
    except SSHException as error:
        # logging.exception(f"Ошибка {type(error)} на {ip}") # вывод с traceback
        logging.error(f"Ошибка {type(error)} на {ip}")


def send_command_to_devices(devices, command, threads=2):
    data = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        result = executor.map(send_show, devices, repeat(command))
        for device, output in zip(devices, result):
            data[device["host"]] = output
    return data


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, "sh clock")
