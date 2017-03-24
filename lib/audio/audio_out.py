import pyaudio
import wave
import ignore_cerr
from watson_developer_cloud import TextToSpeechV1


def play(filename):

	CHUNK = 1024
	wf = wave.open(filename, 'rb')

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
	data = wf.readframes(CHUNK)

	while len(data) > 0:
	    stream.write(data)
	    data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	p.terminate()

def make_speech(message,filename):

	text_to_speech = TextToSpeechV1(
	username='11fec8ca-d894-4ea7-a4c4-4d2a2da816c9',
	password='qYPENLNDbaPq')

	with open(filename,'wb') as audio_file:
		audio_file.write(text_to_speech.synthesize(message,accept='audio/wav',voice="en-US_AllisonVoice"))
	
	play(filename)