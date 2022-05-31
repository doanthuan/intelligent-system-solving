from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
import numpy as np

model = Sequential([
    Dense(100, activation='relu', input_dim=3),
    Dense(500, activation='relu'),
    Dense(1, activation='softmax'),
])
model.compile(loss='binary_crossentropy',
              optimizer=SGD(), metrics=['accuracy'])

data_train = [
    [1, 2, 3],
    [4, 5, 6]
]

print(np.asarray(data_train))

model.fit(np.asarray(data_train), np.asarray([[1], [0]]))

print("trigger")
