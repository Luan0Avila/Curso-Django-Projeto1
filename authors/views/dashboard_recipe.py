from django.views import View
from recipes.models import Recipe
from django.http import Http404
from ..forms.recipe_form import AuthorRecipeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

class DashboardRecipe(View):
    def get(self, request, id):
        self.request
        recipe = Recipe.objects.filter(is_published=False, author=request.user, pk=id,).first()
        if not recipe:
            raise Http404
        
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
    )

        if form.is_valid():
            # agora o form é valido e eu posso tentar salvar
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            
            recipe.save() 

            messages.success(request, 'Your recipe was saved with sucess!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(request, 'authors/pages/dashboard_recipe.html',
        context={'recipe': recipe,
                'form': form})
