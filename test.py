
import asyncio

from shanghai.irc.messages import Message, Privmsg, CtcpRequest
from shanghai.irc.protocol import IRCProtocol
from shanghai.irc.parse import is_channel


class IRCHandler:

    async def on_connected(self, prot):
        prot.sendline('NICK Shanghai|Doll')
        prot.sendline('USER doll * * :Shanghai Doll')

    async def on_message(self, prot: IRCProtocol, msg: Message):
        print(msg)
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


prot = IRCProtocol('irc.euirc.net', 6667, IRCHandler())

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(prot.run())
except KeyboardInterrupt:
    loop.close()
print()
