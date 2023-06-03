#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .record import start_recording, stop_recording
from .verbs import *


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
    print("Using the recording to " + sys.argv)
