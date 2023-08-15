import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone 
from project.settings.config import EMAIL_RESEND_ATTEMPT, EMAIL_RESEND_TIME, SMS_RESEND_ATTEMPT, SMS_RESEND_TIME
from django.utils.http import urlsafe_base64_decode
import string, random, secrets

# Age Calculate View
def calculate_age(date):
    today = datetime.date.today()
    if date:
        return today.year - date.year - ((today.month, today.day) < (date.month, date.day))


# Check Time Difference
def time_difference(from_time):
    '''Calculate the difference between two times on the same date.

    Args:
        date_time [str]: datetime
    '''
    datetime_now = timezone.localtime(timezone.now())
    current_time = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    current_time = parse_datetime(current_time)
    from_time = parse_datetime(from_time)
    difference = current_time - from_time 
    # minutes = difference.total_seconds() / 60
    # minutes = difference.seconds / 60
    minutes = divmod(difference.seconds, 60) 
    # print('Total difference in minutes: ', minutes[0], 'minutes', minutes[1], 'seconds')
    return minutes[0]



class HandleUserCount:
    """Handle User Counts

    - [verification_sent]:
        for email counting user verification resend
    - [forgot_pw_sent]:
        for email counting user forgot password resend
    - [sms_verification_sent]:
        for sms counting user verification resend
    - [sms_forgot_pw_sent]:
        for sms counting user forgot password resend

    """
    def __init__(self, user) -> None:
        self.user = user
        datetime_now = timezone.localtime(timezone.now())
        self.date = datetime_now.strftime("%Y-%m-%d")
        self.datetime = datetime_now.strftime("%Y-%m-%d %H:%M:%S")

        # If not data on db then create
        if not self.user.counts or not self.user.counts.get('date'):
            self.reset()
        

    # Reset All Counts
    def reset(self):
        """
        Create or Reset Counts
        """
        # cls = self.__class__
        self.user.counts = {
            'date': self.date,
            'verification_sent': {'count': 0, 'updated_at': self.datetime},
            'forgot_pw_sent': {'count': 0, 'updated_at': self.datetime},
            'sms_verification_sent': {'count': 0, 'updated_at': self.datetime},
            'sms_forgot_pw_sent': {'count': 0, 'updated_at': self.datetime},
        }
        return bool(self.user.save())


    @property  
    def is_updated_today(self):
        # # last_count_update_date = parse_datetime(self.user.counts.get('date'))        
        return self.date == self.user.counts.get('date')

    # Check Email Resend Parameters
    def has_email_verification_sent_limit(self):        
        verification_sent = self.user.counts.get('verification_sent')
        updated_at = verification_sent.get('updated_at')
        current_count = verification_sent.get('count')
        if current_count < EMAIL_RESEND_ATTEMPT:
            return self._handle_if_has_verification_sent_limit(
                updated_at,
                EMAIL_RESEND_TIME,
                'verification_sent',
                'Check your email.',
            )
        elif not self.is_updated_today:
            self.reset()
            return self.increment_count_and_return('verification_sent', 'Check your email.')
        else:
            return self.error_response('Limit end for today try tomorrow or contact customer care.')
        
    # Check SMS Resend Parameters
    def has_sms_verification_sent_limit(self):        
        sms_verification_sent = self.user.counts.get('sms_verification_sent')
        updated_at = sms_verification_sent.get('updated_at')
        current_count = sms_verification_sent.get('count')
        if current_count < SMS_RESEND_ATTEMPT:
            return self._handle_if_has_verification_sent_limit(
                updated_at,
                SMS_RESEND_TIME,
                'sms_verification_sent',
                'Check your inbox.',
            )
        elif not self.is_updated_today:
            self.reset()
            return self.increment_count_and_return('sms_verification_sent', 'Check your inbox.')
        else:
            return self.error_response('Limit end for today try tomorrow or contact customer care.')

    # Handle if `has_email_verification_sent_limit` and `has_sms_verification_sent_limit`
    def _handle_if_has_verification_sent_limit(self, updated_at, arg1, arg2, arg3):
        diff = time_difference(updated_at)
        if diff < int(arg1):
            return self.error_response(f'Wait for {arg1} minutes.')
        return self.increment_count_and_return(arg2, arg3)

    # Increment in database and return success
    def increment_count_and_return(self, element, message):
        current_count = self.user.counts.get(element).get('count')
        self.user.counts[element] = {'count': (current_count + 1), 'updated_at': self.datetime}
        self.user.save()
        return {
            'has_error':False,
            'detail': message
        }

    # return error
    def error_response(self, message):
        return {
            'has_error': True,
            'detail': message
        }


def isBase64(uidb64):
    try:
        urlsafe_base64_decode(uidb64)
        return True
    except Exception:
        return False


def random_code_generator(length):
    # str1 = ''.join(random.choice(string.ascii_letters) for _ in range(letter_count)) + ''.join(random.choice(string.digits) for _ in range(digit_count))

    # sam_list = list(str1) # it converts the string to list.  
    # random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
    # return ''.join(sam_list)
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length)) 

