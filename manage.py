#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from script.get_env_dict import env

def main():
    if env['DEBUG'] == True:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
        
    elif env['DEBUG'] == False:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development') ## TODO : 本番環境に関する設定は、別途記載 

        
    from django.db.backends.mysql.schema import DatabaseSchemaEditor
    DatabaseSchemaEditor.sql_create_table += " ROW_FORMAT=DYNAMIC"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
