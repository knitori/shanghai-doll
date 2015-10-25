
from . import Message, register_derivative
from .. import parse
from itertools import zip_longest
import re

import logging
logger = logging.getLogger(__name__)


class Ping(Message, metaclass=register_derivative):

    def pong(self):
        return parse.make_line(None, 'PONG', self.middle,
                               self.params, self.trailing)


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
            elif key == 'CHANMODES':
                self.options[key] = tuple(value.split(','))
            else:
                self.options[key] = value

    def __repr__(self):
        chunks = zip_longest(*[iter(self.options)]*3)
        output = ''
        for cols in chunks:
            row = []
            for key in cols:
                if key is None:
                    break
                row.append('{:<50}'.format(key+'='+str(self.options[key])))
            output += '    {}\n'.format(' '.join(row))
        return '<005>\n{}'.format(output)
