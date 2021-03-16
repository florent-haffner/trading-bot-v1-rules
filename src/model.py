import os
from datetime import datetime

from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.callbacks import ModelCheckpoint


class Model:
    def __init__(self, config):
        self.model = keras.Sequential()
        self.buildModel(config)

    def buildModel(self, configs):
        print('[MODEL] Building model')
        for layer in configs['model']['layers']:
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

        self.model.compile(loss=configs['model']['loss'],
                           optimizer=configs['model']['optimizer'])
        print('[MODEL] Finish compilation')
        self.model.summary()  # TODO: remove this

    def train(self, config, X, y):
        print('SHAPE X INPUT TRAIN', X.shape)
        print('SHAPE y INPUT TRAIN', y.shape)

        X = X.reshape(X.shape[0], X.shape[1], 1)
        y = y.reshape(y.shape[0], y.shape[1], 1)

        print('SHAPE X RESHAPE TRAIN', X.shape)
        print('SHAPE y RESHAPE TRAIN', y.shape)

        print('[MODEL] started training process')

        #
        # THIS IS WEIRD but help us to finish multiple epoch
        #
        save_dir = "../../saved_model"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_fname = os.path.join(save_dir,
                                  f'{datetime.now().strftime("%d%m%Y-%H%M%S")}-e{str(config["model"]["training"]["epochs"])}.h5')

        callbacks = [
            ModelCheckpoint(filepath=save_fname,
                            monitor='loss',
                            save_best_only=True,
                            save_weights_only=True)
        ]

        self.model.fit(
            X, y,
            batch_size=config['model']['training']['batch_size'],
            steps_per_epoch=config['model']['training']['steps_per_epoch'],
            epochs=config['model']['training']['epochs'],
            callbacks=callbacks,
            workers=config['model']['training']['workers']
        )
        print('[MODEL] finished training process')
