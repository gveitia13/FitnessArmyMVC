"""
Django settings for FitnessArmyMVC project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!l3fn95^xeq&v2k4*y@e$u^6!2k0&87i5t1g5re1!ft5a3&si%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'rest_framework',
    'ckeditor',
    'django_cleanup.apps.CleanupConfig',
    'app_main',
    'app_cart',
]

CKEDITOR_CONFIGS = {
    'default': {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
        ],
        "toolbar": "Full",
        "height": 150,
        "width": 500,
        "filebrowserWindowWidth": 940,
        "filebrowserWindowHeight": 725,
    }
}

BUSINESS_LOGO_PATH = 'admin/img/logo.jpg'
BUSINESS_NAME = 'Fitness Army'
BUSINESS_NAME_IMG_PATH = 'admin/img/logo.jpg'
BUSINESS_ICON_PATH = 'admin/img/favicon.ico'

JAZZMIN_SETTINGS = {
    "site_brand": BUSINESS_NAME,
    "welcome_sign": '',
    'site_icon': BUSINESS_ICON_PATH,
    'site_logo': BUSINESS_LOGO_PATH,
    'site_logo_classes': 'brand-image',
    "login_logo": BUSINESS_NAME_IMG_PATH,
    "login_logo_dark": False,
    'site_header': BUSINESS_NAME,
    "custom_css": 'admin/css/admin.css',
    'copyright': 'By GoDjango',
    'custom_js': 'admin/js/admin.js',
    # "related_modal_active": True,
    # "search_model": ["auth.User", "auth.Group"],
    # "show_ui_builder": True,
    "user_avatar": 'get_profile_photo',
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-users",
        "auth.Group": "fas fa-users",
        "app_main.Config": "fas fa-cog",
        "app_main.Product": "fas fa-box-open",
        "app_main.Contact": "fas fa-envelope",
        "app_main.Subscriptor": "fas fa-user-plus",
        "app_main.Orden": "fas fa-chart-line",
        "app_main.ComponenteOrden": "fas fa-shopping-bag",
        "app_main.Offer": "fas fa-envelope-open-text",
        # "app_main.Offer": "fas fa-newspaper",
    },
    "order_with_respect_to": ['app_main', 'app_main.config', 'app_main.product', 'app_main.orden',
                              'app_main.componenteorden', 'app_main.offer', 'app_main.contact', 'app_main.subscriptor'],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'FitnessArmyMVC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'FitnessArmyMVC.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_REDIRECT_URL = '/admin/'
#
# LOGOUT_REDIRECT_URL = reverse_lazy('login')
#
# LOGIN_URL = reverse_lazy('login')
#
# AUTH_USER_MODEL = 'user.User'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply.paula8@gmail.com'
EMAIL_HOST_PASSWORD = 'ygjeeypvloptzxzp'

CART_SESSION_ID = "cart"
