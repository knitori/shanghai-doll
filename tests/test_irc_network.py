
from unittest import TestCase
from shanghai.irc import state


class TestIrcParse(TestCase):

    def test_network(self):
        net = state.Network('Testnick')

    def test_users(self):
        net = state.Network('Testnick')
        user1 = state.User('testuser[1]')
        user2 = state.User('TestUser{1}')
        self.assertTrue(user1 == user2)

        tmp_user1 = net.add_user(user1)
        tmp_user2 = net.add_user('testUser{1]')
        self.assertTrue((tmp_user1 is tmp_user2) and (tmp_user2 is user1))

    def test_channels(self):
        net = state.Network('Testnick')
        self.assertTrue(state.Channel('#testchannel{1}') ==
                        state.Channel('#TestChannel[1]'))

        net = state.Network('Testnick')
        chan1 = state.Channel('#testchannel[1]')
        chan2 = state.Channel('#TestChannel{1}')
        self.assertTrue(chan1 == chan2)

        tmp_chan1 = net.add_channel(chan1)
        tmp_chan2 = net.add_channel('#testChannel{1]')
        self.assertTrue((tmp_chan1 is tmp_chan2) and (tmp_chan2 is chan1))

    def test_joins(self):
        net = state.Network('Testnick')

        chan1 = net.add_channel('#channel1')
        chan2 = net.add_channel('#channel2')
        chan3 = net.add_channel('#channel[3]')

        user1 = net.add_user('Nick1')
        user2 = net.add_user('Nick2')
        user3 = net.add_user('Nick3')

        net.join(chan1, user1)
        net.join(chan1, user2)
        net.join(chan1, user3)

        net.join(chan2, user3)
        net.join(chan2, user1)

        net.join(chan3, user2)

        user_in_channel1 = list(net.joined_users('#channel1'))
        user_in_channel2 = list(net.joined_users(chan2))
        user_in_channel3 = list(net.joined_users('#Channel{3}'))

        self.assertEqual(len(user_in_channel1), 3)
        self.assertEqual(len(user_in_channel2), 2)
        self.assertEqual(len(user_in_channel3), 1)

        self.assertEqual({user1, user2, user3}, set(user_in_channel1))
        self.assertEqual({user1, user3}, set(user_in_channel2))
        self.assertEqual({user2}, set(user_in_channel3))
