from django.http.response import Http404
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.contrib import messages
import os
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value
from django.db.models.aggregates import Count
from django.db.models.functions import Concat
from tag.models import Tag

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True,)
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({ 'recipes': page_obj, 'pagination_range': pagination_range })
        return ctx
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()
        
        return JsonResponse(
            list(recipes_list),
            safe=False
            )

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id= self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()
        return qs
    
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()
        
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
        Q(title__icontains = search_term) |
        Q(description__icontains = search_term)
        ),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'additional_url_query': f'&q={search_term}'
        })

        return ctx

class RecipeDetail(DetailView):

    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data( *args, **kwargs)

        ctx.update({ 'is_detail_page': True })
        return ctx
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        
        return qs
    

class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
    
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
        'page_title': f'{page_title} |',
        })

        return ctx


def theory(request, *args, **kwargs):
    #recipes = Recipe.objects.all() # retorna uma QuerySet com todas as receitas
    #recipes = recipes.filter(title__icontains='bolo') #Mesmo que o eu faça um filter, o django só vai buscar no banco de dados quando eu chamar a variável

    # print(recipes[0].title) # o django busca a receita no banco de dados apenas quando ela é chamada
    
    # print(recipes) # O django limita a busca para que seja puxado apenas aquilo que é solicitado

    # list(recipes) # assim a consulta é feita no banco de dados. Assim tambem não vai haver o limite de consulta

    #try:
    #    recipes = Recipe.objects.get(pk=10000) # Busca uma recipe pela pk dela e retorna um objeto
    #except ObjectDoesNotExist: # secaso não exista, ele trata o erro
    #       recipes = None

    #recipes = Recipe.objects.filter(
        #id= F('author__id'), # pode se usar o F para referenciar outros campos para busca
        
        #Q(Q(title__icontains ="pão",
        #id__gt=2, #todas esses requisitos são como a instrução AND do banco de dados
        #is_published=True) | # o | representa a instrução OR
        #Q(
        #    id__lt = 1000
        #))       )
    #).order_by('-id') #,'title')#[:1] #order_by pode ser decrescente ou crecnete respectivamente

    # recipes = Recipe.objects.only('id', 'title')[:10] # values retorna uma lista de dicionários com os campos solicitados

    #recipes = Recipe.objects.only('id', 'title')[:10] # only limita os campos que serão buscados no banco de dados
    #recipes = Recipe.objects.defer('is_published') # defer limita os campos que não serão buscados no banco de dados
    
    recipes = Recipe.objects.get_published()[0:10] #.filter(title__icontains='teste') #se usarmos recipes ao inves do objeto Recipe o django vai retornar a quantidade que recipes tem, por exemplo no caso de 'teste'
    number_of_recipes = recipes.aggregate(number=Count('id')) # O count mostra a qunatidade de receitas

    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
        }
    return render(request, 'recipes/pages/theory.html', context = context)