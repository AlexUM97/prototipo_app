from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    text = models.TextField()
    img = models.ImageField(upload_to='imagenes/',blank=True,null=True)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title