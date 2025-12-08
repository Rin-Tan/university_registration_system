from django.db import models

class Course(models.Model):

    DAYS_OF_WEEK = [
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
    ]

    day_of_week = models.CharField(
        max_length=3,
        choices=DAYS_OF_WEEK
    )

    course_code = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(default=30)
    units = models.PositiveIntegerField(default=3)
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    prerequisites = models.ManyToManyField("self", blank=True, symmetrical=False)
    #professor = models.ForeignKey(Professor,on_delete=models.SET_NULL, null= True)
    

    def __str__(self):
        return f'{self.course_code} - {self.title}'