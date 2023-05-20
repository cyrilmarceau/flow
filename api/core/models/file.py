from django.db import models
from versatileimagefield.fields import VersatileImageField


class File(models.Model):
    TYPE = [
        ("avatar", "avatar"),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE, null=False, blank=False)
    file = VersatileImageField(
        'File',
        upload_to='file',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
