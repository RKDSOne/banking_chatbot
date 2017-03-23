import json
import os
from lib import audio_in
from lib import audio_out
from lib import in_filter
from lib import out_filter
from watson_developer_cloud import ConversationV1

def get_input(choice,node):
	
	if choice=='2': 
		print '\nEnter Something:',
		inp=raw_input()
		if node=='balance check': in_filter.acc1=inp
		return in_filter.filter(inp,node)
	else:
		u_said = audio_in.get_txt(os.getcwd()+'/res/output.wav')
		print 'u said: ',u_said
		if node=='balance check': in_filter.acc1=u_said
		u_said = in_filter.filter(u_said,node)
		return u_said

def show_output(response,choice):

	print 'intent: ',response['intents']
	print 'node: ',response['output']['nodes_visited'][0]
	if len(response['output']['text'])>0:
		for i in response['output']['text']:
			print 'output: ',out_filter.filter(i,response['output']['nodes_visited'][0],in_filter.acc1)
	
	if choice=='1' and len(response['output']['text'])>0:
			for i in response['output']['text']:
				audio_out.make_speech(out_filter.filter(i,response['output']['nodes_visited'][0],in_filter.acc1),os.getcwd()+'/res/output.wav')

if __name__ == '__main__':

	conversation = ConversationV1(
	    username='088d3149-9fda-430e-b5b3-6242776cc23a',
	    password='UUULVbiGwOIM',
	    version='2016-09-20')

	workspace_id = '5888d51f-cac8-4dce-8ff4-dd432cf5b3a7'

	while True:

		print '\nEnter 1 to go keyless and 2 to continue using keyboard:',
		choice = raw_input()
		if choice=='2' or choice=='1': break

	user_in=get_input(choice,'')
	response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in})
	show_output(response,choice)

	while True:

		user_in=get_input(choice,response['output']['nodes_visited'][0])
		if user_in=='-program_end-': break
		response = conversation.message(workspace_id=workspace_id, message_input={'text': user_in}, context=response['context'])
		show_output(response,choice)