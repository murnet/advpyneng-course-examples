import asyncio
import yaml
from pprint import pprint
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


async def progress_dots():
    while True:
        yield "."


async def draw_dots():
    async for dot in progress_dots():
        print(dot, end="", flush=True)
        await asyncio.sleep(0.5)


async def send_show(device, command):
    try:
        async with AsyncScrapli(**device) as ssh:
            response = await ssh.send_command(command)
            return response.result
    except ScrapliException as error:
        print(error)


async def run_all(devices, command):
    coroutines = [send_show(dev, command) for dev in devices]
    dots = asyncio.create_task(draw_dots())
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    dots.cancel()
    return results


if __name__ == "__main__":
    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)
    output = asyncio.run(run_all(devices, "show ip int br"))
    print(output)

