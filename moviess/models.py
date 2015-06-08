from django.db import models

class Movies(models.Model):
	name = models.CharField(max_length=30)
	director = models.CharField(max_length=30)
	rating = models.DecimalField(max_digits = 4, decimal_places = 2)
	popularity = models.DecimalField(max_digits = 5, decimal_places = 2)
	
class Genre(models.Model):
	movie = models.ForeignKey(Movies)
	genere = models.CharField(max_length=10)

class Admin(models.Model):
	name = models.CharField(max_length=30)
	authId = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name + ", " + self.authId
