from rest_framework import serializers
from .models import ParsedPage

class ParsedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedPage
        fields = '__all__'
