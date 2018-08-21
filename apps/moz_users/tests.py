"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase, Client


class MozUserTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()

    def test1_login_page(self):
        self.assertEqual(1, 1)
