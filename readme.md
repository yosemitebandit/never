## never
never forget this text; cause I send it to you again. better name: smstimecapsule


### go-time
 - start mongo:

  mongod --fork --logpath /var/log/mongodb/mongodb.log --logappend --port 12345 --bind_ip 127.0.0.1

 - use supervisor to start the interceptor process, this gathers up the texts and stores them in mongo
 - use supervisor to start the communicator process, this is a little cron-ish job that sends back the texts


### setup
 - make a virtualenv and install some dependencies

    $ virtualenv --no-site-packages ~/virtualenvs/never-lib
    $ pip install -E ~/virtualenvs/never-lib pymongo 
    $ pip install -E ~/virtualenvs/never-lib twilio

 - move the supervisord config file somewhere safe, edit it to your satisfaction
 - move the never config file somewhere safe, edit it to your satisfaction


### mongo
 - created: timestamp
 - resent: bool
 - message: text n stuff
 - send_at_this_time: timestamp

double check your mongo version; gotta have 2.0


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

 - fyi, you can GET things like https://api.twilio.com/2010-04-01/Accounts/[APP-ID-HERE]/SMS/Messages.json?pages=2
   - sign in with your app ID and secret
   - so maybe it would be better to forgo the python lib and use requests
   - pagination seems broken in the python lib

