from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    
class Subject(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_name=models.CharField(max_length=100)
