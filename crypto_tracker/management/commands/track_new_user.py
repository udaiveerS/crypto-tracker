from django.core.management.base import BaseCommand
from twitter_tracker.manager.manager_usernames import TrackUsernames
import logging
from twitter_tracker.repository.twitter_account_repository import TwitterAccountRepository

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'parsed twitter profiles and followers'

    def add_arguments(self, parser):
        parser.add_argument('--username', action='append', type=str)

    def handle(self, *args, **options):
        # Get a user whoes followers we are tracking that was tracked before todays date

        if options['username']:
            user_accounts_json = TrackUsernames.track_follows(options['username'])
            user_accounts = user_accounts_json['data']
            TwitterAccountRepository.save_or_update_twitter_accounts(user_accounts, track_followers=True)
        else:
            logger.info("Provide a username to track with --username argument")

