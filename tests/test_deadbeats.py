from deadbeats import DEADBEATS
import unittest
import pytest
import time
import requests

# load environment variables by pytest-dotenv
class TestCore(unittest.TestCase):
    @pytest.mark.run(order=1)
    def test_channel_id(self):
        assert DEADBEATS.channel_id == "deadbeats"
        DEADBEATS.set_channel_id("test")
        assert DEADBEATS.channel_id == "test"
        DEADBEATS.set_channel_id("deadbeats")
        assert DEADBEATS.channel_id == "deadbeats"

    @pytest.mark.run(order=1)
    def test_thread_ts(self):
        assert DEADBEATS.thread_ts == ""

    @pytest.mark.run(order=2)
    def test_start_thread(self):
        assert DEADBEATS.start_thread().status_code == 200

    def test_ping(self):
        assert DEADBEATS.ping().status_code == 200

    def test_ping_extra(self):
        params = {"test1": 1, "test2": 2, "test3": 3.0}
        assert DEADBEATS.ping(params=params, dead="dead", beats="beats").status_code == 200

    @pytest.mark.run(order=-1)
    def test_reset_thread(self):
        DEADBEATS.reset_thread()
        assert DEADBEATS.thread_ts == ""

    def test_wrapper(self):
        @DEADBEATS.wrap
        def test_inner():
            time.sleep(3)
            return "test"

        assert test_inner() == "test"

    def test_wrapper_error(self):
        @DEADBEATS.wrap
        def test_inner():
            raise ValueError("test error")

        with pytest.raises(Exception):
            test_inner()


    def test_post_error(self):
        assert DEADBEATS._post('test', info={}, url="invalid url") is None

if __name__ == '__main__':
    unittest.main()