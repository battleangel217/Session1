from django.db import models
from django.db.models import Count, Avg, Max

class Products(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField()
    


class School(models.Model):
    name = models.CharField(max_length=100)
    # branch = models.CharField(max_length=100, default="Permsite", null=True)

class Students(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, related_name="students" , on_delete=models.CASCADE)


class CustomUser(models.Model):
    email =models.EmailField(max_length=100)
    username = models.CharField(max_length=100)

    class Meta:
        unique_together = ['email', 'username']

    def details(self):
        return f"{self.email}: {self.username}"
    def __str__(self):
        return f"{self.email}: {self.username}"
    

class Profile(models.Model):
    dob = models.DateField()
    marital_status = models.CharField(default="Single")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')


class UserAuthentication(models.Model):
    user_name = models.CharField(max_length=100, unique=True)


class Courses(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(Students, related_name="offering")


class Teacher(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)

class StudentsEnrolled(models.Model):
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(Course, related_name="students")
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    