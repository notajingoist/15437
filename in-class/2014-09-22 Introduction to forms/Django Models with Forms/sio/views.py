from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import transaction

from models import *
from forms import *

def make_view(request, messages):
    context = {'courses':Course.objects.all(), 'messages':messages}
    return render(request, 'sio.html', context)

def home(request):
    context = {}
    context['courses'] = Course.objects.all()

    context['create_student_form'] = CreateStudentForm()
    context['create_course_form'] = CreateCourseForm()

    return render(request, 'sio.html', context)

@transaction.atomic
def create_student(request):
    context = {}
    context['courses'] = Course.objects.all()

    if request.method == 'GET':
        return redirect(reverse('home1'))

    create_student_form = CreateStudentForm(request.POST)
    context['create_student_form]'] = create_student_form

    if not create_student_form.is_valid():
        return redirect(reverse('home1'))

    new_student = Student(andrew_id=request.POST['andrew_id'],
                          first_name=request.POST['first_name'],
                          last_name=request.POST['last_name'])
    new_student.save()
    
    return redirect(reverse('home1'))

@transaction.atomic
def create_course(request):
    context = {}
    context['courses'] = Course.objects.all()

    if request.method == 'GET':
        return redirect(reverse('home1'))

    create_course_form = CreateCourseForm(request.POST)
    context['create_course_form]'] = create_course_form

    if not create_student_form.is_valid():
       return redirect(reverse('home1'))

    new_course = Course(course_number=request.POST['course_number'],
                        course_name=request.POST['course_name'],
                        instructor=request.POST['instructor'])
    new_course.save()
    
    return redirect(reverse('home1'))


@transaction.atomic
def register_student(request):
    messages = []
    if not 'andrew_id' in request.POST or not request.POST['andrew_id']:
        messages.append("Andrew ID is required.")
    elif Student.objects.filter(andrew_id=request.POST['andrew_id']).count() != 1:
        messages.append("Could not find Andrew ID %s." %
                        request.POST['andrew_id'])
    if not 'course_number' in request.POST or not request.POST['course_number']:
        messages.append("Course number is required.")
    elif Course.objects.filter(course_number=request.POST['course_number']).count() != 1:
        messages.append("Could not find course %s." %
                        request.POST['course_number'])

    if messages:
        return make_view(request, messages)

    course = Course.objects.get(course_number=request.POST['course_number'])
    student = Student.objects.get(andrew_id=request.POST['andrew_id'])
    course.students.add(student)
    course.save()

    messages.append('Added %s to %s' % (student, course))
    return make_view(request, messages)
