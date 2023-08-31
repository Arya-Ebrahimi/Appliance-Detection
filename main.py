import tensorflow as tf


model = tf.keras.models.load_model('iot_model.h5')


print(model.summary())

model.predict
