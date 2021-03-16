import unittest
import sys
sys.path.insert(
    1, '/Users/joao reis/Documents/projects/Discord/Bots/DiscordBottom/DiscordBottom/src/')
import message_parser


class StringParserTest(unittest.TestCase):

    def test_replace_prefix(self):
        prefix = 'abcd'
        s1 = 'abcdaabcd'
        s2 = 'aabcd'
        s3 = 'abc'
        s4 = 'abdc'
        
        self.assertEqual(message_parser.remove_prefix(prefix, s1), 'aabcd')
        self.assertEqual(message_parser.remove_prefix(prefix, s2), s2)
        self.assertEqual(message_parser.remove_prefix(prefix, s3), s3)
        self.assertEqual(message_parser.remove_prefix(prefix, s4), s4)
    
    def test_get_command(self):
        prefix = 'abc'
        str1 = 'abccommand'
        expected = 'command'
        self.assertEqual(message_parser.get_command(prefix, str1), expected)

        str1 = 'abommand'    
        self.assertEqual(message_parser.get_command(prefix, str1), str1)
        str1 = 'abccommand  arg'
        expected = 'command'
        self.assertEqual(message_parser.get_command(prefix, str1), expected)

if __name__ == '__main__':
    unittest.main()