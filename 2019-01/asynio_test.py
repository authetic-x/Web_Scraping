import threading
import asyncio

@asyncio.coroutine
def hello():
    print("Hello")
    yield from asyncio.sleep(1)
    print(" world")

async def new_hello():
    print("Hello")
    await asyncio.sleep(1)
    print(" world")

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET /HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.baidu.com', 'www.sina.com', 'www.sohu.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()