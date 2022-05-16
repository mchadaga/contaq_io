from .settings import *

import django_heroku
django_heroku.settings(locals())

# set SECRET_KEY environment variable to override this
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# On Heroku secure Redis requires disabling ssl certificate checking
# more details here: https://devcenter.heroku.com/articles/connecting-heroku-redis#connecting-in-python

REDIS_URL_FROM_ENV = os.environ.get('REDIS_TLS_URL', os.environ.get('REDIS_URL'))
if REDIS_URL_FROM_ENV and REDIS_URL_FROM_ENV.startswith('rediss'):
    CELERY_BROKER_URL = f"{REDIS_URL_FROM_ENV}?ssl_cert_reqs=none"
    CELERY_RESULT_BACKEND = f"{REDIS_URL_FROM_ENV}?ssl_cert_reqs=none"

# fix ssl mixed content issues
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django security checklist settings.
# More details here: https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security settings
# Without uncommenting the lines below, you will get security warnings when running ./manage.py check --deploy
# https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security

# # Increase this number once you're confident everything works https://stackoverflow.com/a/49168623/8207
# SECURE_HSTS_SECONDS = 60
# # Uncomment these two lines if you are sure that you don't host any subdomains over HTTP.
# # You will get security warnings if you don't do this.
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

USE_HTTPS_IN_ABSOLUTE_URLS = True

DEBUG = False
ALLOWED_HOSTS = [
    'contaq.io',
    'contaq.herokuapp.com'
]

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

