"""
Django settings for gctade project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p^2h9ju&m6wsl4+0+)5h+!v#$t*@2!l65*lmp-vzptu(!oj)p_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
]
CUSTOM_APPS = ["apps.product", "apps.bot"]
THIRD_PARTY_APPS = [
    "rest_framework",
    "ckeditor",
    "ckeditor_uploader",
    "modeltranslation",

]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gctade.urls'

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

WSGI_APPLICATION = 'gctade.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_todo_list',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '5432',
        "ATOMIC_REQUESTS": True
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
LENGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian')
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_FALLBACK_LANGUAGE = {'default': ('en',)}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEDITOR configuration
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_FORCE_JPEG_COMPRESSION = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = True
CKEDITOR_CONFIGS = {
    "default": {
        # 'skin': 'moono',
        "toolbar": "full",
        "height": 300,
        "width": "100%",
        "extraPlugins": ",".join(["image"]),
        "extraAllowedContent": "figure figcaption",
    },
}