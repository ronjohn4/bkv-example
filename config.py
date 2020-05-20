import os
import requests
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Hardcoded Config
    BAG = 'bkvtest'
    ADMINS = ['your-email@example.com']
    ROWS_PER_PAGE_FULL = 10
    ROWS_PER_PAGE_FILTER = 5
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Environment specific Config
    INSTANCE = os.environ.get('INSTANCE')  #This is the only env var that is env specific but never changes
    KEY1 = os.environ.get('KEY1') or 'Key1 Default Value'
    SECONDKEY = os.environ.get('SECONDKEY') or 'SecondKey Default Value'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess2a'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or None

    # Update Environment specific Config from BKV
    try:
        r = requests.get(f'http://127.0.0.1:5000/api/baginstance/{BAG}/{INSTANCE}')
    except:
        r = None

    if r and r.status_code == 200:
        kv_package = json.loads(r.text)
        if 'Key1' in kv_package:
            KEY1 = kv_package['Key1']
            os.environ['KEY1'] = KEY1
        if 'SecondKey' in kv_package:
            SECONDKEY = kv_package['SecondKey']
            os.environ['SECONDKEY'] = SECONDKEY
        if 'SECRET_KEY' in kv_package:
            SECRET_KEY = kv_package['SECRET_KEY']
            os.environ['SECRET_KEY'] = SECRET_KEY
        if 'DATABASE_URL' in kv_package:
            SQLALCHEMY_DATABASE_URI = kv_package['DATABASE_URL']
            os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        if 'LOG_TO_STDOUT' in kv_package:
            LOG_TO_STDOUT = kv_package['LOG_TO_STDOUT']
            os.environ['LOG_TO_STDOUT'] = LOG_TO_STDOUT
