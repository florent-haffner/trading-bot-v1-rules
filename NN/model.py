from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, LSTM

from src.services.krakenDataService import get_formatted_data


class Model:
    def __init__(self, properties):
        self.model = keras.Sequential()
        self.buildModel(properties)

    def buildModel(self, properties):
        print('[MODEL] Building model')
        for layer in properties['model']['layers']:
            neurons = layer['neurons'] if 'neurons' in layer else None
            dropout_rate = layer['rate'] if 'rate' in layer else None
            activation = layer['activation'] if 'activation' in layer else None
            return_seq = layer['return_seq'] if 'return_seq' in layer else None
            input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
            input_dim = layer['input_dim'] if 'input_dim' in layer else None

            if layer['type'] == 'dense':
                self.model.add(Dense(neurons, activation=activation))
            if layer['type'] == 'lstm':
                self.model.add(LSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
            if layer['type'] == 'dropout':
                self.model.add(Dropout(dropout_rate))

        self.model.compile(loss=properties['model']['loss'],
                           optimizer=properties['model']['optimizer'])
        print('[MODEL] Finish compilation')
        self.model.summary()  # TODO: remove this

    def process_input(self, timesteps, matrix):
        print(timesteps)
        count = len(matrix)
        print(count, (count / timesteps))

        # for values in range(len(matrix)):
        #     print(matrix[values])

        return matrix

    # def train(self, config, X, y):
    #     print('SHAPE X INPUT TRAIN', X.shape)
    #     print('SHAPE y INPUT TRAIN', y.shape)
    #
    #     X = X.reshape(X.shape[0], X.shape[1], 1)
    #     y = y.reshape(y.shape[0], y.shape[1], 1)
    #
    #     print('SHAPE X RESHAPE TRAIN', X.shape)
    #     print('SHAPE y RESHAPE TRAIN', y.shape)
    #
    #     print('[MODEL] started training process')
    #
    #     #
    #     # THIS IS WEIRD but help us to finish multiple epoch
    #     #
    #     save_dir = "../../saved_model"
    #     if not os.path.exists(save_dir):
    #         os.mkdir(save_dir)
    #     save_fname = os.path.join(save_dir,
    #                               f'{datetime.now().strftime("%d%m%Y-%H%M%S")}-e{str(config["model"]["training"]["epochs"])}.h5')
    #
    #     callbacks = [
    #         ModelCheckpoint(filepath=save_fname,
    #                         monitor='loss',
    #                         save_best_only=True,
    #                         save_weights_only=True)
    #     ]
    #
    #     self.model.fit(
    #         X, y,
    #         batch_size=config['model']['training']['batch_size'],
    #         steps_per_epoch=config['model']['training']['steps_per_epoch'],
    #         epochs=config['model']['training']['epochs'],
    #         callbacks=callbacks,
    #         workers=config['model']['training']['workers']
    #     )
    #     print('[MODEL] finished training process')


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

    df = get_formatted_data(asset, interval)
    df.plot('timestamp', 'volume')
    plt.title('timestamp vs volume')
    plt.show()
    return df
    # plt.show()

        # train, test = splitDataset(df, .85)
        # X, y = getXy(dataset=train, X_key='timestamp', y_key='volume')
        #
        # # Pre-process mock to scale to 0->1
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
