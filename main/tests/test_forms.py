from django.test import Client
from django.test import TestCase, RequestFactory

from main.forms import *


class FormTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.user = User.objects.create_user(self.username, 'email@test.com', self.password, is_staff=False)
        self.client = Client()

    def test_registration_form_saves_data_to_instance_user_on_save(self):
        """ Tests that the form saves name, email to user object when committing form"""
        form = RegistrationForm(data={'check': True, 'username': 'user2',
                                      'first_name': 'user',
                                      'last_name': 'userlast',
                                      'email': 'email@test.com',
                                      'password1': self.password,
                                      'password2': self.password})
        self.assertTrue(form.is_valid())
        person = form.save()
        self.assertEqual(person.first_name, 'user')
