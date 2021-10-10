import os

import asyncio


server_id = 'server ' + os.environ['SERVER_ID']


async def read(reader, writer, queue):
    """Reads messages and create task 'wait_and_write'. Fills the queue."""
    while True:
        data = await reader.readline()
        if not data:
            writer.close()
            await writer.wait_closed()
            break
        seconds = data.decode().split('\n')[0]
        print(f'I get {seconds}')
        queue.put_nowait(seconds)
        task = asyncio.create_task(wait_and_write(writer, queue))
        # print(f'i create {task, type(task)}')
        # print('ALL TASKS =', len(asyncio.all_tasks()))
    
    
async def wait_and_write(writer, queue):
    """Gets 'seconds' from queue. Sleeps. After that writes message to client"""
    seconds = await queue.get()
    queue.task_done()
    await asyncio.sleep(int(seconds))
    message = f"{server_id}-{seconds}\n"
    if writer.is_closing():
        print("Can't send message. Connection was closed")
    else:
        print(f"Send: {message}")
        writer.write(message.encode())
        
        
async def handle_echo(reader, writer):
    """Creates queue and start task 'read'"""
    queue = asyncio.Queue()
    await asyncio.create_task(read(reader, writer, queue))
    await queue.join()

        
async def main():
    server = await asyncio.start_server(handle_echo, '0.0.0.0', 6000)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())