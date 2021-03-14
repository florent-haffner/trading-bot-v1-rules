
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class Model:
    def __init__(self):
        self.model = keras.Sequential()
        self.createLayers()

    def createLayers(self):
        self.model.add(layers.Dense(2, activation="relu"))
        self.model.add(layers.Dense(4, activation="relu"))
        self.model.add(layers.Dense(4))
        print(len(self.model.layers))

        X = tf.ones((1,4))
        y = self.model(X)
        self.model.summary()
