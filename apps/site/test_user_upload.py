from django.conf.urls import url, include
from django.urls import reverse
from django.test import TestCase, Client, modify_settings
from django.test.utils import override_settings
from django.conf import settings
from mock import patch
from apps.site.models import EncryptedDisk
import os
import mock


class NonPrivilegedUserUpload(TestCase):

    fixtures = [
        'users',
        'encrypteddisk',
    ]

    def setUp(self):
        self.client = Client()


    def test1_index_page_redirects_to_user_upload(self):
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse("index_upload"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("upload"))
        
    def test2_upload_form_has_proper_fields(self):
        proper_fields = [
            'asset_tag',
            'encryption_type',
            'recovery_key',
            'binary_blob',
        ]
        improper_fields = [
            'legacy_binary_blob',
            'legacy_binary_blob_data',
            'file_data',
        ]
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse("upload"))
        response_fields = response.context['form'].fields
        for field in proper_fields:
            self.assertTrue(field in response_fields)
        for field in improper_fields:
            self.assertFalse(field in response_fields)
        self.assertEqual(len(response_fields), len(proper_fields))

    def test3_form_save_sets_redirect(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        response = self.client.post(reverse("upload"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '?success=1')

    def test4_form_save_sets_asset_tag(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        response = self.client.post(reverse("upload"), data=data)
        after_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(after_disks), 2)
        created_disk = after_disks[1]
        self.assertEqual(created_disk.asset_tag, data['asset_tag'])

    def test5_form_save_sets_recovery_key_encrypted(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        response = self.client.post(reverse("upload"), data=data)
        after_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(after_disks), 2)
        created_disk = after_disks[1]

        self.assertFalse(data['recovery_key'] in created_disk.recovery_key)
        self.assertTrue('-----BEGIN PGP MESSAGE-----' in str(created_disk.recovery_key))
        self.assertTrue('-----END PGP MESSAGE-----' in str(created_disk.recovery_key))

    def test6_form_save_sets_binary_data(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        with open('./apps/site/fixtures/users.json') as fp:
            data['binary_blob'] = fp
            response = self.client.post(reverse("upload"), data=data)
            after_disks = EncryptedDisk.objects.all()
            self.assertEqual(len(after_disks), 2)
            created_disk = after_disks[1]
            self.assertFalse('user' in created_disk.recovery_key)
            self.assertTrue('-----BEGIN PGP MESSAGE-----' in str(created_disk.file_data))
            self.assertTrue('-----END PGP MESSAGE-----' in str(created_disk.file_data))
    def test7_form_save_sets_file_name(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        with open('./apps/site/fixtures/users.json') as fp:
            data['binary_blob'] = fp
            response = self.client.post(reverse("upload"), data=data)
            after_disks = EncryptedDisk.objects.all()
            self.assertEqual(len(after_disks), 2)
            created_disk = after_disks[1]
            self.assertEqual('users.json', created_disk.file_name)

    def test8_can_download_encrypted_file_just_uploaded(self):
        data = {
            'asset_tag': '1234',
            'recovery_key': 'ABCD1234',
            'encryption_type': '1',
        }
        self.client.login(username='test_normal_user', password='password')
        initial_disks = EncryptedDisk.objects.all()
        self.assertEqual(len(initial_disks), 1)
        with open('./apps/site/fixtures/users.json') as fp:
            data['binary_blob'] = fp
            response = self.client.post(reverse("upload"), data=data)
        new_disk = EncryptedDisk.objects.all()[1]
        download_response = self.client.get(reverse("attach", kwargs={'id': new_disk.id}))
        self.assertEqual(download_response.content.decode("utf8"), new_disk.file_data)