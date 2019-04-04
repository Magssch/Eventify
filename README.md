## Eventify <a href="https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-32/-/jobs" rel="nofollow"><img src="https://camo.githubusercontent.com/e0ccc5d7f1cfb949df587a15d495a7ee7a9534ba/68747470733a2f2f6170692e7472617669732d63692e6f72672f7761677461696c2f7761677461696c2e7376673f6272616e63683d6d6173746572" alt="Build Status" data-canonical-src="https://api.travis-ci.org/wagtail/wagtail.svg?branch=master" style="max-width:100%;"></a>

Eventify is an event platform where you can make your own events and attend others events. The platform should also give the user an easy way to keep track of future events you are attending. Further it was a priority from the customer that security should be taken care of.

![Homepage](./example.png "Eventify - Homepage")
## Motivation

This project was a part of our submission in the subject TDT4140 Programvareutvikling. Our product owner is Eventify and they wanted us to make a fully functional event platform.


## Techonology stack

#### Frameworks:

<ul>
<li><a href="https://www.djangoproject.com/" rel="nofollow">Django</a> - Web framework for Python</li>
<li><a href="https://www.postgresql.org/" rel="nofollow">PostgreSQL</a> - Database</li>
<li><a href="https://materializecss.com/" rel="nofollow">Materialize CSS</a> - Front-end framework</li>
<li><a href="https://pypi.org/project/django-bootstrap4/" rel="nofollow">Bootstrap 4</a> - CSS framework</li>
</ul>

#### Dependencies:

* numpy 
* pyserial 
* pytz 
* psycopg2 
* gunicorn 
* dj-database-url 
* whitenoise 
* Pillow 
* django-newsletter


## Django directory structure
```
├── manage.py
├── eventifySite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   └── . . .
    ├── models.py
    ├── static
    │   └── main
    │       ├── css
    │       │   └── . . .
    │       ├── fonts
    │       │   └── . . .
    │       ├── images
    │       │   └── . . .
    │       └── js
    │           └── . . .
    ├── templates
    │   ├── main
    │   │   └── . . .
    │   └── registration
    │       └── . . .
    ├── tests
    │   └── . . .
    ├── urls.py
    └── views.py
```


## Development setup

* Install postgreSQL from <a href="https://www.postgresql.org/download/" rel="nofollow">here</a>

* *(Recommended)* Setup virtualenv

* Install requirements:

    * `$ pip install -r requirements.txt`

* Setup newletter component:

    In views.py SITE_NEWSLETTER and SITE_EMAIL are set by default to:
    
    * SITE_NEWSLETTER = 'Eventify'
    * SITE_EMAIL = 'eventify.site@gmai.com'
    
    These can be changed by choice. The values declare the name and email for the sites newsletter.
    
    ![Views](./SITE.png "views")
    
* SMTP setup / Email backend:

    To send mail, django-newsletter uses Django-provided email utilities, so ensure that email settings are properly configured for your project.
    The utilities are set by default, but can be configured in settings.py.
    
    * EMAIL_HOST = 'localhost'
    * EMAIL_PORT = 25
    * EMAIL_USER = ' '
    * EMAIL_HOST_PASSWORD = ' '
    * EMAIL_USE_TLS = False
    * EMAIL_USE_SSL = False
    
    * EMAIL_HOST:
        * The host to use for sending email i.e. gmail, outlook, etc.
    
    * EMAIL_PORT:
        * 

* Start server:

    * `$ python manage.py runserver`

* Create admin user to access admin page:

    * `$ python manage.py createsuperuser`

## Tests

Running the tests:

* `$ coverage run manage.py test`
