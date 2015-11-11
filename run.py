from config import Config
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://%(username)s:%(password)s@localhost/%(database_name)s' % {
        'username': Config.DB_USER,
        'password': Config.DB_PASSWORD,
        'database_name': Config.DATABASE_URI
    }

if __name__ == '__main__':
    from models import *
    from views import *
    app.run(debug=True)
