from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from tag.models import Tag
from ..serializers import TagSerializer

@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    serializer = RecipeSerializer(instance=recipe, many=False, context={'request': request})
    return Response(serializer.data)

    #Outra forma de fazer

    #recipe = Recipe.objects.get_published().filter(pk=pk).first()
    #if recipe:
        #serializer = RecipeSerializer(instance=recipe, many=False)
        #return Response(serializer.data)
    #else:
        #return Response({
            #"detail" : "Eita"
        #}, status=status.HTTP_404_NOT_FOUND)

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False, context={'request': request})
    return Response(serializer.data)