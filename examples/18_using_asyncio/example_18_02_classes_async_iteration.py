import asyncio
import yaml
from pprint import pprint
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


class ProgressBar:
    def __init__(self, symbol="."):
        self.symbol = symbol

    async def __anext__(self):
        return self.symbol

    def __aiter__(self):
        return self


async def draw_progress():
    async for sym in ProgressBar():
        print(sym, end="", flush=True)
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
    bar = asyncio.create_task(draw_progress())
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    return results


if __name__ == "__main__":
    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)
    output = asyncio.run(run_all(devices, "show ip int br"))
    print(output)
