
import asyncio
import logging
import io
import sys

import urwid

from shanghai.irc.messages import Message, Privmsg, CtcpRequest
from shanghai.irc.protocol import IRCProtocol
from shanghai.irc.parse import is_channel
from shanghai.irc.state import Network
from shanghai import utils


logger = logging.getLogger(__name__)


class IRCHandler:

    def __init__(self):
        self.network = Network('Shanghai|Doll')

    async def on_connected(self, prot):
        logger.info('Connected to {}:{}'
                    .format(prot.host, prot.port))
        prot.sendline('NICK {}'.format(self.network.mynick))
        prot.sendline('USER doll * * :Shanghai Doll')

    async def on_disconnect(self, prot):
        logger.info('Disconnected from {}:{}'
                    .format(prot.host, prot.port))
        loop = asyncio.get_event_loop()
        loop.call_later(30, self.reconnect, prot.host, prot.port)

    def reconnect(self, host, port):
        self.__init__()
        asyncio.ensure_future(IRCProtocol(host, port, self).run())

    async def on_message(self, prot: IRCProtocol, msg: Message):
        global main_window
        main_window.print_received_message(str(msg))
        self.network.feed_message(msg)

        if msg.isnumeric('001'):
            prot.sendline('JOIN #botted')
            prot.loop.call_later(
                15, prot.sendline,
                'PRIVMSG #botted :waited for '
                '15 seconds to say something! o/')
        if isinstance(msg, Privmsg):
            if msg.message == '+test':
                prot.sendline('QUIT :quitting you bastard!'
                              .format(msg.sender))
            elif msg.message == '+cycle':
                if is_channel(msg.target):
                    prot.sendline('PART {} :Cycling! Because I can!'
                                  .format(msg.target))
                    prot.sendline('JOIN {}'.format(msg.target))
            elif msg.message.startswith('+'):
                return

            if is_channel(msg.target) and \
                    ('http://' in msg.message or 'https://' in msg.message)\
                    and not msg.message.startswith('+'):
                def replace_url(match):
                    the_url, = match.groups('url')
                    return '\x0304\x02{}\x0F'.format(the_url)
                text = utils.url_pattern.sub(replace_url, msg.message)
                prot.sendline('PRIVMSG {} :Matched: {}'
                              .format(msg.target, text))
        if isinstance(msg, CtcpRequest):
            if msg.ctcp_command == 'VERSION':
                prot.sendline('NOTICE {} :\x01VERSION {}\x01'
                              .format(msg.sender, 'Shanghai Doll 0.1dev'))


logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    level=logging.DEBUG,
    datefmt="%d.%m.%Y %H:%M:%S",
    filename='logs/main.log',
)


loop = asyncio.get_event_loop()
handler = IRCHandler()

prot1 = IRCProtocol('irc.euirc.net', 6667, handler)
# prot2 = IRCProtocol('irc.freenode.net', 6667, IRCHandler())

asyncio.ensure_future(prot1.run())
# asyncio.ensure_future(prot2.run())

# urwid
# urwid
# urwid
# urwid

from shanghai.urwid import MainWindow
main_window = MainWindow(
    event_loop=urwid.AsyncioEventLoop(loop=loop)
)
main_window.main()
# uloop.run()

print()
