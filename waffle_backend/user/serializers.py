from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import ParticipantProfile, InstructorProfile

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    #role = serializers.CharField(allow_blank=False)
    #university = serializers.CharField(allow_blank=True, required=False)
    #company=serializers.CharField(allow_blank=True, required=False)
    #year=serializers.IntegerField(allow_null=True,required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'last_login',
            'date_joined',
            #'role',
            #'university',
            #'company',
            #'year',
        )

    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if bool(first_name) ^ bool(last_name):
            raise serializers.ValidationError("First name and last name should appear together.")
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            raise serializers.ValidationError("First name or last name should not have number.")
        return data

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        #print('user')
        Token.objects.create(user=user)
        #print('token')
        return user


class ParticipantProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantProfile
        fields = (
            'user',
            'created_at',
            'updated_at',
            'university',
        )

class InstructorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstructorProfile
        fields = (
            'user',
            'created_at',
            'updated_at',
            'company',
            'year',
        )
