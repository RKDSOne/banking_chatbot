import json
import audio_in
import audio_out
from watson_developer_cloud import ConversationV1

def get_input(choice):
	
	if choice=='2': 
		print '\nEnter Something:',
		return raw_input()
	else:
		u_said = audio_in.get_txt('output.wav')
		print 'u said: ',u_said
		return u_said

def show_output(response,choice):

	print 'intent: ',response['intents']
	if len(response['output']['text'])>0:
		print 'output: ',response['output']['text'][0]
	
	if choice=='1' and len(response['output']['text'])>0:
			audio_out.make_speech(response['output']['text'][0],'output.wav')

if __name__ == '__main__':

	conversation = ConversationV1(
	    username='088d3149-9fda-430e-b5b3-6242776cc23a',
	    password='UUULVbiGwOIM',
	    version='2016-09-20')

	workspace_id = '5bc49e8e-c02b-4261-ad34-8397ca8e8beb'

	while True:

		print '\nEnter 1 to go keyless and 2 to continue using keyboard:',
		choice = raw_input()
		if choice=='2' or choice=='1': break

	user_in=get_input(choice)
	response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in})
	show_output(response,choice)

	while True:

		user_in=get_input(choice)
		response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in}, context=response['context'])
		show_output(response,choice)