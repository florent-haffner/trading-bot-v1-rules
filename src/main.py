import json
from data_acquisition import getFormattedData

import tensorflow as tf
from src.stocks_indicators import get_stocks_indicator
import matplotlib.pyplot as plt

def get_measure_viz(df, measure):
    df[measure].plot()
    plt.title(measure)
    plt.show()
    # print(measure)
    # print(df[measure])


def get_last_n_percentage(df, nbr_percentage):
    print(len(df))
    calculated_length = (len(df) * nbr_percentage) / 100
    tmp = df[:int(calculated_length)]
    print(len(tmp))
    return tmp


def run():
    # #
    # # TODO -> TF CONFIG : seems like it help my model to get over the training process
    # #
    # config = tf.compat.v1.ConfigProto()
    # config.gpu_options.per_process_gpu_memory_fraction = 0.7
    # tf.compat.v1.keras.backend.set_session(
    #     tf.compat.v1.Session(config=config))
    #
    # model = None
    # with open("ressources/applications.properties.json", 'r') as applications_properties:
    #     properties = json.load(applications_properties)

    asset = 'ETHEUR'
    interval = '60'

    df = getFormattedData(asset, interval)
    df.plot('timestamp', 'volume')
    plt.title('timestamp vs volume')
    plt.show()
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
    # df = [0,1,2,3,4,5,6,7,8,9]

    print('Dataset :', len(df) / 24, 'days')
    df = get_stocks_indicator(df)
    print(df.keys())

    tmp_df = get_last_n_percentage(df, 25)
    tmp_df.head(1)
    tmp_df.tail(1)

    get_measure_viz(tmp_df, 'close_12_ema')
    get_measure_viz(tmp_df, 'close_26_ema')

    get_measure_viz(tmp_df, 'macd')
    get_measure_viz(tmp_df, 'macds')
    get_measure_viz(tmp_df, 'macdh')
