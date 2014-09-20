from django.db import models

# Create your models here.
class Student(models.Model):
    andrew_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.andrew_id

class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)

    def __unicode__(self):
        return self.course_name
