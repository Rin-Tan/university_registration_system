from django.db import models

class Course(models.Model):
    course_code = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=150)
    #professor = models.ForeignKey(Professor,on_delete=models.SET_NULL, null= True)
    capacity = models.PositiveIntegerField(default=30)
    units = models.PositiveIntegerField(default=3)
    day_of_week = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    prerequisites = models.ManyToManyField("self", blank=True, symmetrical=False)
    

    def __str__(self):
        return f'{self.course_code} - {self.title}'