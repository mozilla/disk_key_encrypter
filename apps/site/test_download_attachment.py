from django.conf.urls import url, include
from django.urls import reverse
from django.test import TestCase, Client, modify_settings
from django.test.utils import override_settings
from django.conf import settings
from mock import patch
from apps.site.models import EncryptedDisk
import os
import mock

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