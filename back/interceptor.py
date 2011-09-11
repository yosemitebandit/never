'''
interceptor.py
handling them texts
'''
import optparse
import time
import sys
import simplejson as json
import threading

import pymongo

from twilio.rest import TwilioRestClient
# load up a config file that contains an API key

def main():
    parser = create_parser()
    (opts, args) = parser.parse_args()
    check_arg_validity(parser, opts)    # check that the args are valid; will exit and print usage if not


    # import config file with info on mongo connections, redwood clusters, and remotes
    f = open(opts._pathToConfig, 'r')
    config = json.loads(f.read())
    f.close()

        
    # start a thread for each cluster's scraper;  maybe add more later
    threadPool = {}
    key = 'thread1'
    threadPool[key] = threading.Thread(target=worker, args=(config,))
    threadPool[key].start()
    
    # continuously check that the threads are still kicking
    while(1):   
        for key in threadPool:
            if not threadPool[key].is_alive():
                thread_print('*error, restarting %s thread' % key)
                threadPool[key] = threading.Thread(target=worker, args=(config,))
                threadPool[key].start()

        time.sleep(10)

def worker(config):
    ''' gets threaded..scrapes the twilio sms messages
    '''
    thread_print('starting thread')
    client = TwilioRestClient(config['twilio']['account_sid'], config['twilio']['auth_token'])

    while(1):
        messages = []
        for message in client.sms.messages.list():
            if message.direction == 'inbound':
                # or maybe it's: 'oh hai %1d 3h 5m'
                chunks = message.body.split('%')
                if len(chunks) != 2: 
                    print 'punt'
                    continue   # best punter

                specified_message = chunks[0]
                specified_time = chunks[1]
                seconds_till_blastoff = convert_sms_input_to_seconds(specified_time)
                print '\n\n'
                print 'incoming: %s' % specified_time 
                print 'seconds: %d' % seconds_till_blastoff

                date_created_seconds = time.mktime(time.strptime(message.date_created, '%a, %d %b %Y %H:%M:%S +0000'))
                calculated_reply_time = date_created_seconds + seconds_till_blastoff

                messages.append({
                    'body': message.body
                    , 'from': message.from_
                    , 'sid': message.sid
                    , 'date_created_seconds': date_created_seconds
                    , 'calculated_reply_time': calculated_reply_time
                    , 'interpreted_time': specified_time
                    , 'message': specified_message.strip()
                    , 'was_sent': False
                })
        
        
        # check to see if we've already added this message to mongo, yikes..
        cxn = pymongo.Connection(config['mongo']['host'], int(config['mongo']['port']))
        db = cxn[config['mongo']['dbName']]
        for m in messages:
            # if sid not in place, insert into mongo
            query = {'sid': m['sid']}
            returnFields = {'_id': True}
            
            matchingDocs = list(db['messages'].find(query, returnFields).limit(1))
            if matchingDocs:
                # already got it
                continue
            else:
                db['messages'].insert(m)

        
        time.sleep(5)


def convert_sms_input_to_seconds(specified_time):
    '''convert an input: 1d 3h 5m
    '''
    specified_time.strip()
    chunks = specified_time.split()
    days, hours, minutes = None, None, None
    for chunk in chunks:

        if chunk.find('d') != -1:
            days = int(chunk[0:-1])   # all but the letter
        elif chunk.find('h') != -1:
            hours = int(chunk[0:-1])
        elif chunk.find('m') != -1:
            minutes = int(chunk[0:-1])
    seconds = 0
    if days:
        seconds += days*24.*60.*60
    if hours:
        seconds += hours*60.*60.
    if minutes:
        seconds += minutes*60.
    return seconds


def thread_print(message):
    _now = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    sys.stdout.write(_now + ' - ' + message + '\n')


'''Parser-related
'''
def check_arg_validity(parser, opts):
    if not opts._pathToConfig:
        argument_error(['--config'], parser)


def argument_error(missingArguments, parser):
    for arg in missingArguments:
        print 'argument "%s" missing.' % arg
    print_usage()
    #parser.print_help()
    print 'exiting.'
    exit(-1)


def create_parser():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', help='path to config file', dest='_pathToConfig', action='store', metavar='<pathToConfig>')

    return parser


def print_usage():
    print '''
usage:
  $ python interceptor.py --config <configFilePath>
          '''


if __name__ == '__main__':
    main()

