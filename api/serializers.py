import re

from rest_framework import serializers
from .models import Brand, Rule
        

class RuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rule
        fields = '__all__'

    def validate_pattern(self, value):
        """Validates that the given pattern is a valid regex."""
    
        try:
            re.compile(value)
        except re.error as e:
            raise serializers.ValidationError(e)
        return value


class BrandSerializer(serializers.ModelSerializer):
    
    rules = RuleSerializer(read_only=True, many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'rules']