import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class ModelController:
    prediction_period = 10
    model_bias = 0.01

    def __init__(self, modelpath: str = r"D:\python\decide_server\DecideServer\60-20-60-model.hdf5"):
        self._model: tf.keras.Sequential = tf.keras.models.load_model(modelpath)
        self._scaler = MinMaxScaler(feature_range=(0, 1))

    @property
    def model(self):
        return self._model

    @property
    def scaler(self):
        return self._scaler

    def predict(self, data: list):
        data = data[:ModelController.prediction_period]
        assert len(data) == 10, "invalid data length"

        data = np.array(data)
        data = data.reshape(-1, 1)
        self.scaler.fit(data)
        data = self.scaler.transform(data)
        assert data.shape == (10, 1)
        data = data.reshape(1, 10, 1)
        pred = self.model.predict(data)
        pred = self.scaler.inverse_transform(pred)
        pred = pred[0][0]
        bias = pred*ModelController.model_bias
        return pred
