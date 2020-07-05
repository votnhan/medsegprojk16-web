import math
from functools import partial

import tensorflow as tf
import keras.backend as K
from keras.optimizers import SGD, Adam
from keras.callbacks import ModelCheckpoint, CSVLogger, LearningRateScheduler, ReduceLROnPlateau, EarlyStopping
from keras.models import load_model

from .metrics import (dice_coefficient, dice_coefficient_loss, dice_coef, dice_coef_loss,
                            weighted_dice_coefficient_loss, weighted_dice_coefficient, 
                            dice_and_entropy_combination_loss, dice_whole_tumor, dice_tumor_core,
                            dice_enhancing_tumor)

from .model import isensee2017_model

K.common.set_image_dim_ordering('th')


def load_old_model(model_file):
    print("Loading pre-trained model")
    # rename for load model
    
    custom_objects = {'weighted_dice_coefficient_loss': weighted_dice_coefficient_loss,
                      'dice_whole_tumor': dice_whole_tumor,
                      'dice_tumor_core': dice_tumor_core,
                      'dice_enhancing_tumor': dice_enhancing_tumor}
    try:
        from keras_contrib.layers import InstanceNormalization
        custom_objects["InstanceNormalization"] = InstanceNormalization
    except ImportError:
        pass
    try:
        model = load_model(model_file, custom_objects=custom_objects)
        return model

    except ValueError as error:
        if 'InstanceNormalization' in str(error):
            raise ValueError(str(error) + "\n\nPlease install keras-contrib to use InstanceNormalization:\n"
                                          "'pip install git+https://www.github.com/keras-team/keras-contrib.git'")
        else:
            raise error


def load_old_model_with_weights(model_file, config):
    model = isensee2017_model(input_shape=config["input_shape"], n_labels=config["n_labels"],
                                n_base_filters=config["n_base_filters"], activation_name='softmax')

    model.load_weights(model_file)
    return model

