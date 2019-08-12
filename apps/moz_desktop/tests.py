import os
import mock
from django.urls import reverse
from django.test import TestCase
from django.test import TestCase, Client, modify_settings
import apps.site.models as site_models
from apps.site.forms import UploadFormDesktop, UploadFormDesktopUpload
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


class TestADMINAttachmentForm(TestCase):

    fixtures = [
        'users',
        'encrypteddisktwodisks',
    ]

    def setUp(self):
        self.client = Client()

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test1_can_see_attachment(self):
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse('attach', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test2_can_see_detail(self):
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse('detail', kwargs={'id_value': 1}))
        self.assertEqual(response.status_code, 200)

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test3_detail_form_has_recovery_key_not_binary(self):
        self.client.login(username='test_normal_user', password='password')
        disk = get_object_or_404(site_models.EncryptedDisk, id=1)
        form = UploadFormDesktop(instance=disk)

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test3_detail_form_has_recovery_key_not_binary(self):
        key_text = 'ASDFASDF'
        data = {
            'user': User.objects.get(pk=1).id,
            'email_address': 'foo@mozilla.com',
            'asset_tag': '123456',
            'encryption_type': '1',
            'recovery_key': 'ASDFASDF',

        }
        upload_form = UploadFormDesktopUpload(data=data)
        tmp_form = upload_form.save()
        self.assertFalse(tmp_form.recovery_key.startswith("b'"))

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test4_ensure_data_encrypted(self):
        key_text = 'ASDFASDF'
        data = {
            'user': User.objects.get(pk=1).id,
            'email_address': 'foo@mozilla.com',
            'asset_tag': '123456',
            'encryption_type': '1',
            'recovery_key': 'ASDFASDF',

        }
        upload_form = UploadFormDesktopUpload(data=data)
        tmp_form = upload_form.save()
        self.assertFalse(key_text in tmp_form.recovery_key)

    @mock.patch.dict(os.environ, {'ALLOW_ADMIN': 'True'})
    def test5_data_starting_with_binary_leader_gets_stripped(self):
        self.client.login(username='test_normal_user', password='password')
        response = self.client.get(reverse('detail', kwargs={'id_value': 2}))
        self.assertFalse(response.context['form'].initial['recovery_key'].startswith("b'"))
