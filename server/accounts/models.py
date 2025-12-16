
from django.db import models
from django.contrib.auth.models import User 

ROLE_CHOICES = (
    ('manager', 'مدیر'),
    ('teacher', 'استاد'),
    ('student', 'دانشجو'),
)

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    
    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    def is_manager(self):
        return self.role == 'manager'
    
    def is_teacher(self):
        return self.role == 'teacher'
        
    def is_student(self):
        return self.role == 'student'