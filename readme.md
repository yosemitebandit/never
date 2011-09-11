## never
never forget this text
cause I send it to you again
yeah.
smstimecapsule

## back
receiver takes an incoming text and stores it in mongo

### mongo
  created: timestamp
  resent: bool
  message: text n stuff
  send_at_this_time: timestamp

starting: /usr/bin/mongod --fork --logpath /var/log/mongodb/mongodb.log --logappend --port 12345 --bind_ip 127.0.0.1


### twilio..come on man
{
    'body': 'whattup',
    'status': 'sent',
    'direction': 'outbound-reply',
    'parent': <twilio.rest.resources.SmsMessagesobjectat0x10108a9d0>,
    'date_updated': 'Sun,11Sep201113:46:49+0000',
    'price': '-0.01000',
    'auth': ('bla','bla'),
    'name': 'bla',
    'base_uri': 'https: //api.twilio.com/2010-04-01/Accounts/bla/SMS/Messages',
    'account_sid': 'bla',
    'to': '+bla',
    'sid': 'bla',
    'date_sent': 'Sun,11Sep201113:46:49+0000',
    'date_created': 'Sun,11Sep201113:46:48+0000',
    'from_': '+bla',
    'api_version': '2010-04-01'
}

fyi, you can GET things like https://api.twilio.com/2010-04-01/Accounts/[APP-ID-HERE]/SMS/Messages.json?pages=2
and sign in with your app ID and secret

