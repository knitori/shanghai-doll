
from .parse import pack_message
from .messages import Message, Ping
import asyncio


class IRCProtocol:

    def __init__(self, host, port, handler, *, ssl=False, loop=None):
        self.host = host
        self.port = port
        self.ssl = ssl
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self._handler = handler

    async def run(self):
        reader, writer = await asyncio.open_connection(
            self.host, self.port, ssl=self.ssl, loop=self.loop)
        self.writer = writer

        await self._handler.on_connected(self)

        while not reader.at_eof():
            line = await reader.readline()
            line = line.strip().decode('utf-8', 'replace')
            if line:
                msg = Message.from_line(line)
                if isinstance(msg, Ping):
                    self.sendmsg(msg.pong())
                await self._handler.on_message(self, msg)

    def sendmsg(self, msg):
        self.sendline(pack_message(msg))

    def sendline(self, line):
        print('>>> {}'.format(line))
        self.writer.write('{}\r\n'.format(line).encode('utf-8'))
