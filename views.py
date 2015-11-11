from run import app
from models import db, NumberRecord
from flask import request, jsonify
import datetime

class ErrorCode(object):
    NO_NUMBER = 1
    OUT_OF_RANGE = 2

@app.route('/difference')
def display_difference():
    '''
    Given a number through GET, returns json with following attrs:

    - number: the number given through GET
    - value: calculated value from number (see models.NumberRecord)
    - last_requested: datetime in isoformat of when record is updated
    - occurences: number of times this number has been queried

    If any errors occur, a JSON with the following content will return:
    - message: explanation of error
    - code: associated error code
    '''
    try:
        number = int(request.args.get('number'))
    except TypeError:
        return jsonify(**{
            'message': 'Please provide a number',
            'code': ErrorCode.NO_NUMBER
            }
        )

    if not (1 <= number <= 100):
        return jsonify(**{
            'message': 'Number must be in the range of 1 to 100',
            'code': ErrorCode.OUT_OF_RANGE
            }
        )

    record = db.session.query(NumberRecord).filter(
        NumberRecord.number==number).first()
    if not record:
        record = NumberRecord(number=number, occurences=0)
        record.set_value()
        db.session.add(record)

    record.last_requested = datetime.datetime.now()
    record.occurences += 1
    # This feels dirty
    # Would be better to incorporate something like ZopeTransactionManager...
    db.session.commit()

    return jsonify(**record.to_json())
