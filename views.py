from run import app
from models import db, NumberRecord
from flask import request, jsonify
import datetime

@app.route('/difference')
def display_difference():
    '''
    Given a number through GET, returns json with following attrs:

    - number: the number given through GET
    - value: calculated value from number (see models.NumberRecord)
    - last_requested: datetime in isoformat of when record is updated
    - occurences: number of times this number has been queried
    '''
    number = int(request.args.get('number'))
    # TODO: if number is None
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
