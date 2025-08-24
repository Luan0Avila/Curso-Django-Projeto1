from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_without_recipes(self):
        self.make_recipe_in_batch(qtd=20)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('No recipes found here 🥲', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        
        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        #Usuário abre a pagina
        self.browser.get(self.live_server_url)

        #Ve um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for a recipe"]')

        #clica neste input e digita o termo de busca
        #"Recipe title 1" para encontrar a receita com este titulo
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        #o usuario ve o que estava procurando na pagina
        self.assertIn(title_needed, self.browser.find_element(By.CLASS_NAME, 'main-content-list').text)
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()
        
        #Usuário abre a pagina
        self.browser.get(self.live_server_url)

        #ve que tem uma paginação e clica na pagina 2
        page2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2"]')
        page2.click()

        #ve que tem mias 2 receitas na pagina 2
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)

        self.sleep(10)

