"""
Django settings for chatbot project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    SECRET_KEY = '5j9=_4mk70udr3nw%zpq^7km)!74-%pmcj5c#wo1$^8he*@x=f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'chatbot.apps.common',
    'chatbot.apps.creditors',
    'chatbot.apps.debts',
    'chatbot.apps.jobs',
    'chatbot.apps.motion_ai',
    'chatbot.apps.profiles',
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

ROOT_URLCONF = 'chatbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
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

WSGI_APPLICATION = 'chatbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'PST8PDT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if 'ENVIRONMENT' in os.environ:
    ENVIRONMENT = os.environ['ENVIRONMENT']
else:
    ENVIRONMENT = 'DEV'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {
    'default': db_from_env
}

if ENVIRONMENT == 'STAGING':
    # Static file storage for Heroku
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Motion AI
# MOTION_AI_API_KEY = os.environ.get('MOTION_AI_API_KEY')
MOTION_AI_WEBHOOK_SECRET = os.environ.get('MOTION_AI_WEBHOOK_SECRET')
MOTION_AI_DEBT_NEW = 478927  # whenever we encounter this module, a new debt is being created
MOTION_AI_JOB_NEW = 478771  # whenever we encounter this module, a new debt is being created

MOTION_AI_MODULE_MAPPING = {
    33251: {
        'User': {
            402680: 'email',
            402681: 'knowWhereToStart',
            402677: 'totalDebt',
            402678: 'averageInterestRate',
            402679: 'monthlyDebtPayments',
            402673: 'incomeYN',
            402674: 'incomeAmount',
            402675: 'incomeConsistency',
            402682: 'situationDetail',
            402891: 'houseHoldSize',
            402889: 'homeEquity',
            402879: 'ownHome',
            408193: 'behindOnPayments',
            402782: 'daysPastDue',
            402733: 'firstName'
        }
    },

    # CRN V3
    35583: {
        'User': {
            426478: 'firstName',
            426490: 'questionConsultation',

            # question
            435920: 'email',
            426493: 'situationDetail',

            # consultation
            426470: 'incomeAmount',
            426471: 'incomeConsistency',
            426472: 'totalDebt',
            426474: 'monthlyDebtPayments',
            426473: 'averageInterestRate',
            426479: 'behindOnPayments',
            426480: 'daysPastDue',
            426482: 'ownHome',
            426483: 'homeEquity',
            426484: 'houseHoldSize',
            426505: 'state',
            426518: 'phoneOrEmail',
            426475: 'email',
            426486: 'phone',
            426517: 'situationDetail'
        }
    },

    # Fin 3
    39785: {
        'User': {
            478908: 'firstName',

            502695: 'questionConsultation',

            # question
            502697: 'email',
            502710: 'situationDetail',

            # consultation
            478903: 'is_married',
            478759: 'employment_status',

            478859: 'additional_income',
            478865: 'additional_income_amount',
            490584: 'additional_income_consistent',

            478912: 'state',
            478895: 'ownHome',
            478902: 'homeEquity',
            478905: 'houseHoldSize',

            506804: 'totalDebt',
            506805: 'basic_hardship',
            506851: 'monthlyDebtPayments',

            478957: 'credit_score_importance',
            478962: 'needs_future_student_loan',
            478963: 'needs_future_auto_loan',
            478964: 'needs_future_mortgage',

            502737: 'phoneOrEmail',
            502738: 'phone',
            478975: 'email',
            478978: 'situationDetail'
        },
        'Debt': {
            478927: 'creditor_name',
            481737: 'collection_agency',
            478929: 'balance',
            478933: 'interest_rate',
            478932: 'last_paid_at',
            478942: 'monthly_payment',
            478944: 'status',
            478946: 'money_movement'
        },
        'Job': {
            478771: 'employer_name',
            478773: 'employment_length',
            478862: 'income',
            478836: 'income_consistency'
        }
    }
}

# Heavenly
HEAVENLY_URL = os.getenv('HEAVENLY_URL')
HEAVENLY_USERNAME = os.getenv('HEAVENLY_USERNAME')
HEAVENLY_PASSWORD = os.getenv('HEAVENLY_PASSWORD')

# Intercom
INTERCOM_APP_ID = os.getenv('INTERCOM_APP_ID')
INTERCOM_TOKEN = os.getenv('INTERCOM_TOKEN')

# Other
KIRKWOOD_URL = os.getenv('KIRKWOOD_URL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
# TODO: Actually integrate Raven with Django
RAVEN_DSN = os.getenv('RAVEN_DSN')
