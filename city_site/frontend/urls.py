# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from city_app.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
]
