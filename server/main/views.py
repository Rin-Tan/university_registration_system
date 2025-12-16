from django.shortcuts import render
from django.views import View
def dashboard(request):
    return render(request, 'dashboard.html')

def student_unit_management(request):
    return render(request, 'student_unit_management.html')

class StudentCourseView(View):
    def get(self, request):
        return render(request, 'studentCourses.html')

class LoginRenderView(View):
    def get(self, request):
        return render(request, 'login.html')