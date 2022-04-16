from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phoneNum = models.CharField(max_length=255, unique=True)
    userLogin = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    privileges = models.CharField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)
    describtion = models.CharField(max_length=255)
    foreignKeyManager = models.ForeignKey(User, on_delete=models.PROTECT, related_name="projectManager")
    foreignKeyManagerRisk = models.ForeignKey(User, on_delete=models.PROTECT, related_name="riskManager")
    members = models.ManyToManyField(User, related_name="members")


class Phase(models.Model):
    name = models.CharField(max_length=255)
    describtion = models.CharField(max_length=255) # TODO: rename THIS
    participants = models.ManyToManyField(User, related_name="participants")
    dateFrom = models.DateField()
    dateTo = models.DateField()
    foreignKeyProject = models.ForeignKey(Project, on_delete=models.CASCADE)


# TODO: remove this class?
class RiskType(models.Model):
    name = models.CharField(max_length=255)
    describtion = models.CharField(max_length=255)
    effects = models.CharField(max_length=255)


class Risk(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    threat = models.CharField(max_length=255)
    triggers = models.CharField(max_length=255)
    reactions = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    probability = models.FloatField()
    impact = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    datetime_created = models.DateField()
    foreignKeyPhase = models.ForeignKey(Phase, on_delete=models.PROTECT)
    accepted = models.BooleanField(default=False)
