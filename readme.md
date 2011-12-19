This is a time capsule for your text messages.
Send a text to `(650) 830-0777` and, after some amount of time, you'll get the same message back.
No todo lists or otherwise mundane texts allowed - 
send your future self those curious, strange and fascinating moments you would otherwise forget.

Tell the time capsule when to resend the message by adding a special sequence at the end.
For example, send a message like 
`and the sun sank red through the hills and clouds %5d 8h 20m 7s`
and your words will return in five days, eight hours, twenty minutes and seven seconds.

Not all of those parameters are required - you could just add `%7d` 
at the end to see your note-to-self again in a week's time.
But take care - the spaces between the parameters after the `%` sign are required.

This is a Flask app built with Twilio and Mongo.
It was partially built at the tail end of Disrupt 2011 as 'never forget this text.'
Read more at http://yosemitebandit.com/projects


### setup
Here's how to setup your own server to receive and then resend texts:

 - you will need a twilio account with a verified phone number
 - point the incoming SMS callback to this app's twilio endpoint
   - expound..
 - make a virtualenv and install some dependencies
    
    ```
    $ virtualenv --no-site-packages /path/to/virtualenvs/never-lib
    $ pip install -E /path/to/virtualenvs/never-lib mongoengine
    $ pip install -E /path/to/virtualenvs/never-lib apscheduler
    $ pip install -E /path/to/virtualenvs/never-lib flask
    $ pip install -E /path/to/virtualenvs/never-lib requests
    ```

 - copy the sample never settings config file out of the repo and edit it with your settings
 - point an env var to your config file with:
    
    `
    $ set NEVER_SETTINGS=/path/to/config.py
    `

 - copy the sample supervisord config file out of the repo and edit it as well


### go-time
 - start mongo:
    
    `
    $ mongod --fork --logpath /path/to/mongodb.log --logappend --port 12345 --bind_ip 127.0.0.1
    `

 - use supervisord to start the flask server and supervisorctl to control it
    
    `
    $ supervisord -c /path/to/supervisord.conf
    `


### should-fix
 - mongo jobstore so jobs persist - test this separately; things are fishy..
 - flesh out the twilio setup section above
 - better error-handling..it's always better error-handling
 - test s,m,h,d
 - test messages over 140 chars
 - fabfile


### would-be-nice
 - get a random text from your past
 - tack on when the message was sent originally?
 - twilio takes a few seconds to send the text - account for this with an offset?
