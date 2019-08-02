#./mamage.py コマンド生成

./manage.py のコマンドによりデータベースにデータを挿入する。

コマンドの作成場所はアプリケーションmainの中で、

```javascript
(venv) mkdir main/management
(venv) touch main/management/__init__.py
(venv) mkdir main/management/commands
(venv) touch main/management/commands/__init__.py
```

により作成する。  
そして、main/management/commands/import_data.pyにおいて

```python
class Command(BaseCommand):
    help = 'Import user data'

    def handle(self, *args, **options):
        self.stdout.write("Importing products")

```

とすると、以下のようにコマンドが生成されている

```javascript
//./manage.py
...
[main]
    import_data
...

//./manage.py import_data
"Importing products"
```

# サムネイルの作成

製品の画像を並べて表示するため、圧縮したもの

作成したコマンド例 

signals.pyを読み出し

```python
#main/app.py
class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from . import signals

```

```javascript
./manage.py import_data ./main/fixtures/import_data.csv ./main/fixtures/user-images/ ./main/fixtures/product-images/
```
