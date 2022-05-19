"""
Django settings for Contaq.io project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'akdIakJsnSjviEWZKwrbCCpFWHdqYKteawHDFZts'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.forms',
]

# Put your third-party apps here
THIRD_PARTY_APPS = [
    'allauth',  # allauth account/registration management
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'rest_framework_api_key',
    'celery_progress',
    'djstripe',  # stripe integration
]

PEGASUS_APPS = [
    'pegasus.apps.examples.apps.PegasusExamplesConfig',
    'pegasus.apps.employees.apps.PegasusEmployeesConfig',
]

# Put your project-specific apps here
PROJECT_APPS = [
    'apps.subscriptions.apps.SubscriptionConfig',
    'apps.users.apps.UserConfig',
    'apps.api.apps.APIConfig',
    'apps.web',
    'apps.app'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PEGASUS_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contaq_io.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.web.context_processors.project_meta',
                 # this line can be removed if not using google analytics
                'apps.web.context_processors.google_analytics_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'contaq_io.wsgi.application'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 20
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'contaq_io', 
        'USER': 'postgres', 
        'PASSWORD': os.environ.get("pg_pwd"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}



# Auth / login stuff

# Django recommends overriding the user model even if you don't think you need to because it makes
# future changes much easier.
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Allauth setup

ACCOUNT_ADAPTER = 'apps.users.adapter.EmailAsUsernameAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True



# User signup configuration: change to "mandatory" to require users to confirm email before signing in.
# or "optional" to send confirmation emails but not require them
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


# enable social login
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static_root'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# uncomment to use manifest storage to bust cache when file change
# note: this may break some image references in sass files which is why it is not enabled by default
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# future versions of Django will use BigAutoField as the default, but it can result in unwanted library
# migration files being generated, so we stick with AutoField for now.
# change this to BigAutoField if you're sure you want to use it and aren't worried about migrations.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Email setup

# use in development
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("mailgun_key"),
    "MAILGUN_SENDER_DOMAIN": 'mg.contaq.io',
}
DEFAULT_FROM_EMAIL = "Contaq.io Team <no-reply@contaq.io>"
SERVER_EMAIL = "Contaq.io Team <no-reply@contaq.io>"
# use in production
# see https://github.com/anymail/django-anymail for more details/examples
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# Django sites

SITE_ID = 1

# DRF config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'apps.api.permissions.IsAuthenticatedOrHasUserAPIKey',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}


# Celery setup (using redis)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# Pegasus config

# replace any values below with specifics for your project
PROJECT_METADATA = {
    'NAME': "Contaq.io",
    'URL': 'http://contaq.io',
    'DESCRIPTION': "Contaq.io is a powerful lead generation tool that finds verified contacts in any niche and location!",
    'IMAGE': 'https://upload.wikimedia.org/wikipedia/commons/2/20/PEO-pegasus_black.svg',
    'KEYWORDS': 'SaaS, django',
    'CONTACT_EMAIL': 'mchadaga1@gmail.com',
}

USE_HTTPS_IN_ABSOLUTE_URLS = False  # set this to True in production to have URLs generated with https instead of http

ADMINS = [('Mani Chadaga', 'mchadaga1@gmail.com')]

GOOGLE_ANALYTICS_ID = ''  # replace with your google analytics ID to connect to Google Analytics


# Stripe config

STRIPE_PAYMENT_MODE = 'elements'  # change to "elements" to try Stripe-elements-based embedded payments

# modeled to be the same as https://github.com/dj-stripe/dj-stripe
STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "pk_live_51KpDrzGI5m9eEtt4v5PrTXEGSbqXPkl8hGYQoiYHgU26vR7B07pUolBMXVmv2fIEHI0JHq8NUzrAFbwCWMxegTXG00GdtsVZRg")
STRIPE_LIVE_SECRET_KEY = os.environ.get("stripe_live_key")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_51KpDrzGI5m9eEtt4XzBqfHqDv6xOw0Bx1GZpGBjoHj3nJjNOAkglDKi9os5PGAsxG8nQK6sNaWi1NnI1xRFpgWn200PwP0MPYM")
# STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", os.environ.get("stripe_key"))
STRIPE_TEST_SECRET_KEY = os.environ.get("stripe_key")
STRIPE_LIVE_MODE = (os.environ.get("LIVE_MODE")=="TRUE")  # Change to True in production

# djstripe settings
# Get it from the section in the Stripe dashboard where you added the webhook endpoint
# or from the stripe CLI when testing
# DJSTRIPE_WEBHOOK_SECRET = os.environ.get('DJSTRIPE_WEBHOOK_SECRET', os.environ.get("stripe_whsec"))
if STRIPE_LIVE_MODE:
    DJSTRIPE_WEBHOOK_SECRET = os.environ.get("stripe_live_whsec")
else:
    DJSTRIPE_WEBHOOK_SECRET = os.environ.get("stripe_whsec")

DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'  # change to 'djstripe_id' if not a new installation
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # change to False if not a new installation
