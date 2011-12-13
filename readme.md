## never
Send this service a text and, after some amount of time, you'll get the same message back.
It's an SMS time capsule (formerly known as never-forget-this-text).
Tell it when to resend the message by adding `%5d 8h 20m 7s` at the end
and the message will return in five days, eight hours, twenty minutes and seven seconds.
Not all of those parameters are required - you could just ask for `%7d`
to see your note-to-self again in a week's time.
But take care - the spaces between the parameters are required.

This is a Flask app built with Twilio and Mongo.
Read more at http://yosemitebandit.com/projects


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
 - mongo jobstore so jobs persist
 - flesh out the twilio setup section above
 - better error-handling..it's always better error-handling
 - test s,m,h,d
 - add a fabfile


### would-be-nice
 - get a random text from your past sends
 - preamble that says when the message was sent?
 - twilio takes a few seconds to send the text -- account for this offset?
