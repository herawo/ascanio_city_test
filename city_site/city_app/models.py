from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)


class Department(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)


class ZipCode(models.Model):

    class Meta:
        ordering = ['value']

    value = models.CharField(max_length=10)


class City(models.Model):

    class Meta:
        ordering = ['name']

    population = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    zip_codes = models.ManyToManyField(ZipCode)

