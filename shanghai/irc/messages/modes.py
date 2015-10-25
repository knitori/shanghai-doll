
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
        target = self.params[0]
        if parse.is_channel(target):
            # assume channel mode
            pass
        else:
            # assume user mode
            pass
