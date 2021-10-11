import os

import asyncio


server_id = 'server ' + os.environ['SERVER_ID']


async def handle_echo(reader, writer):
    """Reads seconds and create task 'wait_and_write' for each inputed second"""
    while True:
        data = await reader.readline()
        if not data:
            writer.close()
            await writer.wait_closed()
            break
        seconds = data.decode().split('\n')[0]
        print(f'I get {seconds}')
        task = asyncio.create_task(wait_and_write(writer, seconds))
        # print(f'i create {task, type(task)}')
        # print('ALL TASKS =', len(asyncio.all_tasks()))
    
    
async def wait_and_write(writer, seconds):
    """Sleeps 'seconds'. After that writes message to client"""
    await asyncio.sleep(int(seconds))
    message = f"{server_id}-{seconds}\n"
    if writer.is_closing():
        print("Can't send message. Connection was closed")
    else:
        print(f"Send: {message}")
        writer.write(message.encode())
        
                
async def main():
    server = await asyncio.start_server(handle_echo, '0.0.0.0', 6000)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())