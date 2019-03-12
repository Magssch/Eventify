from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from main.forms import EditProfileForm
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from main.views import * 


class HomeViewTestCaseNotAUser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.client = Client()
        self.url = reverse('homepage')

    def test_home_view_renders_correctl_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'main/home.html')
    
    def test_not_user_create_event_redirects_correct(self):
        url = reverse('create_event')
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_not_user_profile_redirects_correct(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_not_user_can_see_events(self):
        url = reverse('events')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'main/events.html') 
    
    def test_not_user_can_see_past_events(self):
        request = self.factory.get('/events')
        request.META['view_past']= 'True'
        response = events(request)
        self.assertEqual(response.status_code, 200)


    def test_not_user_can_view_terms(self):
        url = reverse('terms')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'main/terms.html')


class HomeViewTestCasualUser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.client = Client()
        self.url = reverse('homepage')
        self.user = User.objects.create_user(self.username, 'email@test.com', self.password, is_staff=False)
        self.login = self.client.login(username=self.username, password=self.password)
        self.user.is_staff = False
        self.user.save()

    def setup_request(self, request):
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()


    def test_home_view_renders_correctl_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'main/home.html')
    
    def test_user_create_event_redirects_correct(self):
        url = reverse('create_event')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_valid_user_can_edit_profile(self):
        url = reverse('edit_profile')
        response = self.client.get(url, follow=True)
        request = response.wsgi_request
        self.assertTemplateUsed(response, 'registration/edit_profile.html')       

    def test_user_edit_profile_post(self):
        request = self.factory.get('/edit_profile')
        request.user = self.user
        request.method = 'POST'
        response = edit_profile(request)
        self.assertEqual(response.status_code, 302)

class HomeViewTestStaffUser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.client = Client()
        self.url = reverse('homepage')
        self.user = User.objects.create_user(self.username, 'email@test.com', self.password, is_staff=False)
        self.login = self.client.login(username=self.username, password=self.password)
        self.user.is_staff = True
        self.user.save()

    def setup_request(self, request):
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def test_staff_create_event_redirects_correct(self):
        request = self.factory.get('/create_event')
        request.user = self.user
        response = create_event(request)
        self.assertEqual(response.status_code, 200)
