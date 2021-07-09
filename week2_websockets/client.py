import Dripbox.Networking
import asyncio

async def client():
    await Dripbox.Networking.port_scan()


if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(client())
    asyncio.get_event_loop().run_forever()
