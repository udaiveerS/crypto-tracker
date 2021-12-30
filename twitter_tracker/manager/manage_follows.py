import requests
import os
import logging
import time
from twitter_tracker.models import TwitterAccount
from twitter_tracker.repository.follows_repository import FollowsRepository
from twitter_tracker.repository.twitter_account_repository import TwitterAccountRepository

logger = logging.getLogger(__name__)


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

class ManageFollows:
    MAX_RESULTS = 1000

    @staticmethod
    def auth():
        return os.environ.get("BEARER_TOKEN")

    # 28064228
    # 1350996311777161219
    @staticmethod
    def create_url(user_id, pagination_token=None):
        user_fields = "user.fields=profile_image_url,public_metrics,created_at,description"
        if pagination_token:
            return "https://api.twitter.com/2/users/{user_id}/following?{user_fields}" \
                   "&max_results={max_results}&pagination_token={pagination_token}". \
                format(user_id=user_id, max_results=ManageFollows.MAX_RESULTS, pagination_token=pagination_token,
                       user_fields=user_fields)

        return "https://api.twitter.com/2/users/{user_id}/following?max_results={max_results}". \
            format(user_id=user_id, max_results=ManageFollows.MAX_RESULTS, user_fields=user_fields)

    @staticmethod
    def create_url_by_user_id():
        # Replace with user ID below
        user_id = 2244994945
        return "https://api.twitter.com/2/users/by/username/{}/following".format("uda4000")

    @staticmethod
    def get_params():
        return {}

    @staticmethod
    def create_headers(bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    @staticmethod
    def connect_to_endpoint(url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    @staticmethod
    def process_follows(user_account: TwitterAccount):
        # process all of the followers and add them to a list
        bearer_token = ManageFollows.auth()
        headers = ManageFollows.create_headers(bearer_token)
        params = ManageFollows.get_params()

        url = ManageFollows.create_url(user_id=user_account.twitter_id)
        json_response = ManageFollows.connect_to_endpoint(url, headers, params)
        if "meta" in json_response and "next_token" in json_response["meta"]:
            next_token = json_response["meta"]["next_token"]
        else:
            next_token = None

        user_accounts = json_response['data']
        FollowsRepository.add_new_follows(user_accounts_followed=user_accounts, tracked_user=user_account)
        TwitterAccountRepository.save_or_update_twitter_accounts(user_accounts=user_accounts)
        logger.info(json_response["meta"])

        # parse these users
        count = 1
        while next_token:
            url = ManageFollows.create_url(user_id=user_account.twitter_id, pagination_token=next_token)
            json_response = ManageFollows.connect_to_endpoint(url, headers, params)
            logger.info(json_response["meta"])

            if 'data' in json_response:
                user_accounts = json_response['data']
                FollowsRepository.add_new_follows(user_accounts_followed=user_accounts, tracked_user=user_account)
                TwitterAccountRepository.save_or_update_twitter_accounts(user_accounts=user_accounts)

            if "meta" in json_response and "next_token" in json_response["meta"]:
                next_token = json_response["meta"]["next_token"]
            else:
                next_token = None

            count += 1
            time.sleep(5)

        logger.info("Parsing followers finished {} pages parsed".format(count))
