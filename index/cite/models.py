from django.db import models

#paper authors and citation authors may be in a different format
class Paper_Author(models.Model):
    name = models.CharField(max_length=80, unique=True)

class Citation_Author(models.Model):
    name = models.CharField(max_length=80, unique=True)

class Citation(models.Model):
    title = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Citation_Author)
    #if we want to put the other fields in the DB, add it here...

class Paper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    #still not sure if this relationship is the best...  C'est la vie
    authors = models.ManyToManyField(Paper_Author)
    length = models.IntegerField()
    #if we want to put the abstract in the DB, add it here...

class Token(models.Model):
    stem = models.CharField(max_length=40, unique=True)
    #not sure if we need this field, though it might be useful
    total = models.IntegerField()

class PaperToken(models.Model):
    """many-many relationship of paper<->token with a count"""
    num = models.IntegerField()
    paper = models.ForeignKey(Paper)
    token = models.ForeignKey(Token)
