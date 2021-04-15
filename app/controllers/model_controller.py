import tensorflow as tf


class ModelController:

    def __init__(self, modelpath: str = "60-20-60-model.hdf5"):
        self._model = tf.keras.models.load_model(modelpath)

    @property
    def model(self):
        return self._model

