#!/usr/bin/env python3

# Converts a value read from a serial port into a pitch via MIDI.
# I.e., plays incoming data as an audible pitch.
# First used for reporting RSSI on radios while I mess with the antenna position.
# Copyright (c) 2017 by Six Mile Creek Systems LLC.

# Requires:
# PyGame: http://pygame.org/download.shtml
#     sudo pip install pygame
# pyserial
#     pip install pyserial
# Python 3.

# Usage:
# Pass the serial port name as the first parameter:
#  python3 rssi.py COM11
#  python3 rssi.py /dev/ttyUSB0


import os
import sys
import time

import pygame.midi
import serial

COM_PORT_BAUD_RATE = 115200

# Flag for the value we're looking for
RSSI_FLAG = 'RSSI='

# Serial port setup
serialPortPath = sys.argv[1]
thePort = serial.Serial(serialPortPath, COM_PORT_BAUD_RATE, timeout=15)

# MIDI setup
pygame.midi.init()
midiOut = pygame.midi.Output(pygame.midi.get_default_output_id())
midiOut.set_instrument(90)

# Read loop
currentNote = 0
peakRssi = -200
try:
    while(True):
        # Read the next line.
        line = thePort.readline().decode('utf-8')
        line = line.strip()
        # print(line)

        # Parse it to get a RSSI value.
        # Get the last space-separated thing on the line, and use it if it starts with '-'.
        lastword = line.split(' ')[-1]
        if lastword.startswith(RSSI_FLAG):
            # Convert to an integer
            rssi = int(lastword[len(RSSI_FLAG):])
            peakRssi = max(peakRssi, rssi)
            print("  RSSI =", rssi, "- max seen:", peakRssi)

            # Convert that to a new note.
            newNote = rssi + 100
            # print("  new note = ", newNote)

            # Play the new note.
            midiOut.note_off(currentNote)
            currentNote = newNote
            midiOut.note_on(currentNote, 127)
except KeyboardInterrupt:
    pass
finally:
    # Clean up.
    midiOut.abort()
    midiOut.close()
