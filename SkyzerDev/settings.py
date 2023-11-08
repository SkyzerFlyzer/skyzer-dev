"""
Django settings for SkyzerDev project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import json
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from smart_media.settings import *
from lotus.settings import *

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['APP_SECRET_KEY']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

OIDC_RP_CLIENT_ID = os.environ['CLIENT_ID']
OIDC_RP_CLIENT_SECRET = os.environ['CLIENT_SECRET']
OIDC_RP_APIKEY = os.environ['API_KEY']
OIDC_OP_ISSUER = os.environ['ISSUER']
OIDC_OP_AUTHORIZATION_ENDPOINT = OIDC_OP_ISSUER + "/oauth2/authorize"
OIDC_OP_TOKEN_ENDPOINT = OIDC_OP_ISSUER + "/oauth2/token"
OIDC_OP_USER_ENDPOINT = OIDC_OP_ISSUER + "/oauth2/userinfo"
OIDC_RP_SCOPES = "openid profile email"
OIDC_RP_SIGN_ALGO = "HS256"
OIDC_OP_JWKS_ENDPOINT = OIDC_OP_ISSUER + "/.well-known/jwks.json"
LOGIN_REDIRECT_URL = os.environ['LOGIN_REDIRECT_URL']
LOGOUT_REDIRECT_URL = os.environ['LOGOUT_REDIRECT_URL']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
# convert to boolean
DEBUG = os.environ['DEBUG'].lower() in ['true', '1', 't']

ALLOWED_HOSTS = json.loads(os.environ['ALLOWED_HOSTS'])

# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    "sorl.thumbnail",
    "smart_media",
    "ckeditor",
    "ckeditor_uploader",
    "taggit",
    "lotus",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SkyzerDev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SkyzerDev.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = "/var/www/skyzer.dev/static/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
)

CKEDITOR_UPLOAD_PATH = "uploads/"
CSRF_TRUSTED_ORIGINS = json.loads(os.environ['TRUSTED_ORIGINS'])