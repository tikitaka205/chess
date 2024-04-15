from pathlib import Path
import os
# import django.contrib.postgres.fields

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

DP_MODE = False # 배포 모드 설정 Deploy_Mode

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret') if DP_MODE else 'secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False if DP_MODE else True

# ALLOWED_HOSTS = []
if os.environ.get('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS=os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
else:
    ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['backend'] if DP_MODE else ['*']

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # service app
    'chess',
    'user',
    'chat',


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blindchess.urls'

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

WSGI_APPLICATION = 'blindchess.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ],
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# POSTGRES_DB 뒤 들어가는건 없을때의 디폴트값을 쓴다
# POSTGRES_DATABASE = os.environ.get('POSTGRES_DB', '')
#  if DP_MODE else False
# print("DP_MODE",DP_MODE)
# print("POSTGRES_DATABASE",POSTGRES_DATABASE)
# if POSTGRES_DATABASE:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'
ASGI_APPLICATION = "blindchess.asgi.application"

# if DP_MODE:
#     CHANNEL_LAYERS = {
#         "default": {
#             "BACKEND": "channels_redis.core.RedisChannelLayer",
#             "CONFIG": {
#                 "hosts": [("127.0.0.1", 6379)],
#             },
#         },
#     }
# else:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#CORS 모든 호스트 허용
# CORS
# live server port 5500
# CORS_ORIGIN_WHITELIST = ['localhost', '127.0.0.1', '[::1]', '0.0.0.0']

# 예외 없이 다 수락
# CORS_ALLOW_CREDENTIALS = False if DP_MODE else True
# CORS_ALLOW_ALL_ORIGINS = False if DP_MODE else True
# CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
CORS_ORIGIN_ALLOW_ALL = True



# LOGGING = {
#     'version': 1,	#logging 버젼
#     'disable_existing_loggers': False, # 원래 있던 로깅들을 그래도 냅둠 # 만약 True면 못쓴다는 거겠죠?
#     'handlers': {					# 로깅 메세지에서 일어나는 일을 결정하는 녀석이라고 장고공식문서에 나와있다
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {				# 로깅을 console에 띄울지 ... 다른데 띄울지 그냥 DEBUG용으로 레벨을 설정할 수 도있고,
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }