from rest_framework import serializers
from city_app.models import City


class ZipCodeField(serializers.Field):
    def to_representation(self, value):
        zip_code_dict = {}
        for zip_code in value.zip_codes.all():
            zip_code_dict.update({zip_code.id: zip_code.value})
        return zip_code_dict



class CitySerializer(serializers.ModelSerializer):

    zip_codes_values = ZipCodeField(source='*')

    class Meta:
        model = City
        fields = ['name', 'population', 'zip_codes_values']