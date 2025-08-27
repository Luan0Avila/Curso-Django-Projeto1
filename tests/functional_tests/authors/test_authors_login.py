from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import pytest

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='my_user', password='pass')

        #usuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #usuario ve um formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        #usuario digita seu usuario e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        #usuario envia o formulario
        form.submit()


        #usuario ve a menssagem de login com sucesso
        self.assertIn(f'Your are logged in with {user.username}', self.browser.find_element(By.TAG_NAME, 'body').text)
        #end test
        