import requests
from datetime import datetime
import os, sys


__version__ = '0.1.0'


class _DEADBEATS:
    def __init__(self):
        self.access_token = os.getenv("SLACK_ACCESS_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.headers = {
            "content-type": "application/json",
            'Authorization': f'Bearer {self.access_token}'
        }

        self.thread_ts = ""


    def set_access_token(self, access_token):
        self.access_token = access_token


    def set_channel_id(self, channel_id):
        self.channel_id = channel_id


    def start_thread(self, text="", data={}, **kwargs):
        time = str(datetime.now().isoformat(timespec='seconds'))
        info = "\n".join(f'{k}:\t{v}' for k, v in {**data, **kwargs}.items())
        default_message = f"start :tada:"
        text = (text or default_message) + f"\nstart time:{time}\n{info}"

        response = requests.post("https://slack.com/api/chat.postMessage",
            headers = self.headers,
            json = {
                "channel": self.channel_id,
                "text": text,
            }
        )
        self.thread_ts = response.json()["ts"]


    def _post(self, text, info = {}):
        time = str(datetime.now())
        info = "\n".join(f'{k}:\t{v}' for k, v in info.items())

        return requests.post("https://slack.com/api/chat.postMessage",
            headers = self.headers,
            json = {
                "channel": self.channel_id,
                "text": f"{text}\ntime:{time}\n{info}",
                "thread_ts": self.thread_ts,
            }
        )


    def ping(self, text="", params={}, **kwargs):
        default_message = f"ping :heart:"
        text = text or default_message
        return self._post(text = text, info = {**params, **kwargs})


    def wrap(self, function):
        def inner(*args, **kargs):
            self.start("start! :flexed_biceps:")
            try:
                return function(*args, **kargs)
            except Exception as e:
                self.error(e)
                sys.exit()
            self._post("end! :confetti_ball:")
        return inner


DEADBEATS = _DEADBEATS()


def main():
    print("test!")


if __name__ == "__main__":
    main()