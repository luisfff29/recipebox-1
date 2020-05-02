from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    description = models.TextField()
    prep_time = models.CharField(max_length=20)
    cook_time = models.CharField(max_length=20)
    ingredients = models.TextField()
    instructions = models.TextField()
    serves = models.CharField(max_length=20)

    def __str__(self):
        return self.title
