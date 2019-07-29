import pickle
import numpy as np

pkl_filename = 'res/model.pkl'
model = None

with open(pkl_filename, 'rb') as file:
    global model
    model = pickle.load(file)

'''
    data: array of ['L0', 'L1', 'L2', 'L3', 'L4', 'R0', 'R1', 'R2', 'R3', 'R4']
'''
def predict_data_point(data):
    global model
    if model is not None:
        return model.predict(np.array(data))
    else:
        print "Don't forget to load the model"