from rest_framework import serializers
from .models import (
    Fields,
    FrequentQuestions,
    Plantation,
    FertilizerAddition,
    PestControl,
    Irrigation,
    Harvest,
)

class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = '__all__'


class FrequentQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentQuestions
        fields = '__all__'


class PlantationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantation
        fields = '__all__'


class FertilizerAdditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerAddition
        fields = '__all__'


class PestControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestControl
        fields = '__all__'


class IrrigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Irrigation
        fields = '__all__'

    
class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'