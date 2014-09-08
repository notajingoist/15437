from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    
    context['student_name'] = ''
    if 'student_name' in request.GET:
        context['student_name'] = request.GET['student_name']
    
    context['course_name'] = ''
    if 'course_name' in request.GET:
        context['course_name'] = request.GET['course_name']

    context['registered_student_name'] = ''
    context['registered_course_name'] = ''
    if 'registered_student_name' in request.GET \
        and 'registered_course_name' in request.GET:
        context['registered_student_name'] = request.GET['registered_student_name']
        context['registered_course_name'] = request.GET['registered_course_name']

    return render(request, 'index.html', context)
