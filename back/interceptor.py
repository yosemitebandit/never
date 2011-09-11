'''
interceptor.py
handling them texts
'''
import optparse
import time
import sys
import simplejson as json
import threading

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
        print dir(client.sms.messages)

        for message in client.sms.messages.list():
            if message.direction == 'inbound':
                print message.body
                print message.from_
        
        time.sleep(5)
    

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

