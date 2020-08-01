from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)


class Department(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)


class City(models.Model):
    population = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)

