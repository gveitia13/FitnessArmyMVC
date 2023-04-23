from rest_framework import serializers

from app_main.models import Property, Product


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ['product']


class ProductSerializer(serializers.ModelSerializer):
    property_set = PropertySerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
