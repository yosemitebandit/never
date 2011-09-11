'''
interceptor.py
handling them texts
'''
import optparse
import simplejson as json

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

    client = TwilioRestClient(config['twilio']['account_sid'], config['twilio']['auth_token'])

    for message in client.sms.messages.list():
        print message
        print message.body
        
    



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

