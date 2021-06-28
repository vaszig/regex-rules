from rest_framework import generics
from .serializers import BrandSerializer, RuleSerializer
from .models import Brand, Rule
    

class BrandsList(generics.ListCreateAPIView):
    """"View for new brands or list existing ones depending on the request method."""
    
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """"View for modifying a brand depending on the request method."""

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    lookup_field = 'id'


class RulesList(generics.ListCreateAPIView):
    """"View for new rules or list existing ones depending on the request method."""

    serializer_class = RuleSerializer
    queryset = Rule.objects.all()


class RuleDetail(generics.RetrieveUpdateDestroyAPIView):
    """"View for modifying a rule depending on the request method."""

    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    lookup_field = 'id'
