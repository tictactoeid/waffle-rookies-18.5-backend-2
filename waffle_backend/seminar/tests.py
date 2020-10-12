from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import json
import random
from user.models import InstructorProfile, ParticipantProfile
from seminar.serializers import InstructorsOfSeminarSerializer, ParticipantsOfSeminarSerializer, SeminarSerializer
from seminar.models import UserSeminar, Seminar
# Create your tests here.

class PostSeminarTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='testUserInst').key
        self.instructor_user = User.objects.get(username='testUserInst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='testUserPart').key
        self.participant_user = User.objects.get(username='testUserPart')

    def test_post_seminar(self):
        count = Seminar.objects.count()
        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)
        count_again = Seminar.objects.count()
        self.assertEqual(count+1, count_again)

    def test_post_seminar_requesting_user_participant(self):
        count = Seminar.objects.count()
        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)

    def test_post_seminar_incomplete_request(self):
        count = Seminar.objects.count()
        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": "Hello",
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": "Hello",
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "1130",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "FAKE",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = Seminar.objects.count()
        self.assertEqual(count, count_again)


class PutSeminarSeminarIdTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='testUserInst').key
        self.instructor_user = User.objects.get(username='testUserInst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='testUserPart').key
        self.participant_user = User.objects.get(username='testUserPart')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor2_token = 'Token ' + Token.objects.get(user__username='testUserInst2').key
        self.instructor2_user = User.objects.get(username='testUserInst2')

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.id = response.json()["id"]

    def test_put_seminar_seminarid(self):
        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 60,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 60)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backendSeminar",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backendSeminar")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "False",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], False)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 5,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 5)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "12:00",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "12:00:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

    def test_put_seminar_seminarid_not_an_instructor(self):
        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "12:00",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(
            '/api/v1/seminar/' + str(self.id) + '/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "12:00",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor2_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class GetSeminarTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor1_token = 'Token ' + Token.objects.get(user__username='testUserInst').key
        self.instructor1_user = User.objects.get(username='testUserInst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='testUserPart').key
        self.participant_user = User.objects.get(username='testUserPart')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor2_token = 'Token ' + Token.objects.get(user__username='testUserInst2').key
        self.instructor2_user = User.objects.get(username='testUserInst2')

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor1_token
        )
        self.id_1 = response.json()["id"]

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "android",
                "capacity": 30,
                "count": 3,
                "time": "15:30",
                "online": "False",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor2_token
        )
        self.id_2 = response.json()["id"]


    def test_get_seminar_seminarid(self):
        response = self.client.get(
            '/api/v1/seminar/' + str(self.id_1) + '/',
            HTTP_AUTHORIZATION=self.instructor2_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.get(
            '/api/v1/seminar/' + str(self.id_1) + '/',
            HTTP_AUTHORIZATION=self.instructor1_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        response = self.client.get(
            '/api/v1/seminar/' + str(self.id_1) + '/',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

    def test_get_seminar_seminarid_not_exist(self):
        seminar = True
        id = 1
        while seminar: # 해당 id를 갖는 seminar가 존재하지 않는 id 찾기.
            id += 1
            seminar = Seminar.objects.filter(id = id)

        response = self.client.get(
            '/api/v1/seminar/' + str(id) + '/',
            HTTP_AUTHORIZATION=self.instructor2_token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_seminar_name(self):
        response = self.client.get(
            '/api/v1/seminar/',
            {'name': 'backend'},
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        backendSeminar = Seminar.objects.filter(name = "backend")
        backendSeminarSerializer = SeminarSerializer(backendSeminar, many=True)
        self.assertIsNotNone(data)

        self.assertIn("id", data[0])
        self.assertEqual(data[0]["name"], "backend")
        self.assertEqual(data[0]["capacity"], 50)
        self.assertEqual(data[0]["count"], 4)
        self.assertEqual(data[0]["time"], "11:30:00")
        self.assertEqual(data[0]["online"], True)

        instructors = data[0]["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data[0]["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

    def test_get_seminar_order(self):
        response = self.client.get(
            '/api/v1/seminar/',
            {'order': 'earliest'},
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsNotNone(data)

        self.assertIn("id", data[0])
        self.assertEqual(data[0]["name"], "backend")
        self.assertEqual(data[0]["capacity"], 50)
        self.assertEqual(data[0]["count"], 4)
        self.assertEqual(data[0]["time"], "11:30:00")
        self.assertEqual(data[0]["online"], True)

        instructors = data[0]["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data[0]["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

        self.assertIn("id", data[1])
        self.assertEqual(data[1]["name"], "android")
        self.assertEqual(data[1]["capacity"], 30)
        self.assertEqual(data[1]["count"], 3)
        self.assertEqual(data[1]["time"], "15:30:00")
        self.assertEqual(data[1]["online"], False)

        instructors = data[1]["instructors"]

        userseminar = UserSeminar.objects.filter(seminar = data[1]["id"], role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)

class PostSeminarSeminaridUserTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='testUserInst').key
        self.instructor_user = User.objects.get(username='testUserInst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='testUserPart').key
        self.participant_user = User.objects.get(username='testUserPart')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant2_token = 'Token ' + Token.objects.get(user__username='testUserPart2').key
        self.participant2_user = User.objects.get(username='testUserPart2')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart3",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant3_token = 'Token ' + Token.objects.get(user__username='testUserPart3').key
        self.participant3_user = User.objects.get(username='testUserPart3')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor2_token = 'Token ' + Token.objects.get(user__username='testUserInst2').key
        self.instructor2_user = User.objects.get(username='testUserInst2')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "Inst",
                "password": "password",
                "first_name": "Jimi",
                "last_name": "Jung",
                "email": "test1@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor333_token = 'Token ' + Token.objects.get(user__username='Inst').key
        self.instructor333_user = User.objects.get(username='Inst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "Inst4",
                "password": "password",
                "first_name": "Jimi",
                "last_name": "Jung",
                "email": "test1@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor4_token = 'Token ' + Token.objects.get(user__username='Inst4').key
        self.instructor4_user = User.objects.get(username='Inst4')

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.id = response.json()["id"]

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "android",
                "capacity": 1,
                "count": 3,
                "time": "15:30",
                "online": "False",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor2_token
        )
        self.id_2 = response.json()["id"]

        self.client.post(
            '/api/v1/seminar/' +str(self.id_2)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant2_token
        )
        self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )


    def test_post_seminar_seminarid_user_participant(self):
        count = UserSeminar.objects.filter(seminar=self.id, role='participant').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant3_token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        participants = data["participants"]
        userseminar = UserSeminar.objects.filter(seminar = data["id"], role = 'participant')
        participants_serializer = ParticipantsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(participants)
        count_again = userseminar.count()
        self.assertEqual(count+1, count_again)



    def test_post_seminar_seminarid_user_instructor(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'instructor').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "instructor",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor4_token
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

        instructors = data["instructors"]
        userseminar = UserSeminar.objects.filter(seminar = self.id, role = 'instructor')
        instructors_serializer = InstructorsOfSeminarSerializer(userseminar, many=True)
        self.assertIsNotNone(instructors)
        self.assertEqual(instructors, instructors_serializer.data)
        count_again = userseminar.count()
        self.assertEqual(count+1, count_again)

    def test_post_seminar_seminarid_user_already_participating_in(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'instructor').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "instructor",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = UserSeminar.objects.filter(seminar = self.id, role = 'instructor').count()
        self.assertEqual(count, count_again)

    def test_post_seminar_seminarid_user_with_wrong_role(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'instructor').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        count_again = UserSeminar.objects.filter(seminar = self.id, role = 'instructor').count()
        self.assertEqual(count, count_again)

    def test_post_seminar_seminarid_user_already_an_instructor(self):
        count = UserSeminar.objects.filter(seminar = self.id_2, role = 'instructor').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id_2)+'/user/',
            json.dumps({
                "role": "instructor",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = UserSeminar.objects.filter(seminar = self.id_2, role = 'instructor').count()
        self.assertEqual(count, count_again)

    def test_post_seminar_seminarid_user_full_capacity(self):
        count = UserSeminar.objects.filter(seminar = self.id_2, role = 'participant').count()
        response = self.client.post(
            '/api/v1/seminar/' +str(self.id_2)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant2_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        count_again = UserSeminar.objects.filter(seminar = self.id_2, role = 'participant').count()
        self.assertEqual(count, count_again)

class DeleteSeminarTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='testUserInst').key
        self.instructor_user = User.objects.get(username='testUserInst')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='testUserPart').key
        self.participant_user = User.objects.get(username='testUserPart')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserPart2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test1234@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant2_token = 'Token ' + Token.objects.get(user__username='testUserPart2').key
        self.participant2_user = User.objects.get(username='testUserPart2')

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "testUserInst2",
                "password": "password",
                "first_name": "Jimin",
                "last_name": "Jung",
                "email": "test111@snu.ac.kr",
                "role": "instructor",
                "year": 3,
                "company": "대학원"
            }),
            content_type='application/json'
        )
        self.instructor2_token = 'Token ' + Token.objects.get(user__username='testUserInst2').key
        self.instructor2_user = User.objects.get(username='testUserInst2')

        response = self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "backend",
                "capacity": 50,
                "count": 4,
                "time": "11:30",
                "online": "True",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.id = response.json()["id"]

        self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )

    def test_delete_seminar_seminarid_user(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()

        response = self.client.delete(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_again = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()
        self.assertEqual(count, count_again)
        userseminar = UserSeminar.objects.get(user = self.participant_user)
        self.assertEqual(userseminar.is_active, False)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

    def test_delete_seminar_seminarid_user_not_participating_in(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()

        response = self.client.delete(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant2_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_again = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()
        self.assertEqual(count, count_again)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "backend")
        self.assertEqual(data["capacity"], 50)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["time"], "11:30:00")
        self.assertEqual(data["online"], True)

    def test_delete_seminar_seminarid_user_instructor(self):
        count = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()

        response = self.client.delete(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        count_again = UserSeminar.objects.filter(seminar = self.id, role = 'participant').count()
        self.assertEqual(count, count_again)

    def test_delete_seminar_seminarid_seminar_not_exists(self):
        seminar = True
        id = 1
        while seminar: # 해당 id를 갖는 seminar가 존재하지 않는 id 찾기.
            id += 1
            seminar = Seminar.objects.filter(id = id)

        response = self.client.delete(
            '/api/v1/seminar/' +str(id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_seminar_seminarid_user_drop_and_participate_again(self):
        response = self.client.delete(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            '/api/v1/seminar/' +str(self.id)+'/user/',
            json.dumps({
                "role": "participant",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
