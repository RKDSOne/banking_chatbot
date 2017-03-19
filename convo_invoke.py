import json
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
    username='8beb1154-3a4f-4b87-80cf-8dec9e1633d8',
    password='UufsQDFiulLE',
    version='2016-09-20')

workspace_id = 'c9c049e2-9a62-42d8-b8aa-5e80d8fb8406'

user_in = raw_input('Enter Something: ')
response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in})
print 'intent: ',response['intents']
print 'output: ',response['output']['text'],'\n'

while True:

	user_in = raw_input('Enter Something: ')
	response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in}, context=response['context'])
	print 'intent: ',response['intents']
	print 'output: ',response['output']['text'],'\n'
