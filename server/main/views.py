from django.shortcuts import render
from django.views import View

def professor_courses(request):
    return render(request, 'professor_courses.html')


class StudentUnitManagerView(View):
    def get(self, request):
        return render(request, 'Student-unit-management.html')
 
   
class StudentCourseView(View):
    def get(self, request):
        return render(request, 'studentCourses.html')
    
class StudentMyCoursesView(View):
    def get(self, request):
        return render(request, 'studentMyCourses.html')

class LoginRenderView(View):
    def get(self, request):
        return render(request, 'login.html')