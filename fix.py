import h5py
import numpy as np
import tensorflow as tf

print('TF version:', tf.__version__)

base = tf.keras.applications.VGG16(
    weights=None,
    include_top=False,
    input_shape=(224, 224, 3)
)

x = tf.keras.layers.Flatten()(base.output)
x = tf.keras.layers.Dense(256, activation='relu')(x)
output = tf.keras.layers.Dense(1, activation='sigmoid')(x)
model = tf.keras.Model(inputs=base.input, outputs=output)

print('Architecture reconstruite OK')

model.load_weights(
    'model/vgg16_malignant_vs_benign.h5',
    by_name=True,
    skip_mismatch=True
)

print('Poids charges OK')

model.save('model/vgg16_fixed.h5')
print('Sauvegarde terminee OK')
