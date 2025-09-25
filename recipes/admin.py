from django.contrib import admin
from .models import Category, Recipe
<<<<<<< HEAD
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag
=======
from tag.models import Tag
from django.contrib.contenttypes.admin import GenericStackedInline
>>>>>>> da87fd53cbe7399bf6c8dee2350b5bbe91bf6061

class CategoryAdmin(admin.ModelAdmin):
    ...

class TagInline(GenericStackedInline):
<<<<<<< HEAD
    model = Tag
=======
    model  = Tag
>>>>>>> da87fd53cbe7399bf6c8dee2350b5bbe91bf6061
    fields = 'name',
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at','is_published', 'author') 
    list_display_links = ('title','created_at', 'id')
    search_fields = ('id','title', 'description', 'slug', 'preparation_steps')
    list_filter = ('category','author','is_published','preparation_steps_is_html')
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('id',)
    prepopulated_fields = {
        "slug": ('title',)
    }

<<<<<<< HEAD
    inlines = [TagInline,]
=======
    inlines = [
        TagInline,
    ]
>>>>>>> da87fd53cbe7399bf6c8dee2350b5bbe91bf6061

admin.site.register(Category, CategoryAdmin)