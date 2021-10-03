from twilio.rest import Client

# The account SID and Auth Token from twilio.com/console
# This is insecure - see http://twil.io/secure

account_sid = 'AC1f9f9e3e72a7f460c853b29368d78b2c'
auth_token = '2b95e2c50dd56728ea30adf40b6dbd87'
client = Client(account_sid, auth_token)

call_to_num = '+17656375965'
call_from_num = '+12817667765'

message = '<Response></Response>'

call = client.calls.create(twiml=message, to=call_to_num, from_=call_from_num)

print(call.sid)
