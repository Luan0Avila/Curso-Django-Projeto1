from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorsLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True)

        self.assertIn('Invalid logou request', response.content.decode('utf-8'))