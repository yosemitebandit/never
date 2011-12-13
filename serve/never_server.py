#!/usr/bin/env python
'''
never_server.py
twilio endpoints and managing the sending of outgoing messages
'''
import datetime

from apscheduler.scheduler import Scheduler
import flask
from mongoengine import *
import requests

app = flask.Flask(__name__)
app.config.from_envvar('NEVER_SETTINGS')

# pull out the delimiter
delimiter = app.config['MESSAGING']['incoming_delimiter']

# mongoengine connection
connect(app.config['MONGO']['db_name']
    , host=app.config['MONGO']['host']
    , port=int(app.config['MONGO']['port']))

# start the job scheduler
scheduler = Scheduler()
scheduler.start()


''' twilio endpoints
'''
@app.route('/api/1/sms/incoming', methods=['POST'])
def incoming_sms():
    ''' twilio posts data here when a text message is received
    see http://www.twilio.com/docs/api/twiml/sms/twilio_request
    '''
    if flask.request.form['AccountSid'] != app.config['TWILIO']['account_sid']:
        flask.abort(401)  # not authorized

    # calculate when to resend this text
    # extract the delay section, demarcated by the delimiter
    parts = flask.request.form['Body'].split(delimiter)
    if len(parts < 2):
        # no delimiter detected
        flask.abort(400)
        # should send some error message back as sms
    else:
        # the delay should be the last bit
        delay_in_seconds = _convert_delay_to_seconds(parts[-1])

        # save the sms in mongo
        try: 
            sms = SMS_Message(
                body = flask.request.form['Body']
                , has_been_resent = False
                , received_at = datetime.datetime.utcnow()
                # assumes the twilio callback is quick so time.time() is valid
                , resend_at = datetime.datetime.utcfromtimestamp(
                    time.time() + delay_in_seconds)
                , sender = flask.request.form['From']
                , twilio_sms_id = flask.request.form['SmsSid'])
            sms.save()
        except:
            # something didn't validate
            flask.abort(400)

        # schedule the sms to be sent at some time
        scheduler.add_date_job(scheduled_sms_send, sms.resend_at, [sms.id])

        flask.render_template('incoming_sms_reply.xml')


''' utilities
'''
def scheduled_sms_send(message_id):
    ''' scheduler calls this function to send out a specific message
    '''
    # query for the message
    message = SMS_Message.objects(id=message_id)[0]
    # strip out the specified delay from the body
    last_percent = len(sms.body) - sms.body[::-1].find(delimiter)
    outgoing_body = sms.body[0:last_percent - 1]
    # add a preamble..uh, later
    # fire off the message
    result = _send_sms(message.sender, outgoing_body)

    if result:
        message.has_been_resent = True
        message.save()


def _send_sms(to, body):
    ''' sending sms messages using twilio's rest api
    http://www.twilio.com/docs/api/rest/sending-sms
    '''
    request = {
        'From': app.config['TWILIO']['sent_from_number']
        , 'To': to
        , 'Body': body
        #, 'StatusCallback': ''  # reports sent/failed
    }

    endpoint = 'https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages'
        % app.config['TWILIO']['account_sid']

    r = requests.post(endpoint, data=request)
    if r.status_code == 200:
        return True
    else:
        return False


def _convert_delay_to_seconds(message):
    ''' message is of the form '5d 6h 1m 10s' 
    return the equivalent number of seconds
    '''
    message.strip()
    time_parts = message.split()
    days, hours, minutes, seconds = 0, 0, 0, 0

    for part in time_parts:                                                       
        if part.find('d') != -1:                                              
            days = int(part[0:-1])   # recover all the numerical pieces except the letter
        elif part.find('h') != -1:                                            
            hours = int(part[0:-1])                                           
        elif part.find('m') != -1:                                            
            minutes = int(part[0:-1])                                         
        elif part.find('s') != -1:                                            
            seconds += int(part[0:-1])                                        
    
    if days:                                                                   
        seconds += days*24.*60.*60                                             
    if hours:                                                                  
        seconds += hours*60.*60.                                               
    if minutes:                                                                
        seconds += minutes.*60.                                                 
    return seconds  


''' mongoengine models
'''
class SMS_Message(Document):
    ''' messages sent in to the service 
    '''
    body = StringField(required=True)
    has_been_resent = BooleanField(required=True)
    received_at = DateTimeField(required=True)
    resend_at = DateTimeField(required=True)
    sender = StringField(required=True)  # phone number
    twilio_sms_id = StringField(required=True)  # twilio's id


if __name__ == '__main__':
    app.run(host=app.config['APP_SERVER']['host']
        , port=int(app.config['APP_SERVER']['port']))
