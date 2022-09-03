from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import re

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=40, validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already in use.")])
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=100, allow_blank=True, required=False)

    def validate(self, data):
        if re.match(re.compile(r"[@._]*[A-Za-z]+[0-9.@-_]*"), data['username']) is None:
            raise ValidationError("Invalid username.")

        if re.match(re.compile(r"[-_.]*[a-zA-z0-9]+@[a-z]+(\.[a-z]+)"), data['email']) is None:
            raise ValidationError("Invalid email")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance