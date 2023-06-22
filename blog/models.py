from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from client.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='blog_title', unique=True)
    content = models.TextField(verbose_name='blog_content')
    image = models.ImageField(upload_to='blog_image/', verbose_name='blog_image', **NULLABLE)
    views = models.IntegerField(verbose_name='blog_views', default=0, **NULLABLE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='blog_created')
    slug = models.SlugField(verbose_name='blog_slug', max_length=255, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(unidecode(self.title))
            super().save(*args, **kwargs)