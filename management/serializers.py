from django.db.models import fields
from .models import * 
from rest_framework import serializers


class ConferenceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Conference
        fields = '__all__'


class PeopleSerializers(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'

class TalksSerializers(serializers.ModelSerializer):

    
    class Meta:
        model = Talk
        exclude = ('public', )