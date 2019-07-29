from .base import *
from script.get_env_dict import env



#####################
# Security settings #
#####################

DEBUG = True

SECRET_KEY = env['SECRET_KEY']

ALLOWED_HOSTS = ['*']


############
# Database #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env['DB_NAME'], #　作成したデータベース名
        'USER': env['DB_USER'], # ログインユーザー名
        'PASSWORD': env['DB_PASS'],
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True, #トランザクション
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY',
        },
        "TEST": {
            'NAME' : 'test_django_test'
        }
    }
}

###########
# Logging #
###########

LOGGING = {
    # バージョンは「1」固定
    'version': 1,
    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 開発用
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d ' '%(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

################
# Static files #
################

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

##################
# Email settings #
##################

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#####################
# Django Extensions #
#####################

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar'
)


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
 ] + MIDDLEWARE




INTERNAL_IPS = ['127.0.0.1']

