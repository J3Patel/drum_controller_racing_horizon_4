#!/usr/bin/env python

"""Contains an example of midi input, and a separate example of midi output.

By default it runs the output example.
python midi.py --output
python midi.py --input

"""

import sys
import os

import pygame
import pygame.midi
import serial
from pygame.locals import *
from pynput.keyboard import Key, Listener, Controller
from pynput import keyboard
import time

keyboard = Controller()

arduino = serial.Serial('COM14', 9600, timeout=.1)

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))

def input_main(device_id = None):
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()


    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print ("using input_id :%s:" % input_id)
    i = pygame.midi.Input( input_id )

    pygame.display.set_mode((1,1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [QUIT]:
                going = False
            if e.type in [KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print (e)
                if e.data2 != 64:
                    if e.data1 == 48:
                        arduino.write(bytes("A", 'utf-8'))
                        time.sleep(0.11)
                        arduino.write(bytes("a", 'utf-8'))
                        # keyboard.press('A')
                        # keyboard.release('A')
                        print("tom1")
                    elif e.data1 == 45:
                        arduino.write(bytes("S", 'utf-8'))
                        time.sleep(0.3)
                        arduino.write(bytes("s", 'utf-8'))
                        print("tom2")
                    elif e.data1 == 38:
                        print("snare")
                        # arduino.write(bytes("A", 'utf-8'))

                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)

                    # elif e.data1 == 36:
                    #     print("kick")
                    elif e.data1 == 4:
                        if e.data2 <= 20:
                            arduino.write(bytes("w", 'utf-8'))
                            # keyboard.release('W')
                            print("stopped accelerating")
                        else:
                            arduino.write(bytes("W", 'utf-8'))
                            # keyboard.press('W')
                            print("accelerating")
                    elif e.data1 == 41:
                        arduino.write(bytes("D", 'utf-8'))
                        time.sleep(0.11)
                        arduino.write(bytes("d", 'utf-8'))

                        print("Tom3")

                    elif e.data1 == 51:
                        print("Ride")
                    elif e.data1 == 46:
                        keyboard.press(Key.esc)
                        keyboard.release(Key.esc)

                        print("HiHat")

        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post( m_e )

    del i
    pygame.midi.quit()

def main(mode='input', device_id=None):
    input_main(device_id)

if __name__ == '__main__':
    try:
        device_id = int( sys.argv[-1] )
    except:
        device_id = None

    input_main(device_id)
