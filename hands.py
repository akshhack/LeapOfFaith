# hands.py 
import json

with open ('res\\braille_map.json') as filedata:
    BRAILLE_DICT = json.loads(filedata.read())
with open ('res\\finger_map.json') as filedata:
    FINGER_DICT = json.loads(filedata.read())

finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
SHIFT = "7"

def get_char(left_hand, right_hand):
        str_left = get_activations_left(left_hand)
        print str_left
        str_right = get_activations_right(right_hand)
        print str_right
        char_key = get_braille_key(str_left, str_right)
        return char_key

def get_activations_left(hand):
    key_str = ""
    left_hand_state = {}
    for finger in hand.fingers:
        left_hand_state[finger_names[finger.type]] = finger.direction.z
        key = ""
        if (finger.is_extended):
            continue
        key += "L" + str(finger.type)
        assert(key in FINGER_DICT)
        key_str += FINGER_DICT[key]
    print "left hand direction: " + str(hand.direction.z)
    print "left hand state: " + str(left_hand_state)
    return key_str

def get_activations_right(hand):
    key_str = ""
    right_hand_state = {}
    for finger in hand.fingers:
        right_hand_state[finger_names[finger.type]] = finger.direction.z
        key = ""
        if (finger.is_extended):
            continue
        key += "R" + str(finger.type)
        assert(key in FINGER_DICT)
        key_str += FINGER_DICT[key]
    print "right hand direction: " + str(hand.direction.z)
    print "right hand state: " + str(right_hand_state)
    return key_str

def get_braille_key(left, right):
    res = ""
    info = set(left + right) # set composed of left and right activations
    shift = SHIFT in info
    for key in BRAILLE_DICT:
        if (set(key) == info):
            res  = BRAILLE_DICT[key]
            if (not shift): # shift key 
                res =  res.lower()
            break
    return res
 