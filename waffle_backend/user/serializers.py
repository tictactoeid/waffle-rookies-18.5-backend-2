from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from seminar.serializers import ParticipantProfileSerializer, InstructorProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from user.models import ParticipantProfile, InstructorProfile
from seminar.models import UserSeminar

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    participant = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    #role = serializers.SerializerMethodField(source = UserSeminar.role)
    role = serializers.ChoiceField(write_only = True, choices = ('participant', 'instructor'))
    university = serializers.CharField(allow_blank=True, required=False)
    accepted = serializers.BooleanField(default = True, required = False)
    company=serializers.CharField(allow_blank=True, required=False)
    year=serializers.IntegerField(allow_null=True,required=False)

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
            'participant',
            'instructor',
            'role',
            'university',
            'accepted',
            'company',
            'year',
        )

    def get_participant(self, user):
        if hasattr(user, 'participant'):
            return ParticipantProfileSerializer(user.participant).data
        else:
            return None

    def get_instructor(self, user):
        if hasattr(user, 'instructor'):
            return InstructorProfileSerializer(user.instructor).data
        else:
            return None


    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if bool(first_name) ^ bool(last_name):
            raise serializers.ValidationError("First name and last name should appear together.")
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            raise serializers.ValidationError("First name or last name should not have number.")

        role = data.get('role')
        if role == 'instructor':
            profileSerializer = InstructorProfileSerializer(data = data, context = self.context)
        else:
            profileSerializer = ParticipantProfileSerializer(data=data, context=self.context)
        profileSerializer.is_valid(raise_exception = True)
        return data

    @transaction.atomic
    def create(self, validated_data):
        company = validated_data.pop('company', '')
        year = validated_data.pop('year', None)
        university = validated_data.pop('university', '')
        accepted = validated_data.pop('accepted', None)
        role = validated_data.pop('role')

        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)
        if role == 'participant':
            ParticipantProfile.objects.create(user = user, university = university, accepted = accepted)
        elif role == 'instructor':
            InstructorProfile.objects.create(user = user, company = company, year = year)
        return user

'''
class ParticipantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantProfile
        fields = (
            'id',
            'created_at',
            'updated_at',
            'university',
            #'accepted',


        )

class InstructorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstructorProfile
        fields = (
            'id',
            'created_at',
            'updated_at',
            'company',
            'year',
        )'''
