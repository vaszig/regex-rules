import re

from django import forms
from django.core.exceptions import ValidationError


TYPE_OF_SEARCH_CHOICES = [
        ('contains', 'Default(contains the pattern)'),
        ('match_in', 'In(includes a whole word)'),
        ('match_out', 'Out(excludes a whole word)'),
    ]


class ResultsForm(forms.Form):
    """Form for validating user's input. Column is the column to filter and pattern the regex pattern."""

    type_of_search = forms.ChoiceField(choices=TYPE_OF_SEARCH_CHOICES, label='Enter type of search')
    column = forms.CharField(max_length=50, label='Enter column to apply regex')
    pattern = forms.CharField(max_length=100, label='Enter regex pattern')

    def clean_pattern(self):
        """Validates that the given pattern is a valid regex."""
        
        regex_pattern = self.cleaned_data['pattern']
        try:
            re.compile(regex_pattern)
        except re.error as e:
            raise ValidationError(e)

        return regex_pattern