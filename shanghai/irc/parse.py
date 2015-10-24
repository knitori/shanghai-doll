
from collections import namedtuple
import re

Line = namedtuple('Line', 'prefix command middle params trailing')
Prefix = namedtuple('Prefix', 'nick ident hostname')


def unpack_prefix(prefix):
    match = re.match(
        r'^(?P<nick>[^!@]+)'
        r'(?:!(?P<ident>[^!@]+))?'
        r'(?:@(?P<hostname>[^!@]+))?$', prefix)
    if match is not None:
        return Prefix(*match.groups())


def unpack_line(line):
    prefix = None
    if line[0:1] == ':':
        prefix, line = line.split(None, 1)
        prefix = unpack_prefix(prefix[1:])

    if ' :' in line:
        tmp_str, trailing = line.split(' :', 1)
        tmp_args = tmp_str.split()
    else:
        trailing = None
        tmp_args = line.split()

    command, *middle = tmp_args

    params = middle[:]
    if trailing is not None:
        params.append(trailing)

    return Line(prefix, command, middle, params, trailing)


def pack_prefix(prefix):
    if not isinstance(prefix, Prefix):
        prefix = Prefix(*prefix)
    prefix_str = prefix.nick
    if prefix.ident is not None:
        prefix_str += '!' + prefix.ident
    if prefix.hostname is not None:
        prefix_str += '@' + prefix.hostname
    return prefix_str


def pack_message(msg):
    if not isinstance(msg, Line):
        msg = Line(*msg)
    if msg.prefix is None:
        parts = [msg.command.upper()]
    else:
        parts = [':' + pack_prefix(msg.prefix), msg.command.upper()]

    parts.extend(msg.middle)
    if msg.trailing is not None:
        parts.append(':' + msg.trailing)
    return ' '.join(parts)


def make_line(*args):
    return Line(*args)


def is_channel(chan):
    # any octet except NUL, BELL, CR, LF, " ", "," and ":"
    # starting with any of: #+&!
    if all(c not in '\0\a\r\n ,:' for c in chan):
        if chan.startswith(('#', '+', '&', '!')):
            return True
    return False


def rfc_lower(s):
    """https://tools.ietf.org/html/rfc2812#section-2.2
    {}|^ --> []\\~"""
    s = s.lower()
    s = s.replace('{', '[')
    s = s.replace('}', ']')
    s = s.replace('|', '\\')
    s = s.replace('^', '~')
    return s


def rfc_upper(s):
    """https://tools.ietf.org/html/rfc2812#section-2.2
    []\\~ --> {}|^"""
    s = s.lower()
    s = s.replace('[', '{')
    s = s.replace(']', '}')
    s = s.replace('\\', '|')
    s = s.replace('~', '^')
    return s
