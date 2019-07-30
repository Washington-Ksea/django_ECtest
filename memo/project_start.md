# はじめに

Djangoの基礎勉強のためECサイトに必要な基本機能を実装する。

## 参考文献

以下の文献を*かなり*参考にしました。

+ [現場で使えるDjangoの教科書 <<基礎編>>](https://www.amazon.co.jp/%E7%8F%BE%E5%A0%B4%E3%81%A7%E4%BD%BF%E3%81%88%E3%82%8B-Django-%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8%E3%80%8A%E5%9F%BA%E7%A4%8E%E7%B7%A8%E3%80%8B-%E6%A8%AA%E7%80%AC-%E6%98%8E%E4%BB%81/dp/4802094744)

+ [現場で使えるDjangoの教科書 <<実践編>>](https://booth.pm/ja/items/1030026)

+ [Practical Django 2 and Channels 2](https://www.apress.com/jp/book/9781484240984)

他、参考にした文献は適宜記載する。

# プロジェクトを始める

プロジェクトの開始

```javascript
mkdir django_test_project

cd django_test_project/

django-admin startproject config .
```

アプリ開発のため、python仮想環境の作成

```javascript

//仮想環境の作成
python3.6 -m venv venv

source venv/bin/activate
(venv):pip install Django==2.2
(venv):pip install django-allauth==0.39.1
(venv):deactivate
```

# プロジェクトの構成

開発環境を整える

```javascript
(venv):python manage.py  startapp main

```

config内の設定を開発用と実環境用に分ける  

mainにurls.pyを作成  

その他、静的ファイルやアプリのテンプレートを置いた結果

```javascript
tree -L 2 .

/*
.
├── README.md
├── config
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── develompment.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── main
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── memo.md
├── static
│   ├── css
│   └── js
├── templates
│   └── main
└── venv
*/
```

設定ファイルの位置変更に伴い、以下の変更を行う

```python
# manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
```

設定の追記

```python
#base.py

INSTALLED_APPS = [
    ...,
    'main.apps.MainConfig',
    ...
]

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

# 拡張設定-プロジェクトの補助

## Django Extensions

```javascript

(venv):pip install django-extensions
(venv):pip install pydotplus // for graph_models
(venv):pip install ipython   // for shell_plus
(venv):pip install werkzeug  // for runserver_plus

```

## Django Debug Toolbar

```javascript
(venv):pip install django-debug-toolbar
```

設定ファイルに追加

```python
#development.py
INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar'
)

#debug_toolbarは最初に入れる
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
 ] + MIDDLEWARE


INTERNAL_IPS = ['127.0.0.1']
```

.config/urls.pyにdebug_toolbarに関するでディパッチャを記載

```javascript

if env('DEBUG') == True:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```


## 環境変数の設定 - django-environ

```javascript
(venv):pip install django-environ
```

使い方

```python
import environ
env = environ.Env()
environ.Env.read_env('.env')

SECRET_KEY = env('SECRET_KEY')
```

# Databaseの設定（Mysql)

+ 参考　[いつもDjangoでMySQL(utf8mb4)を利用するときに行っているDjangoのDATABASE設定](https://qiita.com/shirakiya/items/71861325b2c8988979a2) 

```javascript
pip3 install mysqlclient
```

設定ファイルに設定を記載

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'), #　作成したデータベース名
        'USER': env('DB_USER'), # ログインユーザー名
        'PASSWORD': env('DB_PASS'),
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

```

## mysql インストール　起動　

+ 参考: [Mac での MySQL セットアップ](https://qiita.com/itooww/items/13055c8bb1d226ee5844)
  
```javascript
brew install mysql

mysql.server start

mysql -u root -p

//DB名 django_test, ユーザー名 mysiteuser, パスワード passwordとすると

mysql> CREATE DATABASE django_test;
mysql> CREATE USER 'mysiteuser'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON django_test.* TO 'mysiteuser'@'localhost';
mysql> FLUSH PRIVILEGES;

//ユーザー名を確認
SELECT user, host FROM mysql.user;
//ユーザー名の消去
DROP USER 'mysiteuser'@'localhost'

```



負荷やキャッシュヒット率は下がるが、InnoDBテーブルを圧縮のため、mysqlの設定と,manage.pyを変更

```python
#manage.py
...
    from django.db.backends.mysql.schema import DatabaseSchemaEditor
    DatabaseSchemaEditor.sql_create_table += " ROW_FORMAT=DYNAMIC"

```

```python
#/etc/mysql/mysql.conf.d/mysqld.cnf

[client]
port=3306
socket=/tmp/mysql.sock

[mysql]
port=3306
socket=/tmp/mysql.sock
default-character-set=utf8mb4

[mysqld]
character-set-server = utf8mb4
skip-character-set-client-handshake
collation-server = utf8mb4_general_ci
init-connect = SET NAMES utf8mb4
innodb_file_format = Barracuda
innodb_file_per_table = 1
innodb_large_prefix

sql_mode = TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY

```

## migrations 初期化

データベースをすべて削除して良い場合、以下を実行

```javascript
find . -path "*/migrations/0*.py" -delete
find . -path "*/migrations/__pycache__/0*.pyc" -delete

mysql -u root -p

mysql> drop database django_test;
create database django_test;

mysql.server restart


```

# django superuser の設定

```javascript
python manage.py createsuperuser
```