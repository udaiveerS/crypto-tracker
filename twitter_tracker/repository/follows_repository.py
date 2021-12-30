from typing import List

import twitter_tracker.models
from twitter_tracker.models.twitter_account import TwitterAccount
from django.core.exceptions import ObjectDoesNotExist
import logging
from datetime import datetime
from django.utils import timezone
from twitter_tracker.utils.utils import today_date
from django.db.models import Q
from twitter_tracker.models import Follows

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FollowsRepository:

    @staticmethod
    def get_one_account_for_follows_processing():
        return TwitterAccount.objects \
                   .filter(Q(follows_processed_time__lte=today_date()) | Q(follows_processed_time__isnull=True)) \
                   .filter(track_followers=True)[:1]

    @staticmethod
    def add_new_follows(user_accounts_followed, tracked_user: TwitterAccount):
        # use composite key USR_FOLLOWED_ID-TRACKED_USR_ID to check where in agaist follows table
        composite_ids = []
        for user in user_accounts_followed:
            composite_ids.append(user["id"] + "-" + tracked_user.twitter_id)

        logger.info("adding new followers for {account_name}|{account_id}".format(account_id=tracked_user.twitter_id, account_name=tracked_user.username))

        tracked_users_set: List[Follows] = Follows.objects.filter(user_id_follows_id__in=composite_ids)
        follows_id_set = [user.user_id_follows_id for user in tracked_users_set]

        logger.info("{accounts_tracked} accounts already beingg tracked for {account_name}|{account_id}".format(
            account_id=tracked_user.twitter_id,
            account_name=tracked_user.username,
            accounts_tracked=len(tracked_users_set)))

        for user in user_accounts_followed:
            composite_user_id = user["id"] + "-" + tracked_user.twitter_id
            if composite_user_id not in follows_id_set:
                logger.info("Tracking new user https://twitter.com/" + user["username"])
                new_follow = Follows(
                    user_id_follows_id=user["id"] + "-" + tracked_user.twitter_id,
                    user_id=user["id"],
                    follows=tracked_user.twitter_id,
                    follows_time=timezone.now()
                )
                new_follow.save()
