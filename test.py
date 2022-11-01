from datetime import timedelta
import unittest
from src.srt_file import SRTParser, Caption


class SRTTest(unittest.TestCase):
    def test_add_caption_at_the_end(self):
        srt_file = SRTParser("src/srt_examples/test.srt")

        srt_file.add_caption_at_the_end("hello", timedelta(seconds=1))

        self.assertTrue(str(srt_file).endswith("hello"), str(srt_file))

    def test_parse_str(self):

        text = """1 
00:38:47,301 --> 00:38:48,441 
I'm going to count down !

2 
00:38:54,321 --> 00:38:55,241 
In five..."""

    



if __name__ == "__main__":
    unittest.main()