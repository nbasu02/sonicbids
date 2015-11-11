import unittest
from models import db, NumberRecord
from views import display_difference, ErrorCode
from run import app
from config import Config
from flask.ext.sqlalchemy import SQLAlchemy
import json

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql+psycopg2://%(username)s:%(password)s@localhost/%(database_name)s' % {
                'username': Config.DB_USER,
                'password': Config.DB_PASSWORD,
                'database_name': Config.TEST_DATABASE_URI
            }
        app.config['TESTING'] = True

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestNumberRecord(BaseTest):
    def test_sum_of_squares_small(self):
        record = NumberRecord(number=3)
        self.assertEqual(
            record.sum_of_squares(),
            14
            )

    def test_sum_of_squares_bigger(self):
        record = NumberRecord(number=10)
        self.assertEqual(
            record.sum_of_squares(),
            385
            )

    def test_sum_of_squares_huge(self):
        # Model supports numbers > 100.  Frontend does not
        record = NumberRecord(number=101)
        self.assertEqual(
            record.sum_of_squares(),
            348551
            )

    def test_sum_of_squares_out_of_range(self):
        record = NumberRecord(number=0)
        self.assertIsNone(record.sum_of_squares())

    def test_square_of_sum_small(self):
        record = NumberRecord(number=3)
        self.assertEqual(
            record.square_of_sum(),
            36
            )

    def test_square_of_sum_bigger(self):
        record = NumberRecord(number=10)
        self.assertEqual(
            record.square_of_sum(),
            3025
            )

    def test_square_of_sum_huge(self):
        record = NumberRecord(number=101)
        self.assertEqual(
            record.square_of_sum(),
            26532801
            )

    def test_square_of_sum_out_of_range(self):
        record = NumberRecord(number=0)
        self.assertIsNone(record.square_of_sum())

    def test_set_value_small(self):
        record = NumberRecord(number=3)
        record.set_value()
        self.assertEqual(record.value, 22)

    def test_set_value_bigger(self):
        record = NumberRecord(number=10)
        record.set_value()
        self.assertEqual(record.value, 2640)

    def test_set_value_huge(self):
        record = NumberRecord(number=101)
        record.set_value()
        self.assertEqual(record.value, 26184250)

    def test_set_value_out_of_range(self):
        record = NumberRecord(number=0)
        record.set_value()
        self.assertIsNone(record.value)

class TestView(BaseTest):
    def test_display_difference_normal(self):
        response = self.app.get('/difference?number=11',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # check it was created
        record = db.session.query(NumberRecord).first()
        self.assertEqual(record.id, 1)
        self.assertEqual(record.number, 11)
        # because requests doesn't allow get requests to return json...
        output = json.loads(response.data)

        last_requested = record.last_requested
        expected = {
            'number': 11,
            'last_requested': last_requested.isoformat(),
            'occurences': 1,
            'value': 3850
        }
        self.assertDictEqual(output, expected)

        # And run a second time to see if the last_requested and
        # occurences changed
        response = self.app.get('/difference?number=11',
            content_type='application/json')

        output = json.loads(response.data)
        record = db.session.query(NumberRecord).first()

        # Check and make sure last_requested was updated
        self.assertNotEqual(record.last_requested, last_requested)
        last_requested = record.last_requested

        # Check the occurences count was updated, and last_requested is properly
        # displayed
        self.assertEqual(output['occurences'], 2)
        self.assertEqual(output['last_requested'], last_requested.isoformat())

    def test_display_difference_no_num(self):
        # No number inserted
        response = self.app.get('/difference')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        # Make sure a message and error code are correctly returned
        self.assertIn('message', output)
        self.assertEqual(output['code'], ErrorCode.NO_NUMBER)

    def test_display_difference_nan(self):
        # A non number is inserted
        response = self.app.get('/difference?number=abc')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        # Make sure a message and error code are correctly returned
        self.assertIn('message', output)
        self.assertEqual(output['code'], ErrorCode.NO_NUMBER)

    def test_display_difference_greater_than_100(self):
        # out of range
        response = self.app.get('/difference?number=101')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        # Make sure a message and error code are correctly returned
        self.assertIn('message', output)
        self.assertEqual(output['code'], ErrorCode.OUT_OF_RANGE)

    def test_display_difference_less_than_1(self):
        # out of range
        response = self.app.get('/difference?number=0')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.data)
        # Make sure a message and error code are correctly returned
        self.assertIn('message', output)
        self.assertEqual(output['code'], ErrorCode.OUT_OF_RANGE)
