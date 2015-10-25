
from .. import parse
import logging
logger = logging.getLogger(__name__)


class Message:
    _command_map = {}

    def __init__(self, pkg):
        self._pkg = pkg
        self.prefix = pkg.prefix
        self.command = pkg.command
        self.middle = pkg.middle
        self.params = pkg.params
        self.trailing = pkg.trailing
        self.process()

    def process(self):
        pass

    def isnumeric(self, number=None):
        if number is None:
            return self.command.isdigit()
        return self.command.isdigit() and int(self.command) == int(number)

    @classmethod
    def from_line(cls, line):
        msg = parse.unpack_line(line)
        if msg.command.isdigit():
            command = 'Numeric{}'.format(msg.command)
        else:
            command = msg.command
        return cls._command_map.get(command.upper(), cls)(msg)

    def __repr__(self):
        return parse.pack_message(self._pkg)


def register_derivative(name, bases, attr):
    """wizardry"""
    new_cls = type(name, bases, attr)

    for cls in bases:
        cmd_map = getattr(cls, '_command_map', None)
        if cmd_map is not None:
            command = name.upper()
            if command in cmd_map:
                raise KeyError('command {} is already registered to this '
                               'class'.format(command))
            cmd_map[command] = new_cls
    return new_cls
