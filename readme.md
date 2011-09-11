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
{'body': 'whattup', 'status': 'sent', 'direction': 'outbound-reply', 'parent': <twilio.rest.resources.SmsMessages object at 0x10108a9d0>, 'date_updated': 'Sun, 11 Sep 2011 13:46:49 +0000', 'price': '-0.01000', 'auth': ('AC8e2d834f465243a6a80bfbca7033c99c', 'afcba56a5c43868e29f9b08dfe198485'), 'name': 'SM99bd5ab7557a4daa8e931b1752dbaa38', 'base_uri': 'https://api.twilio.com/2010-04-01/Accounts/AC8e2d834f465243a6a80bfbca7033c99c/SMS/Messages', 'account_sid': 'AC8e2d834f465243a6a80bfbca7033c99c', 'to': '+16506906913', 'sid': 'SM99bd5ab7557a4daa8e931b1752dbaa38', 'date_sent': 'Sun, 11 Sep 2011 13:46:49 +0000', 'date_created': 'Sun, 11 Sep 2011 13:46:48 +0000', 'from_': '+17037943748', 'api_version': '2010-04-01'}
{'body': 'Gday', 'status': 'received', 'direction': 'inbound', 'parent': <twilio.rest.resources.SmsMessages object at 0x10108a9d0>, 'date_updated': 'Sun, 11 Sep 2011 13:46:48 +0000', 'price': '-0.01000', 'auth': ('AC8e2d834f465243a6a80bfbca7033c99c', 'afcba56a5c43868e29f9b08dfe198485'), 'name': 'SMf626903299a01007b5dc37599ee71772', 'base_uri': 'https://api.twilio.com/2010-04-01/Accounts/AC8e2d834f465243a6a80bfbca7033c99c/SMS/Messages', 'account_sid': 'AC8e2d834f465243a6a80bfbca7033c99c', 'to': '+17037943748', 'sid': 'SMf626903299a01007b5dc37599ee71772', 'date_sent': 'Sun, 11 Sep 2011 13:46:48 +0000', 'date_created': 'Sun, 11 Sep 2011 13:46:48 +0000', 'from_': '+16506906913', 'api_version': '2010-04-01'}

