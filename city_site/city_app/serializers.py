from rest_framework import serializers
from city_app.models import City


class CitySerializer(serializers.ModelSerializer):

    zip_code_values = serializers.SerializerMethodField('get_zip_code_values')
    region = serializers.SerializerMethodField('get_region')
    department = serializers.SerializerMethodField('get_department')

    class Meta:
        model = City
        fields = ['id', 'name', 'population', 'zip_code_values', 'region', 'department']

    def get_zip_code_values(self, instance):
        return [code.value for code in instance.zip_codes.all()]

    def get_department(self, instance):
        return instance.department.name

    def get_region(self, instance):
        return instance.department.region.name