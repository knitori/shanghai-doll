
from . import parse


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

    def __eq__(self, other):
        if isinstance(other, User):
            return parse.rfc_lower(self.nick) == parse.rfc_lower(other.nick)
        return parse.rfc_lower(self.nick) == parse.rfc_lower(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'User({!r})'.format(self.nick)


class Network:

    def __init__(self, mynick):
        self.mynick = mynick
        self.channels = set()
        self.users = set()
        self.joins = set()  # tuples of (Channel(), User())

    def find_channel(self, name: str):
        """Return channel object with channel name <name>
        Or None if not found"""
        for channel in self.channels:
            if channel == name:
                return channel
        return None

    def find_user(self, nick: str):
        """Return user object with nickname <nick>
        Or None if not found"""
        for user in self.users:
            if user == nick:
                return user
        return None

    def add_channel(self, name_or_chan):
        """Add a channel to the network, create if necessary, and
        return the channel object."""
        if not isinstance(name_or_chan, Channel):
            name_or_chan = Channel(name_or_chan)
        self.channels.add(name_or_chan)
        return name_or_chan

    def add_user(self, nick_or_user):
        """Add a user to the network, create if necessary, and
        return the user object."""
        if not isinstance(nick_or_user, User):
            nick_or_user = User(nick_or_user)
        self.users.add(nick_or_user)
        return nick_or_user

    def join(self, channel: Channel, user: User):
        """Join channel and user object.
        This means, that the user <user> is on channel <channel>."""
        self.joins.add((channel, user))

    def detach(self, channel: Channel, user: User):
        """Detach channel and user object from each other.
        This means, the user <user> left the channel <channel>."""
        tmp = (channel, user)
        if tmp in self.joins:
            self.joins.remove(tmp)
