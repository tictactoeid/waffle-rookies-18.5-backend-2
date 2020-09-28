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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not hasattr(user, 'instructor'):
            return Response({"error": "Only instructors can use this method."}, status=status.HTTP_403_FORBIDDEN)

        '''name = request.data.get('name')
        capacity = request.data.get('capacity')
        count = request.data.get('count')
        time = request.data.get('time')
        online = request.data.get('online')'''


        #seminar = Seminar(name = name, capacity = capacity, count = count, time = time, online = online)
        #userseminar = UserSeminar(user=user, seminar = seminar)

        seminar = Seminar.objects.create(**serializer.validated_data, instructors=user.instructor)
        InstructorProfile.objects.create(user = user, seminar = seminar)
        #serializer.save(**serializer.validated_data, instructors = InstructorProfileSerializer(user.instructor))
        #print(serializer.data)
        #print(serializer)
        #UserSeminar.objects.create(user = user, seminar = seminar)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

    #def update(self, request, pk=None):




