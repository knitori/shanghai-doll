
from . import Message, register_derivative
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Ping(Message, metaclass=register_derivative):

    def pong(self):
        return parse.make_line(None, 'PONG', self.middle,
                               self.params, self.trailing)

    def __repr__(self):
        return '<Ping?> <Pong!>'
