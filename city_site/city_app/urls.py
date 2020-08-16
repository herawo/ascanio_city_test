from city_app.views import CityViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'city', CityViewSet, basename='city')

app_name = 'city_app'
urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>', include(router.urls)),
]