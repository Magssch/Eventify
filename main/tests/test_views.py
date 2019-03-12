from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from main.forms import EditProfileForm
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
import unittest
from PIL import Image
from django.utils.six import BytesIO

from main.views import * 
from main.forms import *

# "borrowed" from easy_thumbnails/tests/test_processors.py
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='JPEG'):
    """
    Generate a test image, returning the filename that it was saved as.
    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


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

    #@unittest.skip("WIP")
    def test_user_edit_profile_post(self):
        request = self.factory.get('/edit_profile')
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        request.method = 'POST'
        response = edit_profile(request)
        self.assertEqual(response.status_code, 302)

        #My solution was to just mock out the messages framework for those tests, there may be better solutions (the django test client?)

class HomeViewTestStaffUser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.client = Client()
        self.url = reverse('homepage')
        self.user = User.objects.create_user(self.username, 'email@test.com', self.password, is_staff=False)
        self.user.is_staff = True
        self.login = self.client.login(username=self.username, password=self.password)
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


        
    def test_staff_can_create_event(self):
        ## Creating image
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = create_image(None, 'testbilde.jpg')
        image_file = SimpleUploadedFile('testbilde.jpg', image.getvalue())

        ## Setting up request
        request = self.factory.get('/create_event')
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        request.POST._mutable = True
        request.POST['name']= 'Test'
        request.POST['location'] = 'Trondheim'
        request.POST['price'] = '1'
        request.POST['description'] = 'Desc'
        request.POST['date'] = timezone.now()
        request.FILES['image'] = image_file
        form = EventForm(request.POST or None, request.FILES or None) 
        self.assertTrue(form.is_valid())
        response = create_event(request)
        self.assertEqual(response.status_code, 302) 


    #@unittest.skip("WIP")
    def test_staff_can_update_event(self):
        ## Creating image
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = create_image(None, 'testbilde.jpg')
        image_file = SimpleUploadedFile('testbilde.jpg', image.getvalue())

        ## Setting up request
        request = self.factory.get('/create_event')
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        request.POST._mutable = True
        request.POST['name']= 'Test'
        request.POST['location'] = 'Trondheim'
        request.POST['price'] = '1'
        request.POST['description'] = 'Desc'
        request.POST['date'] = timezone.now()
        request.FILES['image'] = image_file
        form = EventForm(request.POST or None, request.FILES or None) 
        self.assertTrue(form.is_valid())
        response = create_event(request)
        self.assertEqual(response.status_code, 302) 
         
        #Getting the event 
        events_list = Event.objects.all()
        paginator = Paginator(events_list, 4)
        page = request.GET.get('page')
        events = paginator.get_page(page)
        my_event = events.__getitem__(0)
        id = my_event.__getattribute__('id')

        request = self.factory.get('event_update')
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = event_update(request, id)
        self.assertEqual(response.status_code, 200)

        request.POST._mutable = True
        request.POST['name']= 'Test'
        request.POST['location'] = 'Trondheim'
        request.POST['price'] = '1'
        request.POST['description'] = 'Desc'
        request.POST['date'] = timezone.now()
        request.FILES['image'] = image_file
        response = event_update(request, id)
        self.assertEqual(response.status_code, 302)

        #Checks that non-staff gets redirected (cannot update event)
        self.user.is_staff = False
        self.user.save()
        response = event_update(request, id)
        self.assertEqual(response.status_code, 302)

        #Checks that non-staff gets redirected (cannot update event)
        self.username = 'myuser2'
        self.password = 'valid_password2'
        self.user = User.objects.create_user(self.username, 'email@test2.com', self.password, is_staff=True)
        self.user.is_staff = True
        self.login = self.client.login(username=self.username, password=self.password)
        self.user.save()
        request.user = self.user
        response = event_update(request, id)
        self.assertEqual(response.status_code, 302)


    
