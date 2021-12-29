from typing import List

import requests
import os
import json


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

class TrackUsernames:

    @staticmethod
    def auth():
        return os.environ.get("BEARER_TOKEN")

    @staticmethod
    def create_url(usernames: List[str]):
        # Specify the usernames that you want to lookup below
        # You can enter up to 100 comma-separated values.
        usernames = "usernames=" + ",".join(usernames)
        user_fields = "user.fields=profile_image_url,public_metrics,created_at,description"
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        return url

    @staticmethod
    def get_params():
        return {"user.fields": "created_at"}

    @staticmethod
    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {TrackUsernames.auth()}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r

    @staticmethod
    def connect_to_endpoint(url):
        response = requests.request("GET", url, auth=TrackUsernames.bearer_oauth)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    @staticmethod
    def track_follows(users):
        url = TrackUsernames.create_url(users)
        json_response = TrackUsernames.connect_to_endpoint(url)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        return json_response


if __name__ == '__main__':
    TrackUsernames.track_follows(["bigdsenpai", "zhusu", "0xShual"])
