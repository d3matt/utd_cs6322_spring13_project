from django.db import models

class Paper_Author(models.Model):
    name = models.CharField(max_length=80)

class Citation_Author(models.Model):
    name = models.CharField(max_length=80)

class Citation(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Citation_Author)
    #if we want to put the other fields in the DB, add it here...

class Paper(models.Model):
    title = models.CharField(max_length=255)
    #still not sure if this relationship is the best...  C'est la vie
    authors = models.ManyToManyField(Paper_Author)
    #if we want to put the abstract in the DB, add it here...
