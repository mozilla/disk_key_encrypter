from django.conf.urls import url, include
from django.urls import reverse
from django.test import TestCase, Client, modify_settings
from django.test.utils import override_settings
from django.conf import settings
from mock import patch
from apps.site.models import EncryptedDisk
import os
import mock

namespaces_to_test = {
    'attach': {
        'id': 1
    },
    'detail': {
        'id_value': '1'
    },
    'desktop_admin': {

    },
    'desktop_admin_upload': {

    },
}


class HomePageTest(TestCase):

    fixtures = ['users']

    def setUp(self):
        self.client = Client()

    def test1_home_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)


class DownloadAttachmentTest(TestCase):

    fixtures = [
        'users',
        'encrypteddisk',
    ]

    def setUp(self):
        self.client = Client()


    def test1_download_works_correctly(self):
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse("attach", kwargs={"id": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'-----BEGIN PGP MESSAGE-----Version: GnuPG v2.0.14 (GNU/Linux)File Data Here-----END PGP MESSAGE-----')


class LoginTest(TestCase):

    fixtures = ['users']

    def setUp(self):
        self.client = Client()


    def test1_correct_login(self):
        data = {
                'username': 'test_normal_user',
                'password': 'password'}
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/upload/')

    def test2_incorrect_login(self):
        data = {
                'username': 'test_normal_user',
                'password': 'incorrectpassword'}
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Invalid Username/Password')

class URLsTestALLOW_ADMIN_TRUE(TestCase):

    fixtures = [
        'users',
        'encrypteddisk',
    ]

    def setUp(self):
        self.client = Client()

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test1_cannot_see_protected_urls(self):
        self.client.login(username='test_normal_user', password='password')
        for key,value in namespaces_to_test.items():
            response = self.client.get(reverse(key, kwargs=value))
            self.assertEqual(response.status_code, 200)


class URLsTestALLOW_ADMIN_FALSE(TestCase):

    fixtures = [
        'users',
        'encrypteddisk',
    ]

    def setUp(self):
        self.client = Client()

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'False'})
    def test1_cannot_see_protected_urls(self):
        self.client.login(username='test_normal_user', password='password')
        for key,value in namespaces_to_test.items():
            response = self.client.get(reverse(key, kwargs=value))
            self.assertEqual(response.status_code, 403)

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'False'})
    def test2_cannot_see_protected_urls_with_settings_override(self):
        with self.settings(ALLOW_ADMIN=True):
            self.client.login(username='test_normal_user', password='password')
            for key,value in namespaces_to_test.items():
                response = self.client.get(reverse(key, kwargs=value))
                self.assertEqual(response.status_code, 403)
