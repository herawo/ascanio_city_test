from django.contrib import admin

from city_app.models import City
from city_app.models import Region
from city_app.models import Department

# Register your models here.

admin.site.register(City)
admin.site.register(Region)
admin.site.register(Department)

