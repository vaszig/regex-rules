from django.db import models
from django.forms.fields import ChoiceField


class Brand(models.Model):
    """Model for brands."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    """Model for regex pattern rules."""

    TYPE_OF_SEARCH_CHOICES = (
        ('contains', 'Default(contains the pattern)'),
        ('match_in', 'In(includes a whole word)'),
        ('match_out', 'Out(excludes a whole word)'),
    )

    description = models.CharField(max_length=50)
    type_of_search = models.CharField(max_length=20, choices=TYPE_OF_SEARCH_CHOICES, default='Default')
    pattern = models.CharField(max_length=100)
    column = models.CharField(max_length=50)
    brands = models.ManyToManyField('Brand', related_name='rules')

    def __str__(self):
        return f'Rule {self.description} with pattern {self.pattern}'