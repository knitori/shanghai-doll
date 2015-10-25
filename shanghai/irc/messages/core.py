
from . import Message, register_derivative
from .. import parse
import re
import logging
logger = logging.getLogger(__name__)


class Ping(Message, metaclass=register_derivative):

    def pong(self):
        return parse.make_line(None, 'PONG', self.middle,
                               self.params, self.trailing)

    def __repr__(self):
        return '<Ping?> <Pong!>'


class Numeric005(Message, metaclass=register_derivative):

    def process(self):
        self.options = {}
        for option in self.middle[1:]:
            if '=' in option:
                key, value = option.split('=', 1)
                key = key.upper()
            else:
                key, value = option.upper(), True

            if key == 'PREFIX':
                match = re.match(r'\((.*)\)(.*)$', value)
                self.options[key] = tuple(match.groups())
            else:
                self.options[key] = value

    def __repr__(self):
        return '005[{!r}]'.format(self._pkg)
