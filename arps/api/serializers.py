from rest_framework import serializers
from .models import Fields, FrequentQuestions

class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = '__all__'


class FrequentQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentQuestions
        fields = '__all__'