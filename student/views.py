from django.shortcuts import render, HttpResponse
from .models import Student, StudentDetail, Course, Clas


# Create your views here.

def add_student(request):
    # 添加记录
    # 一对多与一对一的关联属性
    stu = Student.objects.create(name="张三", age=22, sex=1, birthday="1992-12-12", clas_id=5, stu_detail_id=1)
    print(stu.name)
    return HttpResponse("添加成功")
