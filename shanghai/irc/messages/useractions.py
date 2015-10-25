
from . import Message, register_derivative
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Join(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.channel = self._pkg.params[0]

    def __repr__(self):
        return '\033[34;1m* {} joined {}\033[0m'\
            .format(self.subject, self.channel)


class Part(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.channel = self._pkg.middle[0]
        self.message = self._pkg.trailing

    def __repr__(self):
        if self.message is None:
            return '\033[35;1m* {} parted {}\033[0m'\
                .format(self.subject, self.channel)
        return '\033[35;1m* {} parted {} ({})\033[0m'.format(
            self.subject, self.channel, self.message)


class Kick(Message, metaclass=register_derivative):

    def process(self):
        self.kicker = self._pkg.prefix.nick
        self.channel = self._pkg.middle[0]
        self.kicked = self._pkg.middle[1]
        self.reason = self._pkg.trailing

    def __repr__(self):
        if self.reason is None:
            return '\033[44;1m* {s.kicked} was kicked by {s.kicker} ' \
                   'from {s.channel}\033[0m'.format(s=self)
        return '\033[44;1m* {s.kicked} was kicked by {s.kicker} ' \
               'from {s.channel}. Reason: {s.reason}\033[0m'.format(s=self)


class Quit(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.message = self._pkg.trailing

    def __repr__(self):
        if self.message is None:
            return '\033[30;1m* {} quitted\033[0m'.format(self.subject)
        return '\033[30;1m* {} quitted ({})\033[0m'.format(self.subject, self.message)


class Nick(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.newnick = self._pkg.params[0]

    def __repr__(self):
        return '\033[43;1m* {} changed its nickname to {}\033[0m'.format(
            self.subject, self.newnick)
