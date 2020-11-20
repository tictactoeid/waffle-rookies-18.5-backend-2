from seminar.models import Seminar, UserSeminar
from rest_framework import serializers
from user.models import InstructorProfile, ParticipantProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class InstructorProfileSerializer(serializers.ModelSerializer):

    charge = serializers.SerializerMethodField()

    class Meta:
        model = InstructorProfile # User?
        fields = (
            'id',
            'company',
            'year',
            'charge',
        )

    def get_charge(self, profile):
        seminars = profile.user.userseminar.filter(role='instructor').last()
        if seminars:
            return InstructorSeminarSerializer(seminars, context=self.context, many=True).data
        else:
            return None

class ParticipantProfileSerializer(serializers.ModelSerializer):

    accepted = serializers.BooleanField(default=True, required=False)
    seminars = serializers.SerializerMethodField(read_only=True)
    #user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ParticipantProfile
        fields = (
            'id',
            'university',
            'accepted',
            'seminars',
            #'user_id',
        )

    def get_seminars(self, profile):
        seminars = profile.user.userseminar.filter(role='participant')
        #user = User.objects.filter(participant = profile.id)
        #seminars = UserSeminar.objects.filter(user = user, role = 'participant')
        return ParticipantSeminarSerializer(seminars, context=self.context, many=True).data

class InstructorSeminarSerializer(serializers.ModelSerializer): # InstructorProfileSerializer에서 접근하는 seminar 정보
    #joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source = 'seminar.id')
    name = serializers.CharField(source = 'seminar.name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at',
            'id',
            'name',
        )


class ParticipantSeminarSerializer(serializers.ModelSerializer): # ParticipantProfileSerializer에서 접근하는 seminar 정보
    #joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source = 'seminar.id')
    name = serializers.CharField(source = 'seminar.name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at',
            'id',
            'name',
            'is_active',
            'dropped_at',
        )


class SeminarSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    capacity = serializers.IntegerField()
    count = serializers.IntegerField()
    time = serializers.TimeField()
    online = serializers.BooleanField(default = True)

    instructors = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    #instructors = InstructorProfileSerializer(many=True, required=False)
    #participants = ParticipantProfileSerializer(many=True, required=False)

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

    def get_instructors(self, seminar):
        instructors = seminar.userseminar.filter(role = 'instructor')
        try:
            return InstructorsOfSeminarSerializer(instructors, context=self.context, many=True).data
        except ObjectDoesNotExist:
            return None

    def get_participants(self, seminar):
        participants = seminar.userseminar.filter(role = 'participants')
        try:
            return ParticipantsOfSeminarSerializer(participants, context=self.context, many=True).data # many = True
        except ObjectDoesNotExist:
            return None


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
            raise serializers.ValidationError("You should type seminar's name.")
        else:
            return value

    def create(self, validated_data):  # create(self, validated_Data)
        seminar = Seminar.objects.create(**validated_data)
        return seminar

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'capacity' in validated_data:
            instance.capacity = validated_data['capacity']
        if 'count' in validated_data:
            instance.count = validated_data['count']
        if 'time' in validated_data:
            instance.time = validated_data['time']
        if 'online' in validated_data:
            instance.online = validated_data['online']

        return instance

class InstructorsOfSeminarSerializer(serializers.ModelSerializer): # SeminarSerializer에서 접근하는 Instructors의 InstructorProfileSerializer 정보
    id = serializers.IntegerField(source = 'user.id')
    username = serializers.CharField(source = 'user.username')
    email = serializers.EmailField(source = 'user.email')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')

    class Meta:
        model = UserSeminar
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at',

        )

class ParticipantsOfSeminarSerializer(serializers.ModelSerializer): # SeminarSerializer에서 접근하는 Instructors의 InstructorProfileSerializer 정보
    id = serializers.IntegerField(source = 'user.id')
    username = serializers.CharField(source = 'user.username')
    email = serializers.EmailField(source = 'user.email')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')

    class Meta:
        model = UserSeminar
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at',
            'is_active',
            'dropped_at',

        )
