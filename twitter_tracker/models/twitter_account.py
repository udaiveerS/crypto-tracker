from django.db import models
from twitter_tracker.enums.constant import PROFILE_PARSED


class TwitterAccount(models.Model):
    twitter_id = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255)
    name = models.TextField()

    created_at = models.DateTimeField()
    update_time = models.DateTimeField()
    follows_processed_time = models.DateTimeField(null=True)
    track_followers = models.BooleanField(default=False)

    #Public attributrs
    profile_image_url = models.TextField(null=True)
    url = models.TextField(null=True)
    description = models.TextField(null=True)
    discord = models.TextField(null=True)
    profile_created_at = models.DateTimeField(null=True)

    #public metrics
    followers_count = models.IntegerField(null=True)
    following_count = models.IntegerField(null=True)
    tweet_count = models.IntegerField(null=True)
    listed_count = models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['twitter_id']),
            models.Index(fields=['username'])
        ]



