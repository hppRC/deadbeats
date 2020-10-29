from deadbeats import __version__, DEADBEATS
import unittest


class TestCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_version(self):
        assert __version__ == '0.1.0'

    def test_channel_id(self):
        assert DEADBEATS.channel_id == "deadbeats"

    def test_thread_ts(self):
        assert DEADBEATS.thread_ts == ""

    # def test_set_channel_id(self):
    #     DEADBEATS.set_channel_id("test")
    #     assert DEADBEATS.channel_id == "test"

    def test_ping(self):
        assert DEADBEATS.ping().status_code == 200

if __name__ == '__main__':
    unittest.main()