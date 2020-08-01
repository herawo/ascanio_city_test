from django.shortcuts import render
from rest_framework import viewsets
from city_app.models import City
from city_app.serializers import CitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.


class CityViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]

    def get_queryset(self):
        filters = {}
        qs = self.queryset
        # self.request.GET is immutable so a copy has to be done to remove empty fields
        get_instructions = deepcopy(self.request.GET)
        for key, val in deepcopy(get_instructions).items():
            if not val:
                get_instructions.pop(key)
        for key, value in get_instructions.items():
            return qs.filter(Q(name__icontains=value) | Q(moderated=False))


    