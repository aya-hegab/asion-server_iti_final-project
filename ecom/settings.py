from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2-v(=82c@frr5y)(2vq867%jfon938*x_ipnjv26%0w07-gps%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'product.apps.ProductConfig',
    'category.apps.CategoryConfig',
    'order.apps.OrderConfig',
    'contactUs.apps.ContactusConfig',
    'review.apps.ReviewConfig',
    'cart.apps.CartConfig',
    'delivaryman.apps.DelivarymanConfig',
    'wishlist.apps.WishlistConfig',
    'banner.apps.BannerConfig',
    'rest_framework' ,
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'plan',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "ashiondb",
        "HOST": "localhost",
        "PORT":"5432",
        "USER":"postgres",
        "PASSWORD":"12345"

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

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
    ),
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

AUTH_USER_MODEL= 'users.User'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



MEDIA_URL = 'media/'  # This should be the URL where your media files are served from.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "taghreedmuhammed7@gmail.com"
EMAIL_HOST_PASSWORD = "czdqojphxvnwkkvk"
TAGGIT_CASE_INSENSITIVE = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STRIPE_PUBLIC_KEY="pk_test_51Ori5DKxvLWmSwKTHhWbP8C563cxgB3hNcXmyR3ekcYPdyU72FJ5qunHFjBLc85NNFNlDoJR9Z5lGJMoFL40bGxh00oVXVBwJQ"
# STRIPE_SECRET_KEY="sk_test_51Ori5DKxvLWmSwKThggOsvo4Ayh3HrGANxSR8nIiHz7UAjH8xUsnJXZ0bYDKFU8cpYUTOuIQ3z1GCCmBCxZNh3ai000g8Tq5WG"
# STRIPE_SECRET_WEBHOOK="whsec_255ebc7d30e297a3004ea0df2d754d4298597ba3149da1fad360a26eeedf02db"

STRIPE_PUBLIC_KEY="pk_test_51OsRNnAnclBQmAKpRGVz2IzNgXn8IlDyyx1M03TYO8dOKPvAOUNrr2fWHVREhJ5c8YjalrjWJTvsea6rOdhaWydf00BY8e7dt0"
STRIPE_SECRET_KEY="sk_test_51OsRNnAnclBQmAKpW7b7tDwm8E5oQyYZBz1EVNpBSlsXhlaa65OHjmBIjAga9E3EuwNe1phDdk2XbzoFQOP0xs6y00ivabzHuy"
STRIPE_SECRET_WEBHOOK="whsec_4aba0fecb407d9e9b55250fbb420f38d35944687e651e1e11b57057c2739a6c3"
SITE_URL='http://localhost:3000/'
