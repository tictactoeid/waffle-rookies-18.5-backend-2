import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from seminar.models import Seminar, UserSeminar
from seminar.serializers import SeminarSerializer, InstructorProfileSerializer

class SeminarViewSet(viewsets.GenericViewSet):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer
    permission_classes = (IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(), )
        return self.permission_classes

    def create(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not hasattr(user, 'instructor'):
            return Response({"error": "Only instructors can use this method."}, status=status.HTTP_403_FORBIDDEN)

        seminar = serializer.save()

        userseminar = UserSeminar.objects.create(user=user, seminar=seminar, role = 'instructor', joined_at = datetime.datetime.now())

        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk=None): # PUT /api/v1/seminar/pk/
        user = request.user
        capacity = request.data.get('capacity')

        if not (hasattr(user, 'instructor')):
            return Response({"error": "Only instructor of this seminar can update the seminar."},
                                    status=status.HTTP_403_FORBIDDEN)
        try:
            seminar = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Seminar does not exist."}, status = HTTP_404_NOT_FOUND)

        try:
            userseminar = UserSeminar.objects.get(user = user, seminar = seminar)
        except ObjectDoesNotExist:
            return Response({"error": "Only instructor of this seminar can update the seminar."},
                                    status=status.HTTP_403_FORBIDDEN)

        participants_count = UserSeminar.objects.filter(user=user, seminar=seminar, role='participant').count()
        if capacity:
            if participants_count > capacity:
                return Response({"error": "The capacity of the seminar is too small. " +
                                          "It must be bigger than {0}".format(str(participants_count))},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(seminar, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(seminar, serializer.validated_data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): #GET /api/v1/seminar/{seminar_id}/
        try:
            seminar = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Seminar does not exist."}, status = status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(seminar).data)

    def get(self, request):
        if 'name' in request.query_params:
            name = request.query_params.get('name')
        else:
            name = None

        if 'order' in request.query_params:
            order = request.query_params.get('order')
            if order == 'earliest':
                if name:
                    seminar = Seminar.objects.filter(name=name).order_by('created_at')
                else:
                    seminar = Seminar.objects.all().order_by('created_at')
            else:
                seminar = Seminar.objects.filter(name=name)
        else:
            if name:
                seminar = Seminar.objects.filter(name=name)
            else:
                seminar = Seminar.objects.all()

        data = self.get_serializer(seminar, many=True).data
        return Response(data)


    @action(methods=['POST', 'DELETE'], detail=True, url_path = 'user', url_name='user') # POST, DELETE /api/v1/seminar/{seminar_id}/user/
    def user(self, request, pk=None):
        if self.request.method == 'POST':
            return self.participate(request, pk)
        elif self.request.method == 'DELETE':
            return self.drop(request, pk)
        else:
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def participate(self, request, pk=None):
        try:
            seminar = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Seminar does not exist."}, status = status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(seminar)

        user = request.user
        role = request.data.get('role')
        if role == 'instructor':
            if hasattr(user, 'instructor'):
                try:
                    userseminar = UserSeminar.objects.filter(user=user, role=role)
                    if userseminar:
                        return Response({"error": "You are already an instructor of the seminar."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        UserSeminar.objects.create(user=user, seminar=seminar, role=role,
                                                                 joined_at=datetime.datetime.now())
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    userseminar = UserSeminar.objects.create(user=user, seminar=seminar, role=role,
                                                             joined_at=datetime.datetime.now())
                    return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({"error": "You are not an instructor."}, status=HTTP_403_FORBIDDEN)

        elif role == 'participant':
            if hasattr(user, 'participant'):
                if user.participant.accepted == False:
                    return Response({"error": "Not accepted."}, status=status.HTTP_403_FORBIDDEN)
                elif not UserSeminar.objects.filter(user=user, seminar=seminar):
                    userseminar = UserSeminar.objects.create(user=user, seminar=seminar, role = role, joined_at=datetime.datetime.now())
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "You are already participating in this seminar or dropped this seminar."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You are not a participant."}, status=status.HTTP_403_FORBIDDEN)

    # DELETE /api/v1/seminar/{seminar_id}/user/
    def drop(self, request, pk=None):
        try:
            seminar = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Seminar does not exist."}, status = status.HTTP_404_NOT_FOUND)

        user = request.user
        serializer = self.get_serializer(seminar)
        try:
            userseminar = UserSeminar.objects.get(user=user, seminar=seminar)
            if userseminar.role == 'instructor':
                return Response({'error': 'An instructor cannot drop the seminar course.'}, status = status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(serializer.data, status=status.HTTP_200_OK)

        userseminar.is_active = False
        userseminar.dropped_at = datetime.datetime.now()
        userseminar.save()

        return Response(serializer.data, status = status.HTTP_200_OK)
