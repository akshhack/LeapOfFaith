import pickle
import numpy as np
import os, sys, inspect, thread, time, csv 
from sklearn.neural_network import MLPClassifier
sys.path.insert(0, "lib")
import Leap
from leap_motion_data_collector import get_angle_inter, get_angle_prox, get_dir, get_vector_data

pkl_filename = 'res/model.pkl'
left_hand_fingers = ['L0', 'L1', 'L2', 'L3', 'L4']
right_hand_fingers = ['R0', 'R1', 'R2', 'R3', 'R4']
all_fingers = left_hand_fingers + right_hand_fingers

names = ['L0_PA', 'L1_PA', 'L2_PA', 'L3_PA', 'L4_PA', 'L0_IA', 'L1_IA', 'L2_IA', 
         'L3_IA', 'L4_IA', 'L0_X', 'L1_X', 'L2_X', 'L3_X', 'L4_X', 'L0_Y', 'L1_Y',
         'L2_Y', 'L3_Y', 'L4_Y', 'L0_Z', 'L1_Z', 'L2_Z', 'L3_Z', 'L4_Z', 'L0_PT', 
         'L1_PT', 'L2_PT', 'L3_PT', 'L4_PT', 'L0_YW', 'L1_YW', 'L2_YW', 'L3_YW', 
         'L4_YW', 'L0_R', 'L1_R', 'L2_R', 'L3_R', 'L4_R', 'R0_PA', 'R1_PA', 'R2_PA', 
         'R3_PA', 'R4_PA', 'R0_IA', 'R1_IA', 'R2_IA', 'R3_IA', 'R4_IA', 'R0_X', 'R1_X', 
         'R2_X', 'R3_X', 'R4_X', 'R0_Y', 'R1_Y', 'R2_Y', 'R3_Y', 'R4_Y', 'R0_Z', 'R1_Z', 
         'R2_Z', 'R3_Z', 'R4_Z', 'R0_PT', 'R1_PT', 'R2_PT', 'R3_PT', 'R4_PT', 'R0_YW', 
         'R1_YW', 'R2_YW', 'R3_YW', 'R4_YW', 'R0_R', 'R1_R', 'R2_R', 'R3_R', 'R4_R', 'label']
RAD_TO_DEG = 57.2727273

def get_data_angles(frame):
    dataPoint = {}
    if (frame.hands and len(frame.hands) == 2):

        left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
        right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

        dataPoint = [0 for i in range (10)]

        for finger in left_hand.fingers:
            dataPoint[finger.type] = get_angle_prox(finger)
        for finger in right_hand.fingers:
            dataPoint[finger.type + 5] = get_angle_prox(finger)
        return (dataPoint, True)
    else:
        print "Hands not in focus"
        return (dataPoint, False)

def get_data_all(frame):
    dataPoint = {}
    if (frame.hands and len(frame.hands) == 2):

        left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
        right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

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
        return (dataPoint, True)
    else:
        print "Hands not in focus"
        time.sleep(0.05)
        return (dataPoint, False)

verbose = False

def main():

    global pkl_filename
    global left_hand_fingers
    global right_hand_fingers

    start = raw_input("Pose and hit enter when ready")

    controller = Leap.Controller()

    while True: 
        time.sleep(2.5)
        frame = controller.frame()
        dataPoint, status = get_data_all(frame) if verbose else get_data_angles(frame)
        dataPoint = np.array(dataPoint)
        dataPoint = dataPoint.reshape(1,-1) # reshape for single sample
        #print dataPoint

        if(status):
            with open(pkl_filename, 'rb') as file:
                model = pickle.load(file)
                print "Probability is = " , model.predict_proba(dataPoint)
                print "Prediction is = " + chr(model.predict(dataPoint)[0])
            break
    
if __name__ == "__main__":
    main()