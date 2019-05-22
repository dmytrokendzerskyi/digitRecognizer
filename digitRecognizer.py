from PIL import Image
from tensorflow import keras
from mlxtend.data import loadlocal_mnist

import os
import numpy as np
import random
import cv2

width = 28
height = 28

def create_model():
	model = keras.models.Sequential([
		keras.layers.Conv2D(32, kernel_size = 3, activation='relu', 
			input_shape = (28,28,1)),
		keras.layers.Conv2D(64, kernel_size = 3, activation='relu'),
		keras.layers.Conv2D(128, kernel_size = 5, strides = (2,2), activation='relu'),
		keras.layers.Flatten(),
		keras.layers.Dense(128, activation = 'relu'),
		keras.layers.Dense(10, activation= 'softmax')])

	model.compile(optimizer = 'adam',
				  loss = 'sparse_categorical_crossentropy',
			  	  metrics = ['accuracy'])
	return model

model = create_model()
DataDir = 'numbers-master/numbers-master' 
Categories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

training_data = []

# load first dataset from local directory numbers-master(https://github.com/kensanata/numbers)
for dir in os.listdir(DataDir):
	imageDir = os.path.join(DataDir, dir)
	for category in Categories:
		path = os.path.join(imageDir, category) # path to all directories
		class_num = Categories.index(category)
		for img in os.listdir(path):
			image = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
			image = cv2.resize(image, (width, height))
			image = image / 255.0
			training_data.append([image, class_num])

images,labels = loadlocal_mnist(images_path = 'train-images.idx3-ubyte',
								labels_path = 'train-labels.idx1-ubyte');

test_images,test_labels = loadlocal_mnist(images_path = 't10k-images.idx3-ubyte',
								labels_path = 't10k-labels.idx1-ubyte');

print(images.shape[0], 'images size')

for imageIndex in range(images.shape[0]):
	image = images[imageIndex].reshape(width, height)
	image = image / 255.0
	training_data.append([image, labels[imageIndex]])

random.shuffle(training_data)

training_features = []
training_labels = []
# add second dataset from mlxtend.data
for image, label in training_data :
	training_features.append(image)
	training_labels.append(label)

training_features = np.array(training_features).reshape(-1, width, height, 1)
print(training_features.shape)

model.fit(training_features, training_labels, epochs = 7)

model.save('digitRecognizer.h5')

test_images_set = []

for index in range(test_images.shape[0]):
	test_images_matrix = test_images[index].reshape(width, height)
	test_images_set.append(test_images_matrix / 255.0)

test_images_set = np.array(test_images_set).reshape(-1, width, height, 1)

print(test_images_set.shape, 'test images shape')
print(test_labels.shape, 'test labels shape')

test_loss,test_acc = model.evaluate(test_images_set, test_labels)

print('Test accurancy:', test_acc)

prediction = model.predict(np.array(testImage).reshape(-1, width, height, 1))

print(Categories[np.argmax(prediction)])
print(np.around(prediction, decimals=3))