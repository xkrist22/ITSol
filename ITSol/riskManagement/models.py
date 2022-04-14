import email
from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phoneNum = models.CharField(max_length=255)
    userLogin = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    privileges = models.CharField(max_length=255)


class RiskType(models.Model):
    name = models.CharField(max_length=255)
    popis = models.CharField(max_length=255)
    effects = models.CharField(max_length=255)


class Risk(models.Model):
    name = models.CharField(max_length=255)
    popis = models.CharField(max_length=255)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    probability = models.FloatField()
    state = models.CharField(max_length=255)
    price = models.PositiveBigIntegerField()
    foreignKeyType = models.ForeignKey(RiskType, on_delete=models.PROTECT)


class Project(models.Model):
    name = models.CharField(max_length=255)
    describtion = models.CharField(max_length=255)
    foreignKeyManager = models.ForeignKey(User, on_delete=models.PROTECT)
    members = models.ManyToManyField(User, related_name="projectMembers")


class Phase(models.Model):
    name = models.CharField(max_length=255)
    popis = models.CharField(max_length=255)
    foreignKeyManager = models.ForeignKey(User, on_delete=models.PROTECT)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    foreignKeyProject = models.ForeignKey(Project, on_delete=models.CASCADE)
    
