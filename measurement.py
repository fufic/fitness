import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Numeric
import connectff
import zero_messeger.zero_messeger as zm
import json
import datetime
import pytz
import iso8601

class Weight(connectff.Base):
    __tablename__ = 'weight'

    id = Column(Integer, primary_key=True)
    current_weight = Column(Numeric(3,1))
    time = Column(DateTime)

    def __repr__(self):
        return "<Weight(%d, %d, %d)>" % (self.id, self.current_weight, self.time)


def add_weight_to_db(val):
    session = connectff.Session()
    weight = Weight(current_weight = val, time = datetime.datetime.utcnow())
    session.add(weight)    
    session.commit()

def list_weights():
    session = connectff.Session()
    for user in session.query(Weight):
        print(user.time, user.current_weight, user.id)

#2019-06-02T12:00:00+03:00'
def weight_by_date(date):
    session = connectff.Session()
    dtDate = iso8601.parse_date(date) #parse string to datetime object
    print(dtDate)
    #for user in session.query(Weight):
    #    print(user.time, user.current_weight, user.id)
    return 45.7

def tmpHandler(message):
    print("by tmpHandler")
    params = json.loads(message.decode())
    print("by tmpHandler")
    resp = {}
    if params['intent'] == 'set_weight':
        add_weight_to_db(params['val'])
        resp = {"success":True}
    elif params['intent'] == 'get_weight':
        weight = weight_by_date(params['date'])
        resp = {"success":True, "weight": weight}
    print("by tmpHandler",params)
    return json.dumps(resp).encode()

zmqReceiver = zm.Receiver('tcp://127.0.0.1:8088', tmpHandler)
zmqReceiver.Run()





















"""

ed_ = (name='ed', fullname='Edward Jones')

# ## slide::
# The "id" field is the primary key, which starts as None
# if we didn't set it explicitly.

print(ed_user.name, ed_user.fullname)
print(ed_user.id)






# the Session will *flush* *pending* objects
# to the database before each Query.
our_user = session.query(User).filter_by(name='ed').first()
our_user

# ## slide::
# the User object we've inserted now has a value for ".id"
print(ed_user.id)

# ## slide::
# the Session maintains a *unique* object per identity.
# so "ed_user" and "our_user" are the *same* object

ed_user is our_user

# ## slide::
# Add more objects to be pending for flush.

session.add_all([User(name='wendy',
                      fullname='Wendy Weathersmith'),
                 User(name='mary',
                      fullname='Mary Contrary'),
                 User(name='fred',
                      fullname='Fred Flinstone')])

# ## slide::
# modify "ed_user" - the object is now marked as *dirty*.

ed_user.fullname = 'Ed Jones'

# ## slide::
# the Session can tell us which objects are dirty...

session.dirty

# ## slide::
# and can also tell us which objects are pending...

session.new

# ## slide:: p i
# The whole transaction is committed.  Commit always triggers
# a final flush of remaining changes.

session.commit()
"""