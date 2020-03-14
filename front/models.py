from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserExtension(models.Model):
    # 这里增加想要的字段
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    head_img = models.ImageField(upload_to='header_img', null=True)
    # 结束


class Article(models.Model):
    title = models.CharField(unique=True, max_length=100, null=False)
    auth = models.ForeignKey(UserExtension, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    end_set_time = models.DateTimeField(auto_now=True)
    view_times = models.IntegerField(default=0)
    tags = models.CharField(null=False, max_length=50)
    is_active = models.BooleanField(default=False)


class Image(models.Model):
    img = models.ImageField(upload_to='upload', null=False)


class Comment(models.Model):
    comment_user = models.ForeignKey(UserExtension, on_delete=models.CASCADE, null=False)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()


class Collect(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    collect_user = models.ForeignKey(UserExtension, on_delete=models.CASCADE, null=False)


class Likes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    likes_user = models.ForeignKey(UserExtension, on_delete=models.CASCADE, null=False, )


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()
