"""
Django settings for dpexmem project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from machina import MACHINA_MAIN_STATIC_DIR

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INT_APPS = [
    'advisors',
    'courses',
    'contact',
    'dmedia',
    'events',
    'eauth',
    'home',
    'search',
    'feed',
    'news',
    'partners',
    'utils',
    'videos',
    'research',
    'registration',
    'roadmaps',
    'tools_resources',
    'updates',
    'users',
    'attendances',
    'seoroute',
    'stats'
]

EXT_APPS = [
    'allauth',
    'allauth.account',
    'blog',
    'compressor',
    'crispy_forms',
    'django_extensions',
    'django_select2',
    'djmoney',
    'froala_editor',
    'froala_editor_views',
    'intl_tel_input',
    'mailer',
    'modelcluster',
    'phonenumber_field',
    'rest_framework',
    'stream_django',
    'taggit',
    'wagtailgeowidget',
]

MACH_APPS = [
    'mptt',
    'haystack',
    'widget_tweaks',

    # Machina apps:
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',
]

WAG_APPS = [
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
]

INSTALLED_APPS = DJANGO_APPS + EXT_APPS + INT_APPS + MACH_APPS + WAG_APPS


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'dpexmem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'machina.core.context_processors.metadata',
                'django_settings_export.settings_export',
                'eauth.context_processors.signup',
                'eauth.context_processors.login',
                'utils.context_processors.current_url',
                'utils.context_processors.site_data'
            ],
        },
    },
]

# WSGI_APPLICATION = 'dpexmem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Wagtail settings

WAGTAIL_SITE_NAME = "dpexmem"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = '/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

MACHINA_FORUM_IMAGE_WIDTH = None
MACHINA_FORUM_IMAGE_HEIGHT = None

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DATE_INPUT_FORMATS": ["%M %b, %Y"],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.CustomPagination',
    'PAGE_SIZE': 15
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
)

SETTINGS_EXPORT = [
    'GOOGLE_MAPS_V3_APIKEY',
    'BRAIN_KEY',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MACHINA_FORUM_NAME = 'Discussions'


import moneyed
from moneyed.localization import _FORMATTER
_FORMATTER.add_sign_definition('DEFAULT', moneyed.USD, prefix='USD')


COUNTRIES_OVERRIDE = {
    'ON': 'Online Webinar',
}


WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'froala_editor.widgets.FroalaEditor'
    }
}