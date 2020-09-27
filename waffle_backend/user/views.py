from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from user.serializers import UserSerializer
from user.models import ParticipantProfile, InstructorProfile
from seminar.models import UserSeminar

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(), )
        return self.permission_classes

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = request.data.get('role')
        university = request.data.get('university')
        company = request.data.get('company')
        year = request.data.get('year')
        seminar = request.data.get('seminar')

        if year != None:
            if type(year) != int or year < 0:
                return Response({"error": "Your year should be 0 or a positive integer."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()  # serializer.save(): instance 존재하면 serializers.py의 create(), 없으면 update() 호출
            # print('user')

            if role == 'participant':
                profile = ParticipantProfile(user=user, university=university)
                profile.save()
                userseminar = UserSeminar(user=user, role=role, seminar=seminar)
                userseminar.save()
                # print('role')

            elif role == 'instructor':
                profile = InstructorProfile(user=user, company=company, year=year)
                profile.save()
                userseminar = UserSeminar(user=user, role=role, seminar=seminar)
                userseminar.save()
                # print('role')

            else:
                return Response({"error": "Your role should be 'participant' or 'instructor'."},
                                status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:# as e:
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            #print("Error:" + str(e))

        login(request, user)

        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PUT'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            data = self.get_serializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data)

        return Response({"error": "Wrong username or wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response()

    def retrieve(self, request, pk=None):
        #print('retrieve')
        user = request.user if pk == 'me' else self.get_object()
        return Response(self.get_serializer(user).data)

    def update(self, request, pk=None): # PUT /api/v1/user/me/
        print('update')
        if pk != 'me':
            return Response({"error": "Can't update other Users information"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user

        print(hasattr(user, 'participant'))
        print(hasattr(user, 'instructor'))
        '''try:
            profile = ParticipantProfile(user=user)
            print('participant')
        except DoesNotExistError:
            profile = InstructorProfile(user=user)
            print('instructor')'''
        #elif user.instructor:
        #    profile = InstructorProfile(user=user)
        #    print('instructor')

        try:
            user.instructor
        except ObjectDoesNotExist:
            print("no inst")
        try:
            user.participant
        except ObjectDoesNotExist:
            print("no par")

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data)
