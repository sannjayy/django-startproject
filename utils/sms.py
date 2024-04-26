from project.config import ENABLE_SMS_GATEWAY, SMS_GATEWAY_API_KEY, SMS_GATEWAY_HOST, SMS_GATEWAY_SENDER_ID
import requests, json, threading, urllib.parse


class SMSThread(threading.Thread):
    
    def __init__(self, link):
        self.link = link
        threading.Thread.__init__(self)

    def run(self):
        f = requests.get(self.link)
        # print('f -> ', f)
        # print('link -> ', self.link)
        resp = json.loads(f.text)
        # print(resp)


class SMSUtil:
    # Hit the SMS Gateway API
    @staticmethod
    def send_sms(mobile, msg, sender_id=SMS_GATEWAY_SENDER_ID):
        if ENABLE_SMS_GATEWAY:
            link = f"{SMS_GATEWAY_HOST}/api/push.json?apikey={SMS_GATEWAY_API_KEY}&route=trans&sender={sender_id}&mobileno={mobile}&text={urllib.parse.quote_plus(msg)}"
            SMSThread(link).start()
            
            # return resp.get('status') == 'success'
        print('-> SMS TRIGGERED BUT GATEWAY IS DISABLED <-')
        print(f'Message: {msg}')
    

