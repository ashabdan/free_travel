import os
import random
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from django.db import models
from user.models import CustomUser


def upload_image_path(instance, filename):
    print(instance, filename)
    new_name = random.randint(1000000, 9999999)
    name, ext = Post.get_filename_ext(filename)
    final_name = f'{new_name}{ext}'
    return f'posts/images/{final_name}'


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class DataABC(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(DataABC):
    title = models.CharField(max_length=100)
    description = RichTextField()
    owner = models.ForeignKey(CustomUser, related_name='posts',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='posts')
    preview = models.ImageField(upload_to=upload_image_path)
    quantity = models.PositiveSmallIntegerField(default=1)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.owner} --> {self.title}'

    @staticmethod
    def get_filename_ext(filepath):
        base_name = os.path.basename(filepath)
        name, ext = os.path.splitext(base_name)
        return name, ext


class Comment(DataABC):
    owner = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f'{self.owner} -> {self.post} -> {self.created_at}'


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)