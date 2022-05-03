from django.db import models


# Create your models here
class Clas(models.Model):
    name = models.CharField(max_length=32, verbose_name="班级名称")

class  Course(models.Model):

    title = models.CharField(max_length=32, verbose_name="课程名称")
    