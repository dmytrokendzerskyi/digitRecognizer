from rest_framework import serializers
from .models import *

class DigitImageSerializer(serializers.Serializer) :
	image = serializers.CharField(max_length = 100000)