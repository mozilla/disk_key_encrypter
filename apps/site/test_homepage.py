from django.conf.urls import url, include
from django.urls import reverse
from django.test import TestCase, Client, modify_settings
from django.test.utils import override_settings
from django.conf import settings
from mock import patch
from apps.site.models import EncryptedDisk
import os
import mock



class HomePageTest(TestCase):

    fixtures = ['users']

    def setUp(self):
        self.client = Client()

    def test1_home_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
