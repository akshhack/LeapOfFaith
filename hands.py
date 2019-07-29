# hands.py
import json
import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
from leap_motion_data_collector import get_angle_inter, get_angle_prox, get_dir, get_vector_data

EPSILON = 0.4

verbose = True
pkl_filename = 'res/model.pkl'

if verbose:
    pkl_filename = 'res/modelVerbose.pkl'


with open ('res/braille_map.json') as filedata:
    BRAILLE_DICT = json.loads(filedata.read())
with open ('res/finger_map.json') as filedata:
    FINGER_DICT = json.loads(filedata.read())
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
left_hand_fingers = ['L0', 'L1', 'L2', 'L3', 'L4']
right_hand_fingers = ['R0', 'R1', 'R2', 'R3', 'R4']

left_hand_thresholds = [35, 45, 40, 45, 0]
right_hand_thresholds = [35, 45, 40, 45, 0]

SHIFT = "7"
RAD_TO_DEG = 57.2727273

def calculate_cos(finger):
    global EPSILON
    cos = finger.bone(1).direction.dot(finger.bone(2).direction)
    return cos > -EPSILON and cos < EPSILON

def handOrientation(hand, finger):
    global EPSILON
    cos = hand.direction.dot(finger.bone(1).direction)
    return cos > -EPSILON and cos < EPSILON

def get_data_angles(left_hand, right_hand):
    dataPoint = [0 for i in range (10)]
    for finger in left_hand.fingers:
        dataPoint[finger.type] = get_angle_prox(finger)
    for finger in right_hand.fingers:
        dataPoint[finger.type + 5] = get_angle_prox(finger)
    return dataPoint

def get_data_all(left_hand, right_hand):
    dataPoint = [0 for i in range (80)]
    for finger in left_hand.fingers:
        dataPoint[finger.type] = get_angle_prox(finger)
        dataPoint[finger.type + 5] = get_angle_inter(finger)
        dataPoint[finger.type + 10] = get_dir(finger, 'X')
        dataPoint[finger.type + 15] = get_dir(finger, 'Y')
        dataPoint[finger.type + 20] = get_dir(finger, 'Z')
        dataPoint[finger.type + 25] = get_vector_data(finger, 'pitch')
        dataPoint[finger.type + 30] = get_vector_data(finger, 'yaw')
        dataPoint[finger.type + 35] = get_vector_data(finger, 'roll')
    for finger in right_hand.fingers:
        dataPoint[finger.type + 40] = get_angle_prox(finger)
        dataPoint[finger.type + 45] = get_angle_inter(finger)
        dataPoint[finger.type + 50] = get_dir(finger, 'X')
        dataPoint[finger.type + 55] = get_dir(finger, 'Y')
        dataPoint[finger.type + 60] = get_dir(finger, 'Z')
        dataPoint[finger.type + 65] = get_vector_data(finger, 'pitch')
        dataPoint[finger.type + 70] = get_vector_data(finger, 'yaw')
        dataPoint[finger.type + 75] = get_vector_data(finger, 'roll')
    return dataPoint

def predict_char(left_hand, right_hand):
    global model
    if verbose:
        dataPoint = get_data_all(left_hand, right_hand)
    else: 
        dataPoint = get_data_angles(left_hand, right_hand)
    dataPoint = np.array(dataPoint)
    dataPoint = dataPoint.reshape(1,-1) # reshape for single sample
    probs = model.predict_proba(dataPoint)
    pred = model.predict(dataPoint)
    max_prob = np.max(probs)

    max_char = "" if pred == 0 else chr(pred[0])
    print "Probabilities are = " + str(probs)
    print "Max Probability is = " + str(max_prob)
    print "Max Prediction is = " + max_char
    return (max_char, max_prob)


def get_char(left_hand, right_hand):
        str_left = get_activations_left(left_hand)
        print str_left
        str_right = get_activations_right(right_hand)
        print str_right
        char_key = get_braille_key(str_left, str_right)
        return char_key

def is_extended(hand, finger):
    global left_hand_thresholds
    global right_hand_thresholds
    if hand.is_left:
        return get_angle(finger) < left_hand_thresholds[finger.type] 
    else:
        return get_angle(finger) < right_hand_thresholds[finger.type]

# def is_extended(hand, finger):
#     return not handOrientation(hand, finger)

def get_activations_left(hand):
    key_str = ""
    left_hand_state = {}
    for finger in hand.fingers:
        angle = get_angle(finger)
        left_hand_state[finger_names[finger.type]] = get_angle(finger)
        key = ""
        if is_extended(hand, finger):
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
        angle = get_angle(finger)
        right_hand_state[finger_names[finger.type]] = get_angle(finger)
        key = ""
        if is_extended(hand, finger):
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
    shift = SHIFT in (left + right)
    for key in BRAILLE_DICT:
        if (set(key) == info):
            res  = BRAILLE_DICT[key]
            if (not shift): # shift key
                res =  res.lower()
            break
    return res

def get_angle(finger):
    if (finger.type != 0):
        b1 = finger.bone(1).direction
        b2 = finger.bone(2).direction
    else: # Thumb
        b1 = finger.bone(1).direction
        b2 = finger.bone(2).direction

    angle = b1.angle_to(b2) * RAD_TO_DEG
    return angle
