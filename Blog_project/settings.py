"""
Django settings for Blog_project project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# 设置默认字符编码为 UTF-8
DEFAULT_CHARSET = 'utf-8'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ufr6200zh1ryjd2q0%f@&dsi*#88&f#wrxl4jpgaqho*wu1)-g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['101.35.214.160']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'app01',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# CORS_ALLOWED_ORIGINS = [
#     # 添加允许的前端域名，例如：
# ]
# 可选配置：允许所有源 与上面CORS_ALLOWED_ORIGINS二选一
CORS_ALLOW_ALL_ORIGINS = True
# 跨域设置 
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
#允许所有的请求头
CORS_ALLOW_HEADERS = ('*')

ROOT_URLCONF = 'Blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Blog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'blog_project',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CHARSET': 'utf8mb4',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME':  'blog_project',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': 'mysql',
    #     'PORT': 3306,
    #     'CHARSET': 'utf8mb4',
    # },
    # SAE数据库配置
    # 'remote': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'xxx',
    #     'USER': 'xxx',
    #     'PASSWORD': 'xxx',
    #     'HOST': 'w.rdc.sae.sina.com.cn',
    #     'PORT': '3307',
    # }
}

#设置路由类
# DATABASE_ROUTERS = ['Gallery.db_router.LocalRemoteRouter']


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True #


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'


# STATIC_URL = 'static/dist/'
# STATICFILES_DIRS=[
#     os.path.join(BASE_DIR, 'static/dist/')
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# redis 配置
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         # "LOCATION": "redis://127.0.0.1:6379/1",
#         "LOCATION": "redis://192.168.121.134:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient", # 默认redis客户端
#             "CONNECTION_POOL_KWARGS": {"max_connections": 100}, # 最大连接数
#             "PASSWORD": "123456", # 密码
#             "PICKLE_VERSION": -1, # 指定pickle的序列化版本
#             "SOCKET_CONNECT_TIMEOUT": 2, # 单位秒，连接redis的超时时间 一般是60秒
#             "SOCKET_TIMEOUT": 2, # 单位秒，是执行redis命令的超时时间
#         }
#     }
# }
# # 缓存存储session会话
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# # 使用的缓存别名（默认内存缓存）
# SESSION_CACHE_ALIAS = "default"

