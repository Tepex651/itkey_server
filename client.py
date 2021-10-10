import asyncio
import random
import yaml
import datetime
import sys


config = 'config.yaml'
try:
    with open(config, 'r') as file:
        full_file = yaml.load(file, Loader=yaml.FullLoader)
        configs = [full_file[server] for server in full_file]
except OSError:
    print("Could not open/read file:", config)
    sys.exit()


async def connect_client(**conf):
    """Jpens connection. Starts send_seconds and read_answer at the same time"""
    reader, writer = await asyncio.open_connection(conf['host'], conf['port'])
    print(f"{datetime.datetime.now().time()} - Openned connection with server {conf['id']} port - {conf['port']}")
    await asyncio.gather(send_seconds(writer, conf['id']), read_answer(reader, conf['id']))


async def send_seconds(writer, server_id):
    """Start sending random seconds to server"""
    while True:
        seconds_for_server = str(random.randint(1, 10)) + '\n'
        seconds_for_client = random.randint(1, 10)
        await asyncio.sleep(seconds_for_client)
        print(f'{datetime.datetime.now().time()} - Send to server {server_id}: {seconds_for_server}')
        writer.write(seconds_for_server.encode())
        await writer.drain()


async def read_answer(reader, server_id):
    """Reads answers from server and print them"""
    while True:
        data = await reader.readline()
        message = data.decode().split('\n')[0]
        print(f'{datetime.datetime.now().time()} - Received from server {server_id}: {message}')


async def main():
    """Makes list of connections coroutines and start them at the same time"""
    connections = [connect_client(**conf) for conf in configs]
    await asyncio.gather(*connections)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Connection was closed')