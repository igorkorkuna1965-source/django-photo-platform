from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(
        Album,
        related_name="photos",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    image_full = models.ImageField(upload_to="photos/full/")
    image_thumb = models.ImageField(upload_to="photos/thumb/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.album.title} - {self.title}"

class AlbumLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="album_likes")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'album')

class PhotoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo_likes")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)