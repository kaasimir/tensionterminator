import tensorflow as tf
from tensorflow.keras.layers import Dense
from frameworktest_tf import FrameworkLogger

# Daten vorbereiten
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape((60000, 28 * 28)).astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28)).astype('float32') / 255

# Modell definieren
model = tf.keras.models.Sequential([
    Dense(512, activation='relu', input_shape=(28 * 28,)),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Modell trainieren
logger = FrameworkLogger(train_images, train_labels, test_images, test_labels, 5, model)
# logger.train_model()
logger.generate_statistics()
