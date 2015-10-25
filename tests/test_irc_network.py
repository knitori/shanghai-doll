
from unittest import TestCase
from shanghai.irc import state


class TestIrcParse(TestCase):

    def test_network(self):
        net = state.Network('Testnick')
        chans = [
            '#TestChannel[1]',
            '#TestChannel[2]',
            '#TestChannel[3]',
        ]
        for chan in chans:
            net.add_channel(chan)

        self.assertEqual(len(net.channels), 3)

        chan = net.find_channel('#TestChannel[1]')
        self.assertTrue(chan in net.channels)
