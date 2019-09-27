import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Dense
from keras import regularizers

if __name__ == "__main__":
    import sys 
    sys.path.append('../config')  # for config module

from log import Log
from models import *


class autoEncoder:
    
    def __init__(self, transHistory):
        Log.debug('autoEncoder::__init__()')

        self.transHistory = transHistory
        self.DATA_COL_COUNT = len(transHistory[0])
        npArray = np.asarray(transHistory)

        # Creating The Model
        # nb_epoch = 100
        nb_epoch = 100
        batch_size = len(transHistory)
        input_dim = npArray.shape[1] #num of columns, 30
        encoding_dim = int(input_dim / 2)
        hidden_dim = int(encoding_dim / 2) #i.e. 7
        learning_rate = 1e-7

        input_layer = Input(shape=(input_dim, ))
        encoder = Dense(encoding_dim, activation="tanh", activity_regularizer=regularizers.l1(learning_rate))(input_layer)
        encoder = Dense(hidden_dim, activation="relu")(encoder)
        decoder = Dense(hidden_dim, activation='tanh')(encoder)
        decoder = Dense(input_dim, activation='relu')(decoder)

        self.autoencoder = Model(inputs=input_layer, outputs=decoder)
        
        # Model Training and Logging
        self.autoencoder.compile(metrics=['accuracy'],
                            loss='mean_squared_error',
                            optimizer='adam')

        self.autoencoder.fit(npArray, npArray,
                            epochs=nb_epoch,
                            batch_size=batch_size,
                            shuffle=True,
                            validation_data=(npArray, npArray),
                            verbose=1)


    def getScore(self, transaction):
        Log.debug('autoEncoder::getScore()')

        predictions = self.autoencoder.predict(np.asarray(transaction).reshape(-1, self.DATA_COL_COUNT))
        print(predictions)

        # for r in predictions:
        #     print(r)

        # Log.info('score:' + str(score))
        # return math.floor(abs(score) * 100)



if __name__ == "__main__":

    fds = autoEncoder(
        [
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 1.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.235294],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.075812, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000]
        ]
    )

    score = fds.getScore(
        [
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 1.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.235294],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 1.0, 0.075812, 1.0, 1.0, 1.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 0.0, 1.000000, 0.0, 0.0, 0.000000, 0.000000],
            [0.0, 1.0, 0.000000, 1.0, 1.0, 0.897616, 0.000000]
        ]
    )

    print(score)