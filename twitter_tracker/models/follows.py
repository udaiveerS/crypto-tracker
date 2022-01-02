from django.db import models


class Follows(models.Model):
    user_id_follows_id = models.CharField(primary_key=True, max_length=255)
    followed_user_id = models.CharField(max_length=255)
    follower_id = models.CharField(max_length=255)
    follows_time = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['user_id_follows_id'])
        ]


