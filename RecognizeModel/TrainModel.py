import cv2
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop
from shutil import copyfile
import matplotlib.pyplot as plt
from keras.utils.image_utils import img_to_array
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from keras import backend as k
from keras.callbacks import EarlyStopping

from LoadData import *


def train_val_generators(TRAINING_DIR, VALIDATION_DIR):
    """
      Creates the training and validation data generators

      Args:
        TRAINING_DIR (string): directory path containing the training images
        VALIDATION_DIR (string): directory path containing the testing/validation images

      Returns:
        train_generator, validation_generator - tuple containing the generators
    """
    # Instantiate the ImageDataGenerator class
    train_datagen = ImageDataGenerator(rescale=1.0 / 255,
                                       # rotation_range=2,
                                       # width_shift_range=0.05,
                                       # height_shift_range=0.05,
                                       # shear_range=0.01,
                                       # zoom_range=0.05,
                                       # horizontal_flip=False,
                                       # fill_mode='nearest'
                                       )

    # Pass in the appropriate arguments to the flow_from_directory method
    train_generator = train_datagen.flow_from_directory(directory=TRAINING_DIR,
                                                        color_mode="grayscale",
                                                        # batch_size=128,
                                                        class_mode='categorical',
                                                        target_size=(120, 120))

    # Instantiate the ImageDataGenerator class (don't forget to set the rescale argument)
    validation_datagen = ImageDataGenerator(1.0 / 255)

    # Pass in the appropriate arguments to the flow_from_directory method
    validation_generator = validation_datagen.flow_from_directory(directory=VALIDATION_DIR,
                                                                  color_mode="grayscale",
                                                                  # batch_size=64,
                                                                  class_mode='categorical',
                                                                  target_size=(120, 120))
    return train_generator, validation_generator


def create_model():
    model = Sequential([
            Conv2D(filters=32, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            Dropout(0.3),
            Conv2D(filters=32, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.3),
            Conv2D(filters=64, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            Conv2D(filters=64, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(filters=128, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            Dropout(0.3),
            Conv2D(filters=128, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dropout(0.3),
            Dense(2500, activation='relu'),
            Dropout(0.3),
            Dense(1500, activation='relu'),
            Dropout(0.3),
            Dense(14, activation='softmax')
        ])
    # model = Sequential([
    #     Conv2D(filters=32, kernel_size=(3, 3), padding='same', input_shape=(120, 120, 1), activation='relu'),
    #     BatchNormalization(),
    #     Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu'),
    #     BatchNormalization(),
    #     Conv2D(filters=32, kernel_size=(5, 5), padding='same', strides=(2, 2), input_shape=(120, 120, 1), activation='relu'),
    #     BatchNormalization(),
    #     Dropout(0.4),
    #
    #     Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    #     BatchNormalization(),
    #     Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    #     BatchNormalization(),
    #     Conv2D(filters=32, kernel_size=(5, 5), strides=(2, 2), padding='same', activation='relu'),
    #     BatchNormalization(),
    #     Dropout(0.4),
    #
    #     Flatten(),
    #     Dense(128, activation='relu'),
    #     BatchNormalization(),
    #     Dropout(0.4),
    #     Dense(14, activation='softmax')
    # ])
    model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])
    return model


def train_model(train_generator, validation_generator):
    # Get the untrained model
    model = create_model()
    model.summary()
    callback = tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        min_delta=0.001,
        patience=3,
        mode='max'
    )
    # Train the model
    # Note that this may take some time.
    history = model.fit(train_generator,
                        batch_size=36,
                        epochs=15,
                        verbose=1,
                        validation_data=validation_generator,
                        callbacks=[callback]
                        )
    model.save('.\\Model\\model.h5')
    # -----------------------------------------------------------
    # Retrieve a list of list results on training and test data
    # sets for each training epoch
    # -----------------------------------------------------------

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))  # Get number of epochs
    # ------------------------------------------------
    # Plot training and validation accuracy per epoch
    # ------------------------------------------------
    plt.plot(epochs, acc, 'r', "Training Accuracy")
    plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
    plt.title('Training and validation accuracy')
    plt.show()
    print("")
    # ------------------------------------------------
    # Plot training and validation loss per epoch
    # ------------------------------------------------
    plt.plot(epochs, loss, 'r', "Training Loss")
    plt.plot(epochs, val_loss, 'b', "Validation Loss")
    plt.show()


def main():
    # TRAINING_DIR, VALIDATION_DIR = load_data()
    TRAINING_DIR = ".\\Classify\\Training\\"
    VALIDATION_DIR = ".\\Classify\\Validation\\"
    train_generator, validation_generator = train_val_generators(TRAINING_DIR, VALIDATION_DIR)
    create_model()
    train_model(train_generator, validation_generator)


if __name__ == '__main__':
    main()
