import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CFRS_ENABLED = True
SECRET_KEY = 'can-you-hack-my-secret-key'


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kma:thudayne@localhost/modsec'
WHOOSH_BASE = os.path.join(basedir, 'search.db')
UPLOAD_FOLDER='msla/static/uploads'
ALLOWED_EXTENSIONS="[log]"
PER_PAGE = 100
