from django.db import models

class Artist(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Artifact(models.Model):
  artist = models.ForeignKey(Artist)
  title = models.CharField(max_length=200)

  class Meta:
    unique_together = ('artist', 'title')

  def __str__(self):
    return "%s - %s" % (self.artist, self.title)

class Critic(models.Model):
  name = models.CharField(max_length=200)
  url = models.URLField()

  def __str__(self):
    return self.name

class Category(models.Model):
  name = models.CharField(max_length=200)
  feed = models.URLField()
  critic = models.ForeignKey(Critic)

  def __str__(self):
    return "%s %s" % (self.critic, self.name)

class Review(models.Model):
  artifact = models.ForeignKey(Artifact)
  source = models.ForeignKey(Category)
  url = models.URLField()
  pub_date = models.DateField()
  description = models.TextField()
  score = models.DecimalField(max_digits=3, decimal_places=0)

  class Meta:
    unique_together = ('artifact', 'source')

  def __str__(self):
    return "%s: %s" % (self.source, self.artifact)
