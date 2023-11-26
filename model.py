import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorlfow.keras.layers import Input,Conv2D,Flatten,Dense
from tensorflow.keras.Models import Model

def q_model(actions = 1):
    inputs = Input(shape=(250,100,4,))

    layer1 = Conv2D(32,8,strides = 4, activation='relu')(inputs)
    layer2 = Conv2D(64,4,strides=2,activation='relu')(layer1)
    layer3 = Conv2D(64,3,strides=1,activation='relu')(layer2)

    flat = Flatten()(layer3)

    layer4 = Dense(512,activation='reliu')(flat)

    action = Dense(actions,activation='relu')(layer4)

    model = Model(inputs = inputs, output=action)
    
    return Model