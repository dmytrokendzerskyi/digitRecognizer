from django.http import JsonResponse
from tensorflow import keras
from rest_framework.decorators import api_view
from core.serializers import *
from PIL import Image
from io import BytesIO
import cv2
import base64
import numpy as np
import json
from . import serializers

model = keras.models.load_model('core/ai_model/digitRecognizer.h5');
Categories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
width = 28
height = 28

@api_view(['POST'])
def recognizeImage(request) :
	response = {}
	body_unicode = request.body.decode('utf-8')
	body = json.loads(body_unicode)

	image_serializer = DigitImageSerializer(data=body)
	image_serializer.is_valid(raise_exception=True)
	
	image = readb64(image_serializer.validated_data.get('image'))
	# remove not needed space
	image = truncateImage(image)

	# if image.shape[0] < 3 :
	# 	raise ApiException("Image doesn't contain digit") 

	# rescale image
	image = cv2.resize(image, (width, height))
	image = image / 255.0
	array = np.array(image).reshape(-1, width, height, 1)
	print(image.shape)

	prediction = model.predict(array)
	print('Predictions: ',np.around(prediction, decimals=3))

	response['status'] = 'success'
	response['digit'] = Categories[np.argmax(prediction)]

	return JsonResponse(response)


def truncateImage(image):
	while(image.shape[0] >= 2) :
		contentExist = False
		size = image.shape[1]
		for i in range(size) :
			if image[0][i] != 255.0 or image[i][0] != 255.0 or image[size-1][size-i-1] != 255.0 or image[size-i-1][size-1] != 255.0 :
				contentExist = True
		if contentExist :
			break
		else :
			image = image[1:size-2, 1:size-2]

	return image


def readb64(base64_string):
    sbuf = BytesIO()
    imageData = base64.b64decode(base64_string)
    pimg = Image.open(BytesIO(imageData))
    # set white backgroud
    pimg = Image.composite(pimg, Image.new('RGB', pimg.size, 'white'), pimg)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_BGR2GRAY)
