import unittest
from src.srt_file import SrtFile


class SRTTest(unittest.TestCase):
    def test_add_caption_at_the_end(self):
        srt_file = SrtFile("src/srt_examples/test.srt")

        srt_file.add_caption_at_the_end("hello", "00:19:49,300")

        self.assertTrue(str(srt_file).endswith("hello"), str(srt_file))

        



if __name__ == "__main__":
    unittest.main()