import json
from data_acquisition import getFormattedData

import tensorflow as tf
from src.stocks_indicators import get_stocks_indicator
import matplotlib.pyplot as plt


def run():
    #
    # TODO -> TF CONFIG : seems like it help my model to get over the training process
    #
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.7
    tf.compat.v1.keras.backend.set_session(
        tf.compat.v1.Session(config=config))

    model = None
    with open("ressources/applications.properties.json", 'r') as applications_properties:
        properties = json.load(applications_properties)

        df = getFormattedData(asset='BTCEUR', interval='1')
        df.plot('timestamp', 'volume')
        return df
        # plt.show()

        # train, test = splitDataset(df, .85)
        # X, y = getXy(dataset=train, X_key='timestamp', y_key='volume')
        #
        # # Pre-process data to scale to 0->1
        # scaler = MinMaxScaler()
        # X_train, y_train = process_data_to_scale(scaler, X, y)
        #
        # # TODO : if needed to inverse "scaling"
        # # inverse = scaler.inverse_transform(y_train)
        #
        # model = Model(properties)
        #
        # print('[MODEL] PROCESS INPUT TO ENABLE USAGE OF LSTM')
        # X_train = model.process_input(properties['model']['layers'][0]['input_timesteps'], X_train)
        # y_train = model.process_input(properties['model']['layers'][0]['input_timesteps'], y_train)
        # # model.train(properties, X_train, y_train)


if __name__ == "__main__":
    df = run()

    print('Dataset :', len(df) / 24, 'days')
    df = get_stocks_indicator(df)
    print(df.keys())

    measure = 'macd'
    df[measure].plot()
    plt.title(measure)
    plt.show()
    print(measure)
    print(df[measure])

    measure = 'close_12_ema'
    df[measure].plot()
    plt.title(measure)
    plt.show()
    print(measure)
    print(df[measure])


    measure = 'close_26_ema'
    df[measure].plot()
    plt.title(measure)
    plt.show()
    print(measure)
    print(df[measure])


    measure = 'macds'
    df[measure].plot()
    plt.title(measure)
    plt.show()
    print(measure)
    print(df[measure])


    measure = 'macdh'
    df[measure].plot()
    plt.title(measure)
    plt.show()
    print(measure)
    print(df[measure])
