import shortuuid

from django.contrib.auth.models import User
from django.db import models
from stream_django.activity import Activity

# Create your models here.
class StreamGroup(models.Model):
    uuid = models.CharField("UUID", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    icon = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, through="Membership")

    # lets accessor for getstream get 'actor' for feed
    @property
    def activity_actor_attr(self):
        return self.author
    
    def __str__(self):
        return self.name

class Membership(models.Model):
    PENDING = 1
    ACCEPTED = 2
    BLOCKED = 3
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (BLOCKED, 'Blocked'),
    ]
    FOLLOWER = 1
    MEMBER = 2
    ADMIN = 3
    CREATOR = 4
    POSITION_CHOICES = [
        (FOLLOWER, 'Follower'),
        (MEMBER, 'Member'),
        (ADMIN, 'Admin'),
        (CREATOR, 'Creator'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StreamGroup, on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default=PENDING,
        max_length=20,
    )
    position = models.CharField(
        choices=POSITION_CHOICES,
        default=FOLLOWER,
        max_length=20,
    )

class StreamPost(models.Model, Activity):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StreamGroup, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    @property
    def activity_actor_attr(self):
        return self.author

class StreamComment(models.Model, Activity):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(StreamPost, on_delete=models.CASCADE)    
    content = models.TextField()

    @property
    def activity_actor_attr(self):
        return self.author