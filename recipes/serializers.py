from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag
from .models import Recipe

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name','slug']
    #id = serializers.IntegerField()
    #name = serializers.CharField(max_length=255)
    #slug = serializers.SlugField()

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id','title','description','category','author','tags','public','preparation',
                'tag_objects','tag_links']

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='get_preparation',read_only=True)  
    category = serializers.StringRelatedField()
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(many=True, source='tags', read_only=True, view_name='recipes:recipes_api_v2_tag')



    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'