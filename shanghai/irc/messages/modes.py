
from . import Message, register_derivative
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Mode(Message, metaclass=register_derivative):
    """
    Channelmode:
    :Nitori!~kappa@chireiden.net MODE #botted +v Shanghai|Doll

    Usermode:
    :Shanghai|Doll MODE Shanghai|Doll :+ix
    """

    def process(self):
        self.target = self.params[0]
        self.modes = list(parse.parse_modes(self.params[1]))
        self.args = self.params[2:]

    def __repr__(self):
        if parse.is_channel(self.target):
            return 'ChannelMode({s.target!r}, {s.modes}, args={s.args})'\
                .format(s=self)
        else:
            return 'UserMode({s.target!r}, {s.modes}, args={s.args})'\
                .format(s=self)
