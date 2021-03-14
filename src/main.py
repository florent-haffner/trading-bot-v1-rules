import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from data_acquisition import getFormattedData, splitDataset, getXy, process_data_to_scale

from model import Model



if __name__ == "__main__":
    # minute = getFormattedData('BTCEUR', '1')
    # print(len(minute))
    # minute.plot('timestamp', 'volume')
    # plt.show()
    #
    # heure = getFormattedData('BTCEUR', '60')
    # print(len(heure))
    # heure.plot('timestamp', 'volume')
    # plt.show()

    df = getFormattedData('BTCEUR', '60')
    df.plot('timestamp', 'volume')
    # plt.show()

    train, test = splitDataset(df, .85)
    X, y = getXy(train, 'volume')

    # Pre-process data to scale to 0->1
    scaler = MinMaxScaler()
    X_train, y_train = process_data_to_scale(scaler, X, y)
    print(X_train, y_train)
    inverse = scaler.inverse_transform(y_train)
    print(inverse)

    with open("setup.json", 'r') as JSON_model_setup:
        model_setup = json.load(JSON_model_setup)
        model = Model(model_setup)
        model.model.summary()
