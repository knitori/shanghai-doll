
from unittest import TestCase
from shanghai.irc import parse


class TestIrcParse(TestCase):

    def test_rfc(self):
        # https://tools.ietf.org/html/rfc2812#section-2.2
        a = parse.rfc_lower('ABCabc{}|^0123')
        self.assertEqual(a, 'abcabc[]\\~0123')

        a = parse.rfc_lower('ABCabc[]\\~0123')
        self.assertEqual(a, 'abcabc[]\\~0123')

        a = parse.rfc_upper('ABCabc{}|^0123')
        self.assertEqual(a, 'ABCABC{}|^0123')

        a = parse.rfc_upper('ABCabc[]\\~0123')
        self.assertEqual(a, 'ABCABC{}|^0123')

        self.assertTrue(parse.is_channel('#foobar'))
        self.assertTrue(parse.is_channel('&foobar'))
        self.assertTrue(parse.is_channel('+foobar'))
        self.assertTrue(parse.is_channel('!foobar'))
        self.assertFalse(parse.is_channel('#'))
        self.assertFalse(parse.is_channel('&'))
        self.assertFalse(parse.is_channel('+'))
        self.assertFalse(parse.is_channel('!'))
        self.assertFalse(parse.is_channel('foobar'))
        self.assertFalse(parse.is_channel('#foo\0bar'))
        self.assertFalse(parse.is_channel('#foo\nbar'))
        self.assertFalse(parse.is_channel('#foo\rbar'))
        self.assertFalse(parse.is_channel('#foo\abar'))
        self.assertFalse(parse.is_channel('#foo bar'))
        self.assertFalse(parse.is_channel('#foo,bar'))
        self.assertFalse(parse.is_channel('#foo:bar'))
