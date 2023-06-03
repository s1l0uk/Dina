#!/usr/bin/env sh

pip install -r requirements.txt || \
  brew install portaudio && pip install -r requirements.txt

