from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from seminar.models import Seminar, UserSeminar
from seminar.serializers import SeminarSerializer, InstructorProfileSerializer
from user.models import InstructorProfile
# Create your views here.

class SeminarViewSet(viewsets.GenericViewSet):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer
    permission_classes = (IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(), )
        return self.permission_classes

    # @action(detail=False, methods=['POST'])
    def create(self, request):
        user = request.user
        #seminar =
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not hasattr(user, 'instructor'):
            return Response({"error": "Only instructors can use this method."}, status=status.HTTP_403_FORBIDDEN)

        '''name = request.data.get('name')
        capacity = request.data.get('capacity')
        count = request.data.get('count')
        time = request.data.get('time')
        online = request.data.get('online')'''

        #print(1)
        #seminar = Seminar(name = name, capacity = capacity, count = count, time = time, online = online)


        seminar = Seminar.objects.create(**serializer.validated_data)
        userseminar = UserSeminar.objects.create(user=user, seminar=seminar)
        #print(userseminar)
        #print(seminar)

        #print(2)
        #seminar.instructors = user.instructor.objects.get(id)
        #seminar.save()
        #InstructorProfile.objects.create(user = user)#, seminar = seminar)

        #serializer.save(**serializer.validated_data, instructors = InstructorProfileSerializer(user.instructor))
        #print(serializer.data)
        #print(serializer)
        #UserSeminar.objects.create(user = user, seminar = seminar)

        #serializer = self.get_serializer(seminar, data=request.data)
        #serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        seminar = self.get_object()

        if not seminar:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not hasattr(user, 'instructor'):
            return Response({"error": "Only instructors can use this method."}, status=status.HTTP_403_FORBIDDEN)

        userseminar = UserSeminar.Object.filter(seminar = seminar)

        if not userseminar.object.filter(user):
            return Response({"error": "Only instructors can use this method."}, status=status.HTTP_403_FORBIDDEN)

        capacity = request.data.get('capacity')
        capacity = int(capacity)


        serializer.update(seminar, serializer.validated_data)
        return Response(serializer.data, status = status.HTTP_200_OK)


