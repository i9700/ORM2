from django.db import models


# Create your models here
class Clas(models.Model):
    name = models.CharField(max_length=32, verbose_name="班级名称")

    class Meta:
        db_table = "db_class"


class Course(models.Model):
    title = models.CharField(max_length=32, verbose_name="课程名称")

    # students = models.ManyToManyField("Student", db_table="db_student2course")
    class Meta:
        db_table = "db_course"


class Student(models.Model):
    SEX_CHOICES = (
        (0, "女"),
        (1, "男"),
        (2, "保密"),
    )
    name = models.CharField(max_length=32, unique=True, verbose_name="姓名")
    age = models.SmallIntegerField(default=18, verbose_name="年龄")
    sex = models.SmallIntegerField(choices=SEX_CHOICES)
    birthday = models.DateField()

    # 一对多的关系: 在数据库创建一个关联字段：clas_id(在clas字段后缀新增_id)
    clas = models.ForeignKey(to="Clas", on_delete=models.CASCADE, db_constraint=False)

    # 多对多的关系: 创建第三张关系表
    courses = models.ManyToManyField("Course", db_table="db_student2course")

    # 一对一的关系: 建立关联字段,在数据库中生成关联字段: stu_detail_id
    stu_detail = models.OneToOneField("StudentDetail", on_delete=models.CASCADE)

    class Meta:
        db_table = "db_student"


class StudentDetail(models.Model):
    tel = models.CharField(max_length=11)
    addr = models.CharField(max_length=32)

    class Meta:
        db_table = "db_stu_detail"
