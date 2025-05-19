from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class MaterialsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="pave1.r.2015@mail.ru")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course Description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            video_url="https://youtube.com/test",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тестирование создания курса"""
        data = {
            "title": "Test Course",
            "description": "Test Course Description",
            "owner": self.user.pk,
        }
        response = self.client.post("/courses/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_courses(self):
        """Тестирование получения списка курсов"""
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail(self):
        """Тестирование получения детальной информации о курсе"""
        response = self.client.get(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_courses(self):
        """Тестирование изменения курса"""
        data = {"title": "Updated Course", "description": "Updated Course Description"}
        response = self.client.put(f"/courses/{self.course.pk}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_courses(self):
        """Тестирование удаления курса"""
        response = self.client.delete(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            "title": "Test Lesson",
            "description": "Test Lesson Description",
            "video_url": "https://youtube.com/test",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post("/lessons/create/", data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lessons(self):
        """Тестирование получения списка уроков"""
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson_detail(self):
        """Тестирование получения детальной информации о уроке"""
        response = self.client.get(f"/lessons/{self.lesson.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lessons(self):
        """Тестирование изменения урока"""
        data = {"title": "Updated Lesson",
                "description": "Updated Lesson Description",
                "video_url": "https://youtube.com/updated",
                "course": self.course.pk,
                "owner": self.user.pk,
                }
        response = self.client.put(f"/lessons/{self.lesson.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lessons(self):
        """Тестирование удаления урока"""
        response = self.client.delete(f"/lessons/{self.lesson.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscribe_to_lesson(self):
        """Тестирование подписки на урок"""
        data = {
            "course": self.course.pk,
            # "user": self.user.pk,
        }
        response = self.client.post("/subscription/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка добавлена")
