SECRET_KEY = "secret"
SITE_ID = 1

INSTALLED_APPS = (
    "django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms.fields",
    "sekizai",
    "cms",
    "menus",
    "treebeard",
    "parler",
    "djangocms_alias",
    "djangocms_versioning",
    "djangocms_text",
    "easy_thumbnails",
    "filer",
    "mptt",
    "sortedm2m",
    "taggit",
    "aldryn_common",
    "aldryn_apphooks_config",
    "aldryn_categories",
    "aldryn_people",
    "aldryn_translation_tools",
    "aldryn_newsblog",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "tests.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGE_CODE = 'en'
STATIC_URL = "/static/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tests/templates'],
        'OPTIONS': {
            'context_processors': [
                # Django's defaults.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Needed by Django CMS.

                # Django CMS's core context processors.
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',  # Static file management for template blocks.
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

CMS_CONFIRM_VERSION4 = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
