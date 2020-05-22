import os
import requests
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class RemoteConfig():
    def __init__(self):
        BAG = 'bkvtest'
        INSTANCE = os.environ.get('INSTANCE')  # This is the only Static env var that is env specific

        self.kv_package1 = None
        try:
            r = requests.get(f'http://127.0.0.1:5000/api/baginstance/{BAG}/{INSTANCE}')
            if r.status_code == 200:
                self.kv_package = json.loads(r.text)
        except:
            pass

    def getconfig(self, key):
        if key in self.kv_package:
            return self.kv_package[key]
        else:
            return None


class Config(object):
    rc = RemoteConfig()

    # Environment values that are local only
    ADMINS = ['your-email@example.com']
    ROWS_PER_PAGE_FULL = 10
    ROWS_PER_PAGE_FILTER = 5
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Environment variables that may be managed remotely using BKV
    KEY1 = rc.getconfig('KEY1') or os.environ.get('KEY1') or 'Key1 Default Value'
    SECONDKEY = rc.getconfig('SECONDKEY') or os.environ.get('SECONDKEY') or 'SecondKey Default Value'
    SECRET_KEY = rc.getconfig('SECRET_KEY') or os.environ.get('SECRET_KEY') or 'you-will-never-guess2a'
    LOG_TO_STDOUT = rc.getconfig('LOG_TO_STDOUT') or os.environ.get('LOG_TO_STDOUT') or None
