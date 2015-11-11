from run import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

class NumberRecord(Base):
    __tablename__ = 'number_record'

    # last time this object is requested by frontend
    last_requested = db.Column(db.DateTime)
    # 1 <= number <= 100
    # is used to calculate value
    number = db.Column(db.Integer)
    # is the difference between sum of squares between 1 and number
    # and square of sum of numbers between 1 and number
    value = db.Column(db.Integer)
    # number of times this object is requested
    occurences = db.Column(db.Integer)

    def sum_of_squares(self):
        '''
        Find sum of all squares from 1 to self.number
        i.e. 1^2 + 2^2 + ... + self.number^2
        Uses the formula found here:
        www.trans4mind.com/personal_development/mathematics/series/sumNaturalSquares.htm
        The formula is (n^3)/3 + (n^2)/2 + n/6 == sum of first n natural numbers squared
        '''

        formula = lambda num: int(pow(num, 3)/3.0 + pow(num, 2)/2.0 + num/6.0)
        return formula(self.number)

    def square_of_sum(self):
        '''
        Find square of sum of 1 to self.number
        '''

        formula = lambda num: pow((num*(num+1))/2, 2)
        return formula(self.number)

    def set_value(self):
        '''
        Sets self.value equal to the difference between
        the square of the sum of all numbers up to self.number and
        the sum of all squares up to self.number
        '''

        self.value = self.square_of_sum() - self.sum_of_squares()

    def to_json(self):
        return {
            'number': self.number,
            'value': self.value,
            'occurences': self.occurences,
            'last_requested': self.last_requested.isoformat()
        }

# To set up the database
if __name__ == '__main__':
    import os
    from subprocess import call
    from config import Config

    # Now to do some db setup
    dummy_env = os.environ.copy()
    # normally this sort of step would be done on identical environments, but that's not
    # guaranteed here
    dummy_env['PGPASSWORD'] = Config.DB_PASSWORD

    call('dropdb %(database_name)s -U %(username)s' % {
        'username': Config.DB_USER,
        'database_name': Config.DATABASE_URI
        },
        shell=True, env=dummy_env)
    call('dropdb %(database_name)s -U %(username)s' % {
        'username': Config.DB_USER,
        'database_name': Config.TEST_DATABASE_URI
        },
        shell=True, env=dummy_env)
    call('createdb %(database_name)s -U %(username)s' % {
        'username': Config.DB_USER,
        'database_name': Config.DATABASE_URI
        },
        shell=True, env=dummy_env)
    call('createdb %(database_name)s -U %(username)s' % {
        'username': Config.DB_USER,
        'database_name': Config.TEST_DATABASE_URI
        },
        shell=True, env=dummy_env)

    db.create_all()
