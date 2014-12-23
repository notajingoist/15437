from django.shortcuts import render
from django.db import transaction

from models import *
from forms import *

from django.http import HttpResponse
from django.core import serializers

def make_view(request, 
              messages=[], 
              create_student_form=CreateStudentForm(), 
              create_course_form=CreateCourseForm(), 
              register_student_form=RegisterStudentForm()):
    context = {
               'courses':Course.objects.all(), 
               'messages':messages,
               'create_student_form':create_student_form,
               'create_course_form':create_course_form,
               'register_student_form':register_student_form,
              }
    return render(request, 'sio.html', context)

def home(request):
    return make_view(request, [])

@transaction.atomic
def create_student(request):
    form = CreateStudentForm(request.POST)
    if not form.is_valid():
        return make_view(request, create_student_form=form)

    new_student = Student(andrew_id=form.cleaned_data['andrew_id'],
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
    new_student.save()
    return make_view(request, ['Added %s'%new_student])

@transaction.atomic
def create_course(request):
    form = CreateCourseForm(request.POST)
    if not form.is_valid():
        return make_view(request, create_course_form=form)

    new_course = Course(course_number=request.POST['course_number'],
                        course_name=request.POST['course_name'],
                        instructor=request.POST['instructor'])
    new_course.save()
    return make_view(request, messages=['Added %s'%new_course])

@transaction.atomic
def register_student(request):
    form = RegisterStudentForm(request.POST)
    if not form.is_valid():
        return make_view(request, register_student_form=form)

    course = Course.objects.get(course_number=request.POST['course_number'])
    student = Student.objects.get(andrew_id=request.POST['andrew_id'])
    course.students.add(student)
    course.save()
    return make_view(request, messages=['Added %s to %s' % (student, course)])


# Complete this action to generate a JSON response containing all courses
def get_all_courses(request):
    # manual way:
    # context = {}
    # courses = Course.objects.all()
    # context['courses'] = courses
    # return render(request, 'courses.json', context, content_type='application/json')

    # with django serialization:
    data = serializers.serialize('json', Course.objects.all()) #, fields=('course_number', 'course_name', 'instructor'))
    return HttpResponse(data, content_type='application/json')
    

# ,
#         "students": [ {{course.students}}
#           {% for student in course.students %}
#             {
#               "andrew_id": {{student.andrew_id}},
#               "first_name": {{student.first_name}},
#               "last_name": {{student.last_name}}
#             } {% if not forloop.last %},{% endif %}
#           {% endfor %}
#         ]




