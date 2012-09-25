from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

class HomePageTests(TestCase):
    
    fixtures = ['users']
    def setUp(self):
        self.client = Client()

    def test1_home_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test2_correct_login(self):
        data = {
                'username': 'test_normal_user',
                'password': 'password'}
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 302)
