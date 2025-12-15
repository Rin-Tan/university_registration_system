from django.db import models

class TimeSlot(models.Model):

    DAYS_OF_WEEK = (
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    )
    
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, verbose_name="Day of Week")
    start_time = models.TimeField(verbose_name="start")
    end_time = models.TimeField(verbose_name="finish")

    def __str__(self):
        return f"{self.get_day_display()} - {self.start_time} to {self.end_time}"



class Course(models.Model):

    course_code = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(default=30)
    units = models.PositiveIntegerField(default=3)
    location = models.CharField(max_length=100)
    time_slots = models.ManyToManyField(TimeSlot)
    prerequisites = models.ManyToManyField("self", blank=True, symmetrical=False)
    #professor = models.ForeignKey(Professor,on_delete=models.SET_NULL, null= True)
    

    def __str__(self):
        return f'{self.title} - {self.course_code}'