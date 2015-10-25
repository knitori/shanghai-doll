
from . import Message, register_derivative
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Join(Message, metaclass=register_derivative):

    def process(self):
        pass


class Part(Message, metaclass=register_derivative):

    def process(self):
        pass


class Kick(Message, metaclass=register_derivative):

    def process(self):
        pass


class Quit(Message, metaclass=register_derivative):

    def process(self):
        pass


class Nick(Message, metaclass=register_derivative):

    def process(self):
        pass
