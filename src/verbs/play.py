#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import PyAudio which is cross platform and uses portaudio libraries
# brew install port audio #  or find out your distros method of installation
import time
import json
import subprocess
import pyaudio
from queue import Queue
from threading import Thread
from vosk import Model, KaldiRecognizer


P = pyaudio.PyAudio()
# Initial a Meesages quqe to test if we have input
MESAGES = Queue()
RECORDINGS = Queue()

# Set the microphone to None to be set by the program
MIC = None

# Set some defaults for our sound - don't worry too much about this, it is a
# deep subject around sound itself and capturing these waves. Most microphones
# will be mono which is all we really need
CHANNELS = 1
# Quality of your recording (this will tax your computer resources)
FRAME_RATE = 16000
# Recording time length
RECORD_SECONDS = 20
# Audio format
AUDIO_FORMAT = pyaudio.paInt16
# Sample size
SAMPLE_SIZ = 2



# A method to list all devices with audio capabilites including
# monitors, webcams, microphones and speakers etc
def get_audio_device_info():
    number = P.get_device_count()
    print("There are " + str(number) + " devices attached!")
    devices = {}
    for i in range(number):
        dev = P.get_device_info_by_index(i)
        devices[dev['name']] = dev
    return devices


# A method to take chunks and define how often we are going to read
# from this microphone
def record_microphone(index, chunk=1026):
    # Create a stream from the mic
    stream = P.open(
        format=AUDIO_FORMAT,
        channel=CHANNELS,
        rate=FRAME_RATE,
        input=True,
        index=index,
        framer_per_buffer=chunk
    )

    frames = []

    while not messages.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []

    stream.stop_stream()
    stream.close()
    P.terminate()
    return True



# Wrapper functions to start and stop recording
def start_recording():
    MESSAGES.put(True)
    record = Thread(target=record_microphone)
    record.start()
    transcribe = Thread(target=speech_recognition, args=(output,))
    transcribe.start()


def stop_recording():
    print("Stopped.")
    return MESSAGES.get()


def speech_recognition(output):
    while not MESSAGES.empty():
        frames = recordings.get()

        rec.AcceptWaveform(b''.join(frames))
        result = rec.Result()
        text = json.loads(result)["text"]

        cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
        output.append_stdout(cased)
        time.sleep(1)


    def find_microphone():
    # Get the Devices on our computer instance
    devices = get_audio_device_info()
    # Find the MicroPhone! we have a built in Microphone
    for k, v in devices.items():
        if "Microphone" in k:
            MIC = v
            break
    # Did we find a Mic?
    if not MIC:
        quit("There is no Microphone attached")
    else:
        print("I found this microphone: " + MIC)
        # Now we have a device we can record!
        return MIC['index']


# __name__ is a magic function that returns the name of the running function
# __main__ is a protected function name that is set when this file is called
# we are basically asking python if we are running this file directly or
# importing it from else where, if we are importing it, the following
# will not run
if __name__ == "__main__":
    print('Starting to record')
    start_recording()
    input("Press Enter to stop recording...")
    stop_recording()
