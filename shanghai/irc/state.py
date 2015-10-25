
from . import parse
import logging
logger = logging.getLogger(__name__)


class Channel:

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        """This essentially makes it a value-object."""
        return hash(parse.rfc_lower(self.name))

    def __eq__(self, other):
        if isinstance(other, Channel):
            return parse.rfc_lower(self.name) == parse.rfc_lower(other.name)
        return parse.rfc_lower(self.name) == parse.rfc_lower(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Channel({!r})'.format(self.name)


class User:

    def __init__(self, nick):
        self.nick = nick

    def __hash__(self):
        """Nickname, ident, hostname etc. can change during a connection.
        So we don't use self.nick for the hash."""
        return hash(id(self))

    def __eq__(self, other):
        if isinstance(other, User):
            return parse.rfc_lower(self.nick) == parse.rfc_lower(other.nick)
        return parse.rfc_lower(self.nick) == parse.rfc_lower(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'User({!r})'.format(self.nick)


class Join:

    def __init__(self, channel: Channel, user: User):
        self.channel = channel
        self.user = user
        self.modes = []

    def __hash__(self):
        return hash((self.channel, self.user))

    def __repr__(self):
        return 'Join({!r}, {!r})'.format(self.channel, self.user)


class Network:

    def __init__(self, mynick):
        self.mynick = mynick
        self.channels = set()
        self.users = set()
        self.joins = set()  # tuples of (Channel(), User())

    def find_channel(self, name_or_chan):
        """Return channel object with channel name <name>
        Or None if not found"""
        if isinstance(name_or_chan, Channel):
            return name_or_chan
        for channel in self.channels:
            if channel == name_or_chan:
                return channel
        return None

    def find_user(self, nick_or_user):
        """Return user object with nickname <nick>
        Or None if not found"""
        if isinstance(nick_or_user, User):
            return nick_or_user
        for user in self.users:
            if user == nick_or_user:
                return user
        return None

    def add_channel(self, name_or_chan):
        """Add a channel to the network, create if necessary, and
        return the channel object."""
        found_chan = self.find_channel(name_or_chan)
        if found_chan is None:
            found_chan = Channel(name_or_chan)
        self.channels.add(found_chan)
        return found_chan

    def add_user(self, nick_or_user):
        """Add a user to the network, create if necessary, and
        return the user object."""
        found_user = self.find_user(nick_or_user)
        if found_user is None:
            found_user = User(nick_or_user)
        self.users.add(found_user)
        return found_user

    def join(self, channel: Channel, user: User):
        """Join channel and user object.
        This means, that the user <user> is on channel <channel>."""
        self.joins.add(Join(channel, user))

    def detach(self, channel: Channel, user: User):
        """Detach channel and user object from each other.
        This means, the user <user> left the channel <channel>."""
        to_remove = set()
        for join in self.joins:
            if join.channel == channel and join.user == user:
                to_remove.add(join)
        self.joins -= to_remove

    def joined_users(self, name_or_chan):
        chan = self.find_channel(name_or_chan)
        if chan is None:
            return
        for join in self.joins:
            if join.channel == chan:
                yield join.user

    def joined_channels(self, nick_or_user):
        user = self.find_user(nick_or_user)
        if user is None:
            return
        for join in self.joins:
            if join.user == user:
                yield join.channel

    def feed_message(self, msg):
        print('\033[36;1m>>>\033[0;0m {}'.format(msg))
