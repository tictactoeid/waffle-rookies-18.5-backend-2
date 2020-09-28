from django.contrib.auth.models import User
from seminar.models import Seminar, UserSeminar
from rest_framework import serializers
from user.models import InstructorProfile, ParticipantProfile

class InstructorProfileSerializer(serializers.ModelSerializer):

    joined_at = serializers.SerializerMethodField()

    class Meta:
        model = InstructorProfile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at'
        )
        def get_joined_at(self, user):
            userseminar = UserSeminar.object.filter(user = user)
            return userseminar.joined_at

class ParticipantProfileSerializer(serializers.ModelSerializer):
    joined_at = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    dropped_at = serializers.SerializerMethodField()

    class Meta:
        model = ParticipantProfile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at',
            'is_active',
            'dropped_at'
        )

    def get_joined_at(self, user):
        userseminar = UserSeminar.object.filter(user=user)
        return userseminar.joined_at

    def get_is_active(self, user):
        userseminar = UserSeminar.object.filter(user=user)
        return userseminar.is_active

    def get_dropped_at(self, user):
        userseminar = UserSeminar.object.filter(user=user)
        return userseminar.dropped_at


class SeminarSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    capacity = serializers.IntegerField()
    count = serializers.IntegerField()
    time = serializers.TimeField()
    online = serializers.BooleanField(default = True)
    #instructors = serializers.SerializerMethodField()
    #participants = serializers.SerializerMethodField()
    instructors = InstructorProfileSerializer(read_only=True, many=True)
    participants = ParticipantProfileSerializer(many=True, required=False)

    class Meta:
        model = Seminar
        fields = (
            'id',
            'name',
            'capacity',
            'count',
            'time',
            'online',
            'instructors',
            'participants'
        )

    '''def get_instructors(self, seminar):

        seminar.userseminar.filter
        print(seminar)
        print(seminar.get('id'))
        userseminar = seminar.userseminar
        print(userseminar)
        profile = userseminar.user.instructor
        return profile

    def get_participants(self, seminar):
        userseminar = UserSeminar.objects.filter(seminar = seminar)
        profile = userseminar.user.participants
        return profile'''

    def validate_capacity(self, value):
        try:
            value = int(value)
        except TypeError:
            raise serializers.ValidationError("Capacity must be an integer.")
        else:
            if value < 0:
                raise serializers.ValidationError("Capacity must be a positive integer.")
        return value

    def validate_count(self, value):
        try:
            value = int(value)
        except TypeError:
            raise serializers.ValidationError("Count must be an integer.")
        else:
            if value < 0:
                raise serializers.ValidationError("Count must be a positive integer.")
        return value

    def validate_time(self, value):
        if not ":" in str(value):
            raise serializers.ValidationError("Time should be like 14:30.")
        else:
            print(str(value))
            hour, min, sec = str(value).split(":")
            try:
                intHour = int(hour)
                intMin = int(min)
            except TypeError:
                raise serializers.ValidationError("Hour and minute must be an integer.")
            else:
                if intHour < 0 or intHour > 23 or intMin < 0 or intMin > 59:
                    raise serializers.ValidationError("Invalid time value.")

            return value

    def validate_online(self, value):
        if value == None:
            return "True"

        elif str(value).capitalize() != "True" and str(value).capitalize() != "False":
            raise serializers.ValidationError("Online value must be True or False.")

        else:
            return value

    def validate_name(self, value):
        if value == None:
            raise serializers.ValidationError("You should type your name.")
        else:
            return value

    def create(self, validated_data, **inst):
        if inst:
            validated_data['instructors'] = inst
        return Seminar(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.count = validated_data.get('count', instance.count)
        instance.time = validated_data.get('time', instance.time)
        instance.online = validated_data.get('online', instance.online)
        return instance

'''
class UserSeminarSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSeminar
        fields = (
            'id',

        )'''

