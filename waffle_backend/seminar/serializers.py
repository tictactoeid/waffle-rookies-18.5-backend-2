from seminar.models import Seminar, UserSeminar
from rest_framework import serializers
from user.models import InstructorProfile, ParticipantProfile
from django.core.exceptions import ObjectDoesNotExist

class InstructorProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    joined_at = serializers.SerializerMethodField()

    class Meta:
        model = UserSeminar # User?
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at'
        )
    def get_id(self, userseminar):
        return userseminar.user.id
    def get_username(self, userseminar):
        return userseminar.user.username
    def get_email(self, userseminar):
        return userseminar.user.email
    def get_first_name(self, userseminar):
        return userseminar.user.first_name
    def get_last_name(self, userseminar):
        return userseminar.user.last_name

    def get_joined_at(self, userseminar):
        '''if context:
            print(context)
        #print('get_joined_at() called')
        #print(profile)
        user = profile.user
        #print(user)
        userseminar = user.userseminar
        #print(userseminar)'''
        print(userseminar)
        print(userseminar.user.userseminar)
        return userseminar.joined_at
        #return userseminar

        #print(userseminar)
        #print(userseminar.joined_at)
        #return userseminar.joined_at

        #user = profile.user
        #userseminar = UserSeminar.objects.filter(user = user)
        #return userseminar.joined_at



class ParticipantProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    joined_at = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    dropped_at = serializers.SerializerMethodField()

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
            'dropped_at'
        )
    def get_id(self, userseminar):
        return userseminar.user.id
    def get_username(self, userseminar):
        return userseminar.user.username
    def get_email(self, userseminar):
        return userseminar.user.email
    def get_first_name(self, userseminar):
        return userseminar.user.first_name
    def get_last_name(self, userseminar):
        return userseminar.user.last_name

    def get_joined_at(self, userseminar):
        return userseminar.joined_at

        #print(userseminar)
        #print(userseminar.joined_at)
        #return userseminar.joined_at

    def get_is_active(self, userseminar):
        return userseminar.is_active

    def get_dropped_at(self, userseminar):
        return userseminar.dropped_at


class SeminarSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    capacity = serializers.IntegerField()
    count = serializers.IntegerField()
    time = serializers.TimeField()
    online = serializers.BooleanField(default = True)

    instructors = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    #instructors = InstructorProfileSerializer(read_only=True, many=True, required=False)
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
        userseminar = UserSeminar.objects.filter(seminar = seminar, role = 'instructor')#[0] # [0] 빼기
        #user = userseminar.user
        try:
            #profile = user.instructor
            return InstructorProfileSerializer(userseminar, many=True).data # many = True
        except ObjectDoesNotExist:
            return None

    def get_participants(self, seminar):
        userseminar = UserSeminar.objects.filter(seminar = seminar, role = 'participant')# [0]
        #user = userseminar.user
        try:
            #profile = user.participant
            return ParticipantProfileSerializer(userseminar, many=True).data
        except ObjectDoesNotExist:
            return None

    '''def get_instructors(self, seminar):
        print('seminarserializer')
        print(seminar)
        #print(seminar[0])
        #self.context['seminar_id'] = seminar.id
        #user = request.user


        #id = self.context['seminar_id']
        #id = seminar.id
        #userseminar = UserSeminar.objects.filter(seminar = id)
        #user = userseminar.user
        userseminar = UserSeminar.objects.filter(user = user)
        profile = InstructorProfile.objects.filter(user = user) # user=user
        return InstructorProfileSerializer(profile, many=True).data

        
        us = seminar.userseminar.all()
        profiles = us.filter(user.instructors = )
        userseminar = seminar.userseminar
        print(userseminar)
        profile = userseminar.user.instructor
        return profile'''

   #def get_participants(self, seminar):
   #     userseminar = UserSeminar.objects.filter(seminar = seminar)
   #     profile = userseminar.user.participants
   #     return profile

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
            raise serializers.ValidationError("You should type seminar's name.")
        else:
            return value

    def create(self, validated_data):  # create(self, validated_Data)
        seminar = Seminar.objects.create(**validated_data)
        return seminar

#   def create(self, seminar):
        #seminar.save()
        #return seminar
        #if inst:
        #    validated_data['instructors'] = inst
        #print(validated_data)
        #print(object)


    def update(self, instance, validated_data):
        print(validated_data)
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

'''
class UserSeminarSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSeminar
        fields = (
            'id',

        )'''

