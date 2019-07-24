import os, sys, inspect, thread, time, threading

import Leap
from hands import get_char

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak("Hello World")

import Tkinter as tk

bufferString = ""
bufferStringLock = threading.Lock()

class TextViewer:
    def __init__(self, master):
        master.title("Braille Text Viewer")
        master.geometry('450x400')
        self.label=tk.Label(master, font=("Segoe UI", 70))
        self.label.grid(row=1, column=2)
        self.label.configure(text='')
        self.update_label()
 
    def update_label(self):
        global bufferStringLock
        global bufferString

        bufferStringLock.acquire()
        print "updating string"
        self.label.configure(text = '{}'.format(bufferString))
        bufferStringLock.release()
        self.label.after(1800, self.update_label)

class KeyListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    lang = 'en'

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        time.sleep(3)

        if (frame.hands and len(frame.hands) == 2):
            global bufferString
            global bufferStringLock

            left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
            right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

            a = get_char(left_hand, right_hand)
            speak.Speak(a)
            print "Letter: " + a

            bufferStringLock.acquire()
            if (len(bufferString) > 0 and bufferString[-1] != a):
                bufferString += a
            bufferStringLock.release()
        else:
            print "Hands not detected"
            #speak.Speak("Hands not detected")

def main():
    # Create a Key listener and controller
    listener = KeyListener() 
    controller = Leap.Controller()

    # Have the key listener receive events from the controller
    controller.add_listener(listener) 

    print controller

    # Keep this process running until Enter is pressed
    print "Press Ctrl+C to quit..."
    try:
        root = tk.Tk()
        TextViewer(root)
        print "About to start tkinter crap"
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the Key listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()