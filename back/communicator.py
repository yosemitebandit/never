'''
communicator.py
sendin them texts
'''
import optparse
import time
import sys
import simplejson as json

import pymongo
from twilio.rest import TwilioRestClient
# load up a config file that contains an API key

def main():
    parser = create_parser()
    (opts, args) = parser.parse_args()
    check_arg_validity(parser, opts)    # check that the args are valid; will exit and print usage if not

    # import config file with info on mongo connections and auth and whatnot
    f = open(opts._pathToConfig, 'r')
    config = json.loads(f.read())
    f.close()
        
    client = TwilioRestClient(config['twilio']['account_sid'], config['twilio']['auth_token'])

    cxn = pymongo.Connection(config['mongo']['host'], int(config['mongo']['port']))
    db = cxn[config['mongo']['dbName']]
    while(1):
        # find all the messages that haven't been sent and are marked to be sent at a time earlier than now
        query = {'$and': [{'was_sent': False}, {'calculated_reply_time': {'$lte': time.mktime(time.gmtime())}} ]} 
        returnFields = {'_id': False}

        unsentMessages = list(db['messages'].find(query, returnFields))
        print unsentMessages
        for m in unsentMessages:
            print m['calculated_reply_time'] - time.mktime(time.gmtime())
            
            sent_message = client.sms.messages.create(
                            to = m['from']
                            , from_ = config['twilio']['sent_from_number']
                            , body = m['message'])
            

            # flip that bit
            query = {'sid': m['sid']}
            returnFields = {'_id': True}
            db['messages'].update(query, {'$set': {'was_sent': True}})
        
        time.sleep(10)


def formatted_print(message):
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

