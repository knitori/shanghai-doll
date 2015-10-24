
from . import Message, register_derivative
from .. import parse


class BaseCtcp(Message):

    def process(self):
        self.sender = self.prefix.nick
        self.target = self.middle[0]
        ctcp = self.trailing.strip('\x01').strip().split(None, 1)
        if len(ctcp) == 2:
            self.ctcp_command = ctcp[0].upper()
            self.ctcp_message = ctcp[1]
        else:
            self.ctcp_command = ctcp[0].upper()
            self.ctcp_message = None


class CtcpRequest(BaseCtcp):
    def __repr__(self):
        if self.ctcp_message is not None:
            return '@{s.sender}@ CTCP REQUEST {s.ctcp_command}: ' \
                   '{s.ctcp_message}'.format(s=self)
        else:
            return '@{s.sender}@ CTCP REQUEST {s.ctcp_command}'.format(s=self)


class CtcpResponse(BaseCtcp):
    def __repr__(self):
        if self.ctcp_message is not None:
            return '@{s.sender}@ CTCP REPLY {s.ctcp_command}: ' \
                   '{s.ctcp_message}'.format(s=self)
        else:
            return '@{s.sender}@ CTCP REPLY {s.ctcp_command}'.format(s=self)


class Privmsg(Message, metaclass=register_derivative):

    def process(self):
        self.sender = self.prefix.nick
        self.target = self.middle[0]
        self.message = self.trailing

    def __new__(cls, pkg):
        """If message is in ctcp format, create a CtcpRequest instead
        """
        if pkg.trailing.startswith('\x01') and pkg.trailing.endswith('\x01'):
            instance = super().__new__(CtcpRequest)
            instance.__init__(pkg)  # needed, if: cls != instance.__class__
        else:
            instance = super().__new__(cls)
        return instance

    def __repr__(self):
        target = self.middle[0]
        if parse.is_channel(target):
            return '[{s.target}] <{s.sender}> {s.message}'.format(s=self)
        else:
            return '@query <{s.sender}> {s.message}'.format(s=self)


class Notice(Message, metaclass=register_derivative):
    def process(self):
        if self.prefix is not None:
            self.sender = self.prefix.nick
        else:
            self.sender = None
        self.target = self.middle[0]
        self.message = self.trailing

    def __new__(cls, pkg):
        if pkg.trailing.startswith('\x01') and pkg.trailing.endswith('\x01'):
            instance = super().__new__(CtcpResponse)
            instance.__init__(pkg)  # needed, if: cls != instance.__class__
        else:
            instance = super().__new__(cls)
        return instance

    def __repr__(self):
        target = self.middle[0]
        if parse.is_channel(target) and self.prefix is not None:
            return '({s.target}) -notice- -{s.sender}- {s.message}'\
                .format(s=self)
        elif parse.is_channel(target):
            return '({s.target}) -server-notice- {s.message}'.format(s=self)
        elif self.prefix is not None:
            return '-notice- -{s.sender}- {s.message}'.format(s=self)
        else:
            return '-server-notice- {s.message}'.format(s=self)
