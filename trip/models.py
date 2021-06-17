from django.db import models
from user.models import CustomUser
from post.models import Post


class Trip(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trip')


class TripDetail(models.Model):
    cart = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tripdetail')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tripdetail')

    def __str__(self):
        return self.post.title
