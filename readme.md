## never
never forget this text, cause I'm gonna send it to you again. 
this should really be called 'smstimecapsule'


### setup
 - you will need a twilio account with a verified phone number
 - you will need to point the incoming SMS callback to this app
   - expound..
 - make a virtualenv and install some dependencies

    $ virtualenv --no-site-packages /path/to/virtualenvs/never-lib
    $ pip install -E /path/to/virtualenvs/never-lib mongoengine
    $ pip install -E /path/to/virtualenvs/never-lib apscheduler
    $ pip install -E /path/to/virtualenvs/never-lib flask
    $ pip install -E /path/to/virtualenvs/never-lib requests
 
 - copy the sample never settings config file out of the repo and edit it with your settings
 - point an env var to your config file with:
 
 ```
 set NEVER_SETTINGS=/path/to/config.py
 ```
 - copy the sample supervisord config file out of the repo and edit it as well


### go-time
 - start mongo:

    $ mongod --fork --logpath /path/to/mongodb.log --logappend --port 12345 --bind_ip 127.0.0.1
 
 - use supervisord to start the flask server


### should-fix
 - flesh out the twilio setup section above
 - better error-handling..it's always better error-handling


### would-be-nice
 - get a random text from your past sends
 - send/receive from different numbers
