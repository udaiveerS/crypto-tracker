from twitter_tracker.models.twitter_account import TwitterAccount
from django.core.exceptions import ObjectDoesNotExist
import logging
from datetime import datetime
from django.utils import timezone
from twitter_tracker.utils.utils import today_date
from django.db.models import Q

# Get an instance of a logger
logger = logging.getLogger("root")


class TwitterAccountRepository:

    @staticmethod
    def get_one_account_for_follows_processing():
        return TwitterAccount.objects \
                   .filter(Q(follows_processed_time__lte=today_date()) | Q(follows_processed_time__isnull=True)) \
                   .filter(track_followers=True)[:1]

    @staticmethod
    def save_or_update_twitter_accounts(user_accounts, track_followers=False):
        # For each profile add account metadata

        for user_account in user_accounts:
            new_account = TwitterAccount(
                twitter_id=user_account['id'],
                username=user_account['username'],
                name=user_account['name'],
                created_at=timezone.now(),
                update_time=timezone.now(),
                track_followers=track_followers,
                profile_image_url=user_account['profile_image_url'] if 'profile_image_url' in user_account else None,
                description=user_account["description"] if'description' in user_account else None,
                profile_created_at=timezone.make_aware(datetime.strptime(user_account["created_at"], "%Y-%m-%dT%H:%M"
                                                                                                     ":%S.%fZ")) if 'created_at' in user_account else None,
                followers_count=user_account["public_metrics"]["followers_count"] if'public_metrics' in user_account else None,
                following_count=user_account["public_metrics"]["following_count"] if'public_metrics' in user_account else None,
                tweet_count=user_account["public_metrics"]["tweet_count"] if'public_metrics' in user_account else None,
                listed_count=user_account["public_metrics"]["listed_count"] if'public_metrics' in user_account else None,
            )

            try:
                person = TwitterAccount.objects.get(twitter_id=user_account['id'])
                person.update_time = timezone.now()
                person.description = user_account["description"] if'description' in user_account else None
                person.followers_count = user_account["public_metrics"]["followers_count"] if'public_metrics' in user_account else None
                person.following_count = user_account["public_metrics"]["following_count"] if'public_metrics' in user_account else None
                person.tweet_count = user_account["public_metrics"]["tweet_count"] if'public_metrics' in user_account else None
                person.listed_count = user_account["public_metrics"]["listed_count"] if'public_metrics' in user_account else None
                person.track_followers = person.track_followers | track_followers # if tracking is enabled don't disable it
                logger.debug(user_account['username'] + ' info updated')

                person.save()
            except ObjectDoesNotExist:
                new_account.save()
                logger.debug(user_account['username'] + ' created')
