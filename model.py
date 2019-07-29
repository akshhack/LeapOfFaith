import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle

verbose = False
filename = 'res/mlData.csv'
pkl_filename = 'res/model.pkl'
names = ['L0', 'L1', 'L2', 'L3', 'L4', 'R0', 'R1', 'R2', 'R3', 'R4', 'label']
if verbose:
    filename = 'res/mlDataVerbose.csv'
    names = ['L0_PA', 'L1_PA', 'L2_PA', 'L3_PA', 'L4_PA', 'L0_IA', 'L1_IA', 'L2_IA',
             'L3_IA', 'L4_IA', 'L0_X', 'L1_X', 'L2_X', 'L3_X', 'L4_X', 'L0_Y', 'L1_Y',
             'L2_Y', 'L3_Y', 'L4_Y', 'L0_Z', 'L1_Z', 'L2_Z', 'L3_Z', 'L4_Z', 'L0_PT',
             'L1_PT', 'L2_PT', 'L3_PT', 'L4_PT', 'L0_YW', 'L1_YW', 'L2_YW', 'L3_YW',
             'L4_YW', 'L0_R', 'L1_R', 'L2_R', 'L3_R', 'L4_R', 'R0_PA', 'R1_PA', 'R2_PA',
             'R3_PA', 'R4_PA', 'R0_IA', 'R1_IA', 'R2_IA', 'R3_IA', 'R4_IA', 'R0_X', 'R1_X',
             'R2_X', 'R3_X', 'R4_X', 'R0_Y', 'R1_Y', 'R2_Y', 'R3_Y', 'R4_Y', 'R0_Z', 'R1_Z',
             'R2_Z', 'R3_Z', 'R4_Z', 'R0_PT', 'R1_PT', 'R2_PT', 'R3_PT', 'R4_PT', 'R0_YW',
             'R1_YW', 'R2_YW', 'R3_YW', 'R4_YW', 'R0_R', 'R1_R', 'R2_R', 'R3_R', 'R4_R', 'label']
    pkl_filename = 'res/modelVerbose.pkl'

data = pd.read_csv(filename, names=names, engine='python')

def main():
    data.head()
    X = data.drop('label', axis=1)
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # scaler = StandardScaler()
    #
    # scaler.fit(X_train)
    #
    # X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)
    layers = (60,40)

    mlp = MLPClassifier(hidden_layer_sizes=layers, max_iter=500, learning_rate='invscaling', verbose=True, solver='lbfgs')
    mlp.fit(X_train, y_train)
    predictions = mlp.predict(X_test)
    print confusion_matrix(y_test, predictions)
    print classification_report(y_test, predictions)


    with open (pkl_filename, 'wb') as file:
        pickle.dump(mlp, file)


if __name__ == "__main__":
    main()
