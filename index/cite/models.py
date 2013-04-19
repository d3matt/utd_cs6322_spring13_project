from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __unicode__(self):
        return self.name

class Paper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    filename = models.CharField(max_length=255, unique=True, blank=True, null=True, default=None)
    authors = models.ManyToManyField(Author)
    citations = models.ManyToManyField('self', symmetrical=False)
    length = models.IntegerField()
    #if we want to put the abstract in the DB, add it here...
    def __unicode__(self):
        return self.title

class Token(models.Model):
    stem = models.CharField(max_length=40, unique=True)
    #not sure if we need this field, though it might be useful
    total = models.IntegerField()
    def __unicode__(self):
        return self.stem

class PaperToken(models.Model):
    """many-many relationship of paper<->token with a count"""
    num = models.IntegerField()
    paper = models.ForeignKey(Paper)
    token = models.ForeignKey(Token)
    def __unicode__(self):
        return "%s %s %d" % (unicode(self.token), unicode(self.paper), self.num)
