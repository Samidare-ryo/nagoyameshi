# nagoyameshi/base/models/tag_models.py

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField("タグ名", max_length=50, unique=True)
    slug = models.SlugField("スラッグ", max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
