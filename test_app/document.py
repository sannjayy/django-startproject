from datetime import datetime
from mongoengine import Document, StringField, DictField, DateTimeField, IntField
from django.utils import timezone, dateformat
import pytz

def get_timestamp():
    # Define the IST timezone
    ist_timezone = pytz.timezone('Asia/Kolkata')  # Indian Standard Time

    # Get the current UTC time
    utc_now = datetime.now(pytz.utc)
    # Convert UTC time to IST
    ist_now = utc_now.astimezone(ist_timezone)
    # print('dad -> ', ist_now)
    return ist_now.strftime('%Y-%m-%d %H:%M:%S')
    
    

class TestLog(Document):
    company_code = StringField(required=True)
    user = StringField()
    message = StringField()
    data = DictField()
    created_at = DateTimeField()