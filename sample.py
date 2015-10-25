
import asyncio
import logging

from shanghai.irc.messages import Message, Privmsg, CtcpRequest
from shanghai.irc.protocol import IRCProtocol
from shanghai.irc.parse import is_channel
from shanghai.irc.state import Network

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    level=logging.DEBUG,
    datefmt="%d.%m.%Y %H:%M:%S")
logger = logging.getLogger(__name__)


class IRCHandler:

    def __init__(self):
        self.network = Network('Shanghai|Doll')

    async def on_connected(self, prot):
        prot.sendline('NICK {}'.format(self.network.mynick))
        prot.sendline('USER doll * * :Shanghai Doll')

    async def on_disconnect(self, prot):
        print('Disconnected from {}'.format(prot))

    async def on_message(self, prot: IRCProtocol, msg: Message):
        self.network.feed_message(msg)

        if msg.isnumeric('001'):
            prot.sendline('JOIN #botted')
            prot.loop.call_later(
                15, prot.sendline,
                'PRIVMSG #botted :waited for '
                '15 seconds to say something! o/')
        if isinstance(msg, Privmsg):
            if msg.message == '+test':
                prot.sendline('PRIVMSG {} :\x01VERSION\x01'
                              .format(msg.sender))
            elif msg.message == '+cycle':
                if is_channel(msg.target):
                    prot.sendline('PART {}'.format(msg.target))
                    prot.sendline('JOIN {}'.format(msg.target))
        if isinstance(msg, CtcpRequest):
            if msg.ctcp_command == 'VERSION':
                prot.sendline('NOTICE {} :\x01VERSION {}\x01'
                              .format(msg.sender, 'Shanghai Doll 0.1dev'))


loop = asyncio.get_event_loop()

prot1 = IRCProtocol('irc.euirc.net', 6667, IRCHandler())
# prot2 = IRCProtocol('irc.freenode.net', 6667, IRCHandler())

asyncio.ensure_future(prot1.run())
# asyncio.ensure_future(prot2.run())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
print()
