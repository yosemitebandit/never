
# mongo connection info
MONGO = {
    'db_name': 'never'
    , 'host': '127.0.0.1'
    , 'port': 11111
}

# flask server parameters
DEBUG = False
APP_HOST = '127.0.0.1'
APP_PORT = 8002
LOG_FILE = '/path/to/log/file'

# controls some sending/receiving info
MESSAGING = {
    # the incoming separator between body and delay
    'incoming_delimiter': '%'
    # determines what gets added to the start of outgoing messages
    , 'outgoing_preamble': ''
}

# gotta have a twilio account
TWILIO = {
    'account_sid': 'ACabcdefghijklmnopqrstuvwxyz'
    , 'auth_token': 'zyxwvutsrqponmlkjihgfedcba'
    , 'sent_from_number': '+1234567890'
}
