# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket
import websockets
import asyncio
import traceback

my_name=socket.gethostname()
print(my_name)
ip_address=socket.gethostbyname(my_name)
print(ip_address)

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    s.connect(('8.8.8.8',53))
    print(s.getsockname())
    ip_address=s.getsockname()[0]

async def port_scan():
    if not ip_address=='192' and not ip_address=='10' and not ip_address=='172':
        print('This is a private network: SHUTTING DOWN')
        exit()

    ip_range=ip_address.split('.')
    ip_range.pop()
    ip_range='.'.join(ip_range)
    i=0
    while i<255:
        i+=1
        target_ip=f"{ip_range}.{i}"
        uri=f"ws://{target_ip}:1111"
        try:
            connection = await asyncio.wait_for(websockets.connect(uri), timeout=2)
            await connection.send("hello")
        except ConnectionRefusedError:
            print("Server connection refused")
            pass
        except ConnectionError:
            pass
        except:
            traceback.print_exc()



async def register_client(websocket,dummy):
    async for msg in websocket:
        print(msg)
if __name__ == "__main__":
    start_server=websockets.serve(register_client,ip_address,1111)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
