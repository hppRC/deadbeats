import requests
from datetime import datetime
import os, sys
import subprocess


class _InnerClass:
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


    def reset_thread(self):
        self.thread_ts = ""


    def _post(self, text, info = {}, url="https://slack.com/api/chat.postMessage"):
        time = str(datetime.now())
        info = "\n".join(f'{k}:\t{v}' for k, v in info.items())

        try:
            return requests.post(url,
                headers = self.headers,
                json = {
                    "channel": self.channel_id,
                    "text": f"{text}\ntime:\t{time}\n{info}",
                    "thread_ts": self.thread_ts,
                }
            )
        except requests.exceptions.RequestException as e:
            print(f"post error!\n{e}", file=sys.stderr)
            return None


    def start_thread(self, text="start :tada:", params={}, **kwargs):
        response = self._post(text = text, info = {**params, **kwargs})
        self.thread_ts = response.json()["ts"]
        return response


    def ping(self, text="ping!", params={}, **kwargs):
        return self._post(text = text, info = {**params, **kwargs})


    def wrap(self, function, start_message="start! :sparkles:", end_message="end! :confetti_ball:"):
        def inner(*args, **kargs):
            self._post(start_message)
            try:
                return function(*args, **kargs)
            except Exception as e:
                self._post(e)
                raise e
            self._post(end_messageend_message)
        return inner


DEADBEATS = _InnerClass()


def main():
    # print("DEADBEATS")
    # print("☠️ see https://youtu.be/6ydgEipkUEU")
    start = datetime.now()
    DEADBEATS.start_thread()
    try:
        subprocess.run(sys.argv[1:], shell=True)
    except Exception as e:
        DEADBEATS.ping(e)
        raise e
    end = datetime.now()
    DEADBEATS.ping(text=f"end :sparkles:\nduration:\t{end - start}")


if __name__ == "__main__":
    main()