
from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):

    ROLE_CHOICES = (
    ('manager', 'مدیر'),
    ('teacher', 'استاد'),
    ('student', 'دانشجو'),
)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    min_units = models.PositiveIntegerField(default=0)
    max_units = models.PositiveIntegerField(default=20)
    
    
    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    def is_manager(self):
        return self.role == 'manager'
    
    def is_teacher(self):
        return self.role == 'teacher'
        
    def is_student(self):
        return self.role == 'student'