from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://%(username)s:%(password)s@localhost/neilbasu_sonicbids' % {
        'username': Config.DB_USER,
        'password': Config.DB_PASSWORD,
    }

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
