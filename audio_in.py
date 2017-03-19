# #Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
# #I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

# from array import array
# from struct import pack
# from sys import byteorder
# import copy
# import pyaudio
# import wave

# THRESHOLD = 500  # audio levels not normalised.
# CHUNK_SIZE = 1024
# SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
# FORMAT = pyaudio.paInt16
# FRAME_MAX_VALUE = 2 ** 15 - 1
# NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
# RATE = 44100
# CHANNELS = 1
# TRIM_APPEND = RATE / 4

# def is_silent(data_chunk):
#     """Returns 'True' if below the 'silent' threshold"""
#     return max(data_chunk) < THRESHOLD

# def normalize(data_all):
#     """Amplify the volume out to max -1dB"""
#     # MAXIMUM = 16384
#     normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
#                         / max(abs(i) for i in data_all))

#     r = array('h')
#     for i in data_all:
#         r.append(int(i * normalize_factor))
#     return r

# def trim(data_all):
#     _from = 0
#     _to = len(data_all) - 1
#     for i, b in enumerate(data_all):
#         if abs(b) > THRESHOLD:
#             _from = max(0, i - TRIM_APPEND)
#             break

#     for i, b in enumerate(reversed(data_all)):
#         if abs(b) > THRESHOLD:
#             _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
#             break

#     return copy.deepcopy(data_all[_from:(_to + 1)])

# def record():
#     """Record a word or words from the microphone and 
#     return the data as an array of signed shorts."""

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

#     silent_chunks = 0
#     audio_started = False
#     data_all = array('h')

#     while True:
#         # little endian, signed short
#         data_chunk = array('h', stream.read(CHUNK_SIZE))
#         if byteorder == 'big':
#             data_chunk.byteswap()
#         data_all.extend(data_chunk)

#         silent = is_silent(data_chunk)

#         if audio_started:
#             if silent:
#                 silent_chunks += 1
#                 if silent_chunks > SILENT_CHUNKS:
#                     break
#             else: 
#                 silent_chunks = 0
#         elif not silent:
#             audio_started = True              

#     sample_width = p.get_sample_size(FORMAT)
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
#     data_all = normalize(data_all)
#     return sample_width, data_all

# def record_to_file(path):
#     "Records from the microphone and outputs the resulting data to 'path'"
#     sample_width, data = record()
#     data = pack('<' + ('h' * len(data)), *data)

#     wave_file = wave.open(path, 'wb')
#     wave_file.setnchannels(CHANNELS)
#     wave_file.setsampwidth(sample_width)
#     wave_file.setframerate(RATE)
#     wave_file.writeframes(data)
#     wave_file.close()

# if __name__ == '__main__':
#     print("Wait in silence to begin recording; wait in silence to terminate")
#     record_to_file('demo.wav')
#     print("done - result written to demo.wav")

import pyaudio
import wave
import ignore_cerr
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

def record(filename):

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 4
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

if __name__ == '__main__':
    print get_txt("output.wav")