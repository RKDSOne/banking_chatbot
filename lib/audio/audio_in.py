import pyaudio
import wave
import ignore_cerr
from watson_developer_cloud import SpeechToTextV1

def record(filename):

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = filename

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def get_txt(filename):

    record(filename)
    speech_to_text = SpeechToTextV1( 
        username='96c7b8f0-8894-4652-be04-dc665766d299', 
        password='lJDUI0ohri6U')
    with open(filename,'rb') as audio_file:
        return (speech_to_text.recognize(audio_file, content_type='audio/wav')['results'][0]['alternatives'][0]['transcript'])