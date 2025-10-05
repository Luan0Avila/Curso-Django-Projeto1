from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
#from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class RecipeManagager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
        author_full_name= Concat(F('author__first_name'), Value(' '), 
        F('author__last_name'), Value(' ('), 
        F('author__username'), Value(')')
        )
        ).order_by('-id')

class Recipe(models.Model):
    objects = RecipeManagager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation_time'))
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, default='') #GenericRelation(Tag, related_query_name='recipes')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
    
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOTS, image.name)
    image_pillow = Image.open(image_full_path)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_form_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_form_db:
            if recipe_form_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title.'
                )
        if error_messages:
            raise ValidationError(error_messages)
        

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
