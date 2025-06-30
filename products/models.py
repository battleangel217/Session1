from django.db import models

class Products(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    


class School(models.Model):
    name = models.CharField(max_length=100)
    # branch = models.CharField(max_length=100, default="Permsite", null=True)

class Students(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, related_name="students" , on_delete=models.CASCADE)


class CustomUser(models.Model):
    email =models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    

class Profile(models.Model):
    dob = models.DateField()
    marital_status = models.CharField(default="Single")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')


class UserAuthentication(models.Model):
    user_name = models.CharField(max_length=100)


class Courses(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(Students, related_name="offering")


class Teacher(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class StudentsEnrolled(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=17)
    student = models.ManyToManyField(Course)