from django.core.management.base import BaseCommand
from twitter_tracker.manager.manage_follows import ManageFollows
from twitter_tracker.repository.twitter_account_repository import TwitterAccountRepository
import logging
from twitter_tracker.models.twitter_account import TwitterAccount
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'parsed twitter profiles and followers'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        account_results = TwitterAccountRepository.get_one_account_for_follows_processing()

        if len(account_results) > 0:
            account: TwitterAccount = account_results[0]
            logger.info("queried account")
            logger.info("queried account " + account.username + "|" + account.twitter_id)
        else:
            logger.info("No account to process at the moment")
            return

        ManageFollows.process_follows(account)
        account.follows_processed_time = timezone.now()
        account.save()

        logger.info(f'account processing for {account.username} complete')
