"Return a dictionary of environment variable keyss and their values"
import environ
import os
from config.settings.base import BASE_DIR

import logging
logger = logging.Logger(__file__)

def get_env_dict(env_path):
    "Return a dictionary of environment variable keyss and their values"
    env = {}
    try:
        read_env = environ.Env()
        environ.Env.read_env(env_path)

        #debug
        if read_env('DEBUG') == 'True' or True:
            env['DEBUG'] = True
        elif read_env('DEBUG') == 'False' or False:
            env['DEBUG'] = False
    
        #secret keys
        env['SECRET_KEY'] = read_env('SECRET_KEY')

        #DB setting
        env['DB_NAME'] = read_env('DB_NAME')
        env['DB_USER'] = read_env('DB_USER')
        env['DB_PASS'] = read_env('DB_PASS')

    except environ.ImproperlyConfigured as e:
        logger.info('設定されていないkeyが設定されている: {}'.format(e))
        
    except Exception as e:
        logger.info('環境変数設定のエラー: {e}'.format(e))
    
    logger.debug("{}".format(env))
    return env
        

env_path = os.path.join(BASE_DIR, '.env')
env = get_env_dict(env_path)
print(env)