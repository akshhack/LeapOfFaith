import os, sys, inspect, thread, time, threading
sys.path.insert(0, "lib")
import Leap
from hands import predict_char, get_char
import mac_say


#import win32com.client as wincl
#speak = wincl.Dispatch("SAPI.SpVoice")
#speak.Speak("Hello World")

import Tkinter as tk

mac_say.voices('en')

bufferString = ""
bufferStringLock = threading.Lock()

class TextViewer:
    def __init__(self, master):
        self.master = master
        master.title("Braille Text Viewer")
        master.geometry('1200x750')
        self.label=tk.Label(master, font=("Segoe UI", 200))
        self.label.grid(row=1, column=2)
        self.label.configure(text='')
        self.update_label()

        def on_click(self):
            #bufferString = ""
            self.__init__(master)

        self.reset = tk.Button(master, text="Reset", command=on_click).place(x=15, y=700)

    def update_label(self):
        global bufferStringLock
        global bufferString

        bufferStringLock.acquire()
        # print "updating string in tkinter"
        self.label.configure(text = '{}'.format(bufferString))
        bufferStringLock.release()
        self.label.after(1800, self.update_label)

    
    

def speak(text):
    mac_say.say(text, background=True)

class KeyListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    hand_count = 0

    def on_init(self, controller):
        pass
        # print "Initialized"

    def on_connect(self, controller):
        pass
        # print "Connected"

    def on_disconnect(self, controller):
        pass
        # Note: not dispatched when running in a debugger.
        # print "Disconnected"

    def on_exit(self, controller):
        pass
        # print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        time.sleep(0.3)

        if (frame.hands and len(frame.hands) == 2):
            global bufferString
            global bufferStringLock

            left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
            right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

            KeyListener.hand_count = 0

            #a, prob = predict_char(left_hand, right_hand)
            a = get_char(left_hand, right_hand)
            #speak.Speak(a)
            #print "Letter: " + a

            bufferStringLock.acquire()
            if len(bufferString) == 0 or bufferString[-1] != a:
                bufferString += a
                if a == " ":
                    speak("space")
                elif a == "?":
                    speak("question mark")
                elif a == "!":
                    speak("exclamation mark")
                elif a == ".":
                    speak("period")
                else:
                    speak(a)
                time.sleep(0.7)
            bufferStringLock.release()

        else:
            print "Hands count: ", KeyListener.hand_count
            if (KeyListener.hand_count % 30) == 0:
                speak("Hands not detected")
            KeyListener.hand_count += 1
            pass

def main():
    # Create a Key listener and controller
    listener = KeyListener()
    controller = Leap.Controller()

    # Have the key listener receive events from the controller
    controller.add_listener(listener)

    # print controller

    # Keep this process running until Enter is pressed
    # print "Press Ctrl+C to quit..."
    try:
        root = tk.Tk()
        TextViewer(root)
        # print "About to start tkinter crap"
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the Key listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()