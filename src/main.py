import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from data_acquisition import getFormattedData, splitDataset, getXy, process_data_to_scale

import tensorflow as tf
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

    df = getFormattedData(asset='BTCEUR', interval='60')
    df.plot('timestamp', 'volume')
    # plt.show()

    train, test = splitDataset(df, .85)
    X, y = getXy(dataset=train, X_key='timestamp', y_key='volume')

    # Pre-process data to scale to 0->1
    scaler = MinMaxScaler()
    X_train, y_train = process_data_to_scale(scaler, X, y)

    # TODO : if needed to inverse "scaling"
    # inverse = scaler.inverse_transform(y_train)

    #
    # TODO -> TF CONFIG : seems like it help my model to get over the training process
    #
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.7
    tf.compat.v1.keras.backend.set_session(
        tf.compat.v1.Session(config=config))

    model = None
    with open("ressources/setup.json", 'r') as JSON_model_setup:
        model_setup = json.load(JSON_model_setup)
        model = Model(model_setup)
        model.train(model_setup, X_train, y_train)
