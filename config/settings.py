import os
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import dj_database_url

load_dotenv(Path(__file__).parent.parent / '.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['djangogramm-yurikoste.herokuapp.com', '0.0.0.0', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'sslserver',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'easy_thumbnails',
    'storages',
    'bootstrap4',
    'crispy_forms',
    'test_app.apps.TestAppConfig',
    'followering_and_likes.apps.FolloweringAndLikesConfig',
    'django_bootstrap_icons',
    'social_django'
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_GITHUB_KEY = getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = getenv('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangogramm',
        'USER': 'user',
        'PASSWORD': '12345',
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'test_app.DjangoGrammUser'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    # Needed to login by username in Django admin
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# EMAIL CONFIG
EMAIL_FROM_USER = getenv('EMAIL_FROM_USER')
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_HOST_USER = getenv('EMAIL_FROM_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = getenv('EMAIL_USE_TLS')
EMAIL_PORT = getenv('EMAIL_PORT')
SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')

if DEBUG:
    """
    Settings to run locally with Heroku local
    """
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
    PROJECT_ROOT = os.path.join(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, '../test_app/static/')
    STATIC_URL = '/static/'

    # Extra lookup directories for collectstatic to find static files
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, '../../test_app/img'),
    )

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    _PATH = os.path.abspath(os.path.dirname(__file__))
    MEDIA_ROOT = BASE_DIR
    MEDIA_URL = '/test_app/'
else:
    """
    Settings to run on the Heroku with AWS S3
    """
    # AWS S3 SETTINGS
    AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = getenv('S3_BUCKET_NAME')
    AWS_URL = getenv('AWS_URL')
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_S3_SIGNATURE_VERSION = 's3v4'


    # Static files (CSS, JavaScript, Images)
    STATIC_URL = AWS_URL + '/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = AWS_URL + '/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


    ##Static for Bootstrap
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

    STATIC_URL = '/static/'

    # Extra places for collectstatic to find static files.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


"""
Redirect settings
"""
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/feed"
LOGOUT_REDIRECT_URL = '/login/'


THUMBNAIL_ALIASES = {
    '': {
        'post_preview': {'size': (500, 500), 'crop': True},
    },
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

