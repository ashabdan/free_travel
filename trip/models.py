from django.db import models
from user.models import CustomUser
from post.models import Post


class Trip(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trip')
    tripname = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.tripname


class TripDetail(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tripdetail')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tripdetail')

    def __str__(self):
        return f'{self.trip} -> {self.post.title}'
