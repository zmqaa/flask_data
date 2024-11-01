import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))   #D:\final\study\data_flask
class Config(object):
    SECRET_KEY = 'zmq'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])