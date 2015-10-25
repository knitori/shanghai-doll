
from . import Message, register_derivative
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Join(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.channel = self._pkg.params[0]

    def __repr__(self):
        return '* {} joined {}'.format(self.subject, self.channel)


class Part(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.channel = self._pkg.middle[0]
        self.message = self._pkg.trailing

    def __repr__(self):
        if self.message is None:
            return '* {} parted {}'.format(self.subject, self.channel)
        return '* {} parted {} ({})'.format(
            self.subject, self.channel, self.message)


class Kick(Message, metaclass=register_derivative):

    def process(self):
        self.kicker = self._pkg.prefix.nick
        self.channel = self._pkg.middle[0]
        self.kicked = self._pkg.middle[1]
        self.reason = self._pkg.trailing

    def __repr__(self):
        if self.reason is None:
            return '* {s.kicked} was kicked by {s.kicker} from {s.channel}'\
                .format(s=self)
        return '* {s.kicked} was kicked by {s.kicker} from {s.channel}. ' \
               'Reason: {s.reason}'.format(s=self)


class Quit(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.message = self._pkg.trailing

    def __repr__(self):
        if self.message is None:
            return '* {} quitted'.format(self.subject)
        return '* {} quitted ({})'.format(self.subject, self.message)


class Nick(Message, metaclass=register_derivative):

    def process(self):
        self.subject = self._pkg.prefix.nick
        self.newnick = self._pkg.params[0]

    def __repr__(self):
        return '* {} changed its nickname to {}'.format(
            self.subject, self.newnick)
