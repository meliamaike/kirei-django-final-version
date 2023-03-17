import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z2rnfsj2ob$5$!9vkk*1cc5jt6)%toi_!k$8wk^+9ztw!bnn_h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Other apps
    "cart",
    "crispy_forms",
    "crispy_bootstrap4",
    # My Apps
    "agendas.apps.AgendasConfig",
    "appointments.apps.AppointmentsConfig",
    "carts.apps.CartsConfig",
    "customers.apps.CustomersConfig",
    "home.apps.HomeConfig",
    "invoices.apps.InvoicesConfig",
    "orders.apps.OrdersConfig",
    "payments.apps.PaymentsConfig",
    "products.apps.ProductsConfig",
    "professionals.apps.ProfessionalsConfig",
    "services.apps.ServicesConfig",
    "shoppingcarts.apps.ShoppingcartsConfig",
    "staff.apps.StaffConfig",
    "statistic.apps.StatisticConfig",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django Allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


AUTH_USER_MODEL = "customers.Customer"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# For Allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_RATE_LIMITS = {}
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# # ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# # # ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"

ROOT_URLCONF = "kireidjangoapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processor.cart_total_amount",
                "carts.context_processors.cart_total_quantity",
            ],
            "libraries": {
                "my_filters": "products.templatetags.my_filters",
            },
        },
    },
]

WSGI_APPLICATION = "kireidjangoapp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = "America/Argentina/Buenos_Aires"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

CSRF_COOKIE_HTTPONLY = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = "bootstrap4"

ACCOUNT_FORMS = {
    "signup": "customers.forms.RegisterForm",
    "login": "customers.forms.CustomerLoginForm",
}

# DJANGO-SHOPPING-CART

CART_SESSION_ID = "cart"

