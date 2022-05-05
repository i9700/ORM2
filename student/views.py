from django.shortcuts import render, HttpResponse
from .models import Student, StudentDetail, Course, Clas
from django.db.models import Avg, Count, Max, Min


# Create your views here.

def add_student(request):
    # 添加记录: 一对多与一对一的关联属性

    # stu = Student.objects.create(name="李四", age=24, sex=1, birthday="1990-12-12", clas_id=5, stu_detail_id=2)
    # print(stu.name)
    # print(stu.age)
    # print(stu.clas_id)  # 5

    # 查询这个学生的班级名称
    # Clas.objects.get(pk=5)
    # 该学生的班级对象
    # print(stu.clas)  # 一个学生一个班级，班级的模型类对象

    # 查询这个学生的班级名称
    # print(stu.clas.name)  # 通过模型类对象直接查找该学生班级
    # lisi = Student.objects.get(name="李四")
    # print(lisi.clas.name)
    # print(lisi.stu_detail.tel, lisi.stu_detail.addr)

    # 添加记录: 多对多的关联记录的增删改查
    # stu = Student.objects.create(name="小明", age=28, sex=1, birthday="1995-12-12", clas_id=5, stu_detail_id=5)
    # print(stu)
    # # 添加多对多的数据，比如给stu这个学生绑定两门课程，思修和逻辑学
    # c1 = Course.objects.get(title="思修")
    # print(c1)
    # c2 = Course.objects.get(title="逻辑学")
    # print(c2)
    # res = stu.courses.add(c1, c2)
    # print(res)
    # 添加多对多方式二：
    # stu = Student.objects.get(name="张三")
    # stu.courses.add(1, 3)
    # 添加多对多方式三：
    # stu = Student.objects.get(name="李四")
    # stu.courses.add(*[1, 5])

    # 删除多对多记录;
    # stu = Student.objects.get(name="李四")
    # stu.courses.remove(1)
    # print("删除成功！")

    # 删除clear方法;
    # stu = Student.objects.get(name="yuan")
    # stu.courses.clear()
    # print("删除成功！")

    # set方法,重置;
    # stu = Student.objects.get(name="李四")
    # stu.courses.set([3, 4])
    # print("重置成功！")
    return HttpResponse("添加成功")


def select_student(request):
    '''
    正向查询：通过关联属性查询属于正向查询，反之则称为反向查询

    反向查询：

    基于对象的关联查询(子查询)

   一对多的关联查询
    '''

    # --查询张三所在班级的名称（正向查询）
    stu = Student.objects.get(name="张三")
    print(stu.clas.name)

    # --查询软件1班有哪些学生（反向查询）

    clas = Clas.objects.get(name="软件1班")
    # 反向查询方式一：
    # ret = clas.student_set.all()  # 反向查询按表名小写_set
    # print(ret) # <QuerySet [<Student: rain>, <Student: yuan>, <Student: 小明>]>

    # 反向查询方式二：
    print(clas.student_list.all())

    '''
    一对一的关联查询
    '''

    # -- 查询李四的手机号
    stu = Student.objects.get(name="李四")
    print(stu.stu_detail.tel)

    # -- 查询110手机号的学生
    stu_detail = StudentDetail.objects.get(tel="110")
    # todo:  反向查询方式1： 表名小写
    # print(stu_detail.student)

    # todo: 反向查询方式2：
    print(stu_detail.stu.name, stu_detail.stu.age)

    '''
    多对多关联查询
    '''

    # -- 查询小明所报课程的名称（正向）
    stu = Student.objects.get(name="小明")
    print(stu.courses.all())

    # -- 查询所报篮球课程学生的姓名和年龄（反向）
    course = Course.objects.get(title="篮球")

    print(course.students.all().values("name", "age"))
    return HttpResponse("关联子查询成功！")


def select2_student(request):
    '''
    基于双下划线(join查询)
    '''

    # --查询张三的年龄
    ret = Student.objects.filter(name="张三").values("age")
    print(ret)

    # (1) --查询年龄大于22的学生的姓名以及所在班级名称
    '''  sql:
    select db_student.name, db_class.name
        from db_student
                inner join db_class on db_student.clas_id = db_class.id
    where db_student.age > 25
    '''
    # 方式1：Student作为基表
    res = Student.objects.filter(age__gt=25).values("name", "clas__name")
    print(res)
    # 方式1：Clas作为基表
    res = Clas.objects.filter(student_list__age__gt=25).values("student_list__name", "name")
    print(res)

    # (3)-- 查询计算机科学与技术2班有哪些学生
    res = Clas.objects.filter(name="计算机科学与技术2班").values("student_list__name")
    print(res)

    res = Student.objects.filter(clas__name="计算机科学与技术2班").values("name")
    print(res)

    # (3) 查询张三所报课程的名称
    res = Student.objects.filter(name="张三").values("courses__title")
    print(res)

    # (4) 查询选选修了近代史这门课程学生的姓名和年龄
    res = Course.objects.filter(title="近代史").values("students__name", "students__age")
    print(res)

    # (5) 查询李四的手机号
    res = Student.objects.filter(name="李四").values("stu_detail__tel")
    print(res)

    # (6)查询手机号是110的学生的姓名和所在班级
    # 方式2：
    res = StudentDetail.objects.filter(tel="110").values("stu__name", "stu__clas__name")
    print(res)
    # 方式1：
    res = Student.objects.filter(stu_detail__tel="110").values("name", "clas__name")  # 不相关联系的表可以用都有关系的那张表作为基表
    print(res)

    '''
    分组查询
    '''
    res = Student.objects.values("sex").annotate(c=Count("name"))
    print(res)

    # (1)查询每一个班级的名称以及学生个数
    res = Clas.objects.values("name").annotate(count=Count("student_list__name"))
    print(res)
    # (2)查询每一个学生的姓名，年龄以及选修课程的个数
    res = Student.objects.values("name", "age").annotate(c=Count("courses__title"))
    print(res)
    res = Student.objects.all().annotate(c=Count("courses__title")).values("name", "age", "sex", "c")
    print(res)

    # (3)查询每一个课程名称以及选秀学生的个数
    res = Course.objects.all().annotate(c=Count("students__name")).values("title", "c")
    # res = Course.objects.values("title").annotate(c=Count("students__name"))
    print(res)
    # (4)查询选秀课程个数大于1的学生姓名以及选修课程个数
    res = Student.objects.all().annotate(c=Count("courses__title")).filter(c__gt=1).values("name", "c")
    print(res)
    # (5)查询每一个学生的姓名以及选秀课程的个数并按着选修的课程个数从低到高排序, 降序则在排序的字段名称前加-
    res = Student.objects.all().annotate(c=Count("courses__title")).order_by("-c").values("name", "c")
    print(res)
    return HttpResponse("关联join查询成功！")
