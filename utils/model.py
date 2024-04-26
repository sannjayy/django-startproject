from django.db import models
from django.utils.text import slugify
from utils.functions import random_string_generator


 
def unique_slug_generator(instance, new_slug = None):
    slug =  slugify(new_slug) if new_slug is not None else slugify(instance.title)

    Class = instance.__class__
    max_length = Class._meta.get_field('slug').max_length
    slug = slug[:max_length]
    if qs_exists := Class.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(
            slug = slug[:max_length-20], randstr = random_string_generator(size = 17))

        return unique_slug_generator(instance, new_slug = new_slug)
    return slug



# SingleTon Class
class Singleton(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj