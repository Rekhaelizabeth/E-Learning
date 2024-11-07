from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__role': 'instructor'})
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    start_date = models.DateField()  
    end_date = models.DateField()    
    enrolled_students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    def __str__(self):
        return self.title
