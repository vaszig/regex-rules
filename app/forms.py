import re

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from api.models import Rule


class ResultsForm(ModelForm):
    """Form for validating user's input. Column is the column to filter and pattern the regex pattern."""

    class Meta:
        model = Rule
        fields = ['type_of_search', 'column', 'pattern']

    def validate_pattern(self, value):
        """Validates that the given pattern is a valid regex."""
        
        try:
            re.compile(value)
        except re.error as e:
            return e
        return value
    
    def clean_pattern(self):
        regex_pattern = self.cleaned_data['pattern']
        try:
            re.compile(regex_pattern)
        except re.error as e:
            raise ValidationError(e)

        return regex_pattern
