# leap_motion_data_collector
import os, sys, inspect, thread, time, csv 
sys.path.insert(0, "lib")
import Leap
import string


# Init constants 

NUM_SAMPLES = 100000
left_hand_fingers = ['L0', 'L1', 'L2', 'L3', 'L4']
right_hand_fingers = ['R0', 'R1', 'R2', 'R3', 'R4']

L_PA = ['L0_PA', 'L1_PA', 'L2_PA', 'L3_PA', 'L4_PA']
L_IA = ['L0_IA', 'L1_IA', 'L2_IA', 'L3_IA', 'L4_IA']
L_X = ['L0_X', 'L1_X', 'L2_X', 'L3_X', 'L4_X']
L_Y = ['L0_Y', 'L1_Y', 'L2_Y', 'L3_Y', 'L4_Y']
L_Z = ['L0_Z', 'L1_Z', 'L2_Z', 'L3_Z', 'L4_Z']
L_PT = ['L0_PT', 'L1_PT', 'L2_PT', 'L3_PT', 'L4_PT']
L_YW = ['L0_YW', 'L1_YW', 'L2_YW', 'L3_YW', 'L4_YW']
L_R = ['L0_R', 'L1_R', 'L2_R', 'L3_R', 'L4_R']

R_PA = ['R0_PA', 'R1_PA', 'R2_PA', 'R3_PA', 'R4_PA']
R_IA = ['R0_IA', 'R1_IA', 'R2_IA', 'R3_IA', 'R4_IA']
R_X = ['R0_X', 'R1_X', 'R2_X', 'R3_X', 'R4_X']
R_Y = ['R0_Y', 'R1_Y', 'R2_Y', 'R3_Y', 'R4_Y']
R_Z = ['R0_Z', 'R1_Z', 'R2_Z', 'R3_Z', 'R4_Z']
R_PT = ['R0_PT', 'R1_PT', 'R2_PT', 'R3_PT', 'R4_PT']
R_YW = ['R0_YW', 'R1_YW', 'R2_YW', 'R3_YW', 'R4_YW']
R_R = ['R0_R', 'R1_R', 'R2_R', 'R3_R', 'R4_R']

verbose_fieldnames = sum([L_PA, L_IA, L_X, L_Y, L_Z, L_PT, L_YW, L_R, R_PA, R_IA, R_X, R_Y, R_Z, R_PT, R_YW, R_R, ['label']], [])
#print verbose_fieldnames

RAD_TO_DEG = 57.2727273

def get_angle_prox(finger): #PA
    global RAD_TO_DEG
    b1 = finger.bone(1).direction
    b2 = finger.bone(2).direction
    angle = b1.angle_to(b2) * RAD_TO_DEG
    return angle

def get_angle_inter(finger): #IA
    global RAD_TO_DEG
    if (finger.type != 0):
        b1 = finger.bone(2).direction
        b2 = finger.bone(3).direction
    else: # Thumb
        b1 = finger.bone(1).direction
        b2 = finger.bone(2).direction

    angle = b1.angle_to(b2) * RAD_TO_DEG
    return angle

def get_dir(finger, dir):
    if dir == "X":
        return finger.direction.x
    elif dir == "Y":
        return finger.direction.y 
    elif dir == "Z":
        return finger.direction.z 
    else:
        print "Incorrect args"
        return None

def get_vector_data(finger, spec):
    if spec == 'yaw':
        return finger.direction.yaw
    elif spec == 'pitch':
        return finger.direction.pitch
    elif spec == 'roll':
        return finger.direction.roll
    else:
        print "Incorrect args"
        return None


def get_data_angles(frame, letter, data_counter):
    dataPoint = {}
    if (frame.hands and len(frame.hands) == 2):

        left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
        right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

        dataPoint = {}

        for finger in left_hand.fingers:
            dataPoint[left_hand_fingers[finger.type]] = get_angle_prox(finger)
        for finger in right_hand.fingers:
            dataPoint[right_hand_fingers[finger.type]] = get_angle_prox(finger)

        dataPoint["label"] = 0

        if (data_counter % 100 == 0):
            print "Data Point: " + str(data_counter) + " of letter: " + letter
        return (dataPoint, True)
    else:
        print "Hands not in focus"
        return (dataPoint, False)

def get_data_all(frame, letter, data_counter):
    dataPoint = {}
    if (frame.hands and len(frame.hands) == 2):

        left_hand = frame.hands[0] if frame.hands[0].is_left else frame.hands[1]
        right_hand = frame.hands[1] if frame.hands[1].is_right else frame.hands[0]

        dataPoint = {}

        for finger in left_hand.fingers:
            dataPoint[L_PA[finger.type]] = get_angle_prox(finger)
            dataPoint[L_IA[finger.type]] = get_angle_inter(finger)
            dataPoint[L_X[finger.type]] = get_dir(finger, 'X')
            dataPoint[L_Y[finger.type]] = get_dir(finger, 'Y')
            dataPoint[L_Z[finger.type]] = get_dir(finger, 'Z')
            dataPoint[L_PT[finger.type]] = get_vector_data(finger, 'pitch')
            dataPoint[L_YW[finger.type]] = get_vector_data(finger, 'yaw')
            dataPoint[L_R[finger.type]] = get_vector_data(finger, 'roll')
        for finger in right_hand.fingers:
            dataPoint[R_PA[finger.type]] = get_angle_prox(finger)
            dataPoint[R_IA[finger.type]] = get_angle_inter(finger)
            dataPoint[R_X[finger.type]] = get_dir(finger, 'X')
            dataPoint[R_Y[finger.type]] = get_dir(finger, 'Y')
            dataPoint[R_Z[finger.type]] = get_dir(finger, 'Z')
            dataPoint[R_PT[finger.type]] = get_vector_data(finger, 'pitch')
            dataPoint[R_YW[finger.type]] = get_vector_data(finger, 'yaw')
            dataPoint[R_R[finger.type]] = get_vector_data(finger, 'roll')

        dataPoint["label"] = 0

        if (data_counter % 100 == 0):
            print "Data Point: " + str(data_counter) + " of letter: " + letter
        return (dataPoint, True)
    else:
        print "Hands not in focus"
        time.sleep(0.05)
        return (dataPoint, False)


def main():

    global left_hand_fingers
    global right_hand_fingers
    global NUM_SAMPLES

    controller = Leap.Controller()

    letter = raw_input("Enter label: ")
    verbose = False

    filename = 'res/mlData.csv'
    if verbose: filename = 'res/mlDataVerbose.csv'

    print "Show letter: " + letter
    time.sleep(4)
    #start = raw_input("Wait for Enter to be pressed")

    with open(filename, 'a') as csvfile:
        fieldnames = ['L0', 'L1', 'L2', 'L3', 'L4', 'R0', 'R1', 'R2', 'R3', 'R4', 'label']
        if verbose:
            fieldnames = verbose_fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        data_counter = 0

        while data_counter < NUM_SAMPLES:
            frame = controller.frame()
            if verbose:
                dataPoint, status = get_data_all(frame, letter, data_counter)
            else: 
                dataPoint, status = get_data_angles(frame, letter, data_counter)
            if(status):
                writer.writerow(dataPoint)
                data_counter += 1
            
    print "Completed sampling letter: " + letter

if __name__ == "__main__":
    main()