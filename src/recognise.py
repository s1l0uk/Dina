#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
from vosk import Model, KaldiRecognizer
import time

model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

def speech_recognition(output):

    while not messages.empty():
        frames = recordings.get()

        rec.AcceptWaveform(b''.join(frames))
        result = rec.Result()
        text = json.loads(result)["text"]

        cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
        output.append_stdout(cased)
        time.sleep(1)
