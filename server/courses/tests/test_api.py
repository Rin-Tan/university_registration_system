
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from courses.models import Course
from datetime import time

class CourseListCreateTest(APITestCase):

    def setUp(self):
        self.url = reverse('course-view-create')

    def create_course_data(self, code="CS101", title="Test Course"):
        return {
            "course_code": code,
            "title": title,
            "capacity": 30,
            "units": 3,
            "day_of_week": "Monday",
            "location": "Room 101",
            "start_time": time(9, 0),
            "end_time": time(10, 30),
        }

    def test_get_course_list(self):
        # Arrange
        Course.objects.create(**self.create_course_data(code="CS101", title="Course 1"))
        Course.objects.create(**self.create_course_data(code="CS102", title="Course 2"))

        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_course_success(self):
        # Arrange
        data = self.create_course_data(code="CS103", title="New Course")

        # Act
        response = self.client.post(self.url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course_code'], "CS103")
        self.assertEqual(response.data['title'], "New Course")

    def test_create_course_missing_field(self):
        # Arrange: حذف course_code که ضروری است
        data = self.create_course_data()
        data.pop("course_code")

        # Act
        response = self.client.post(self.url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course_code', response.data)


class CourseRetrieveUpdateDestroyTest(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            course_code="CS201",
            title="Existing Course",
            capacity=30,
            units=3,
            day_of_week="Tuesday",
            location="Room 202",
            start_time=time(10,0),
            end_time=time(11,30),
        )
        self.url = reverse('course-update-destroy', kwargs={'pk': self.course.id})

    def test_retrieve_course(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_code'], self.course.course_code)

    def test_update_course(self):
        data = {
            "course_code": "CS201",
            "title": "Updated Course",
            "capacity": 35,
            "units": 4,
            "day_of_week": "Tuesday",
            "location": "Room 202",
            "start_time": time(10,0),
            "end_time": time(11,30),
            "prerequisites": []
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course")
        self.assertEqual(self.course.capacity, 35)

    def test_delete_course(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())
