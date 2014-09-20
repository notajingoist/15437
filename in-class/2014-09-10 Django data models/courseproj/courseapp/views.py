from django.shortcuts import render

# Create your views here.

def home(request):
    all_courses = Course.objects.all()
    all_students = Student.objects.all()

    context = {}
    context['courses'] = all_courses;
    contexte['students'] = all_students;

    return render(request, 'index.html', context)


def create_student(request):
    errors = []
    if not 'andrew_id' in request.GET or not request.GET['item']:
        errors.append('You must enter an andrew ID to create a student.')
    if not 'first_name' in request.GET or not request.GET['first_name'


    context = {}
    
    context['andrew_id'] = ''
    context['first_name'] = ''
    context['last_name'] = ''
    if 'andrew_id' in request.GET \
        and 'first_name' in request.GET \ 
        and 'last_name' in request.GET:
        context['andrew_id'] = request.GET['andrew_id']
        context['first_name'] = request.GET['first_name']
        context['last_name'] = request.GET['last_name']

    return render(request, 'index.html', context)


def create_course(request):
    context = {}
    
    context['course_number'] = ''
    context['course_name'] = ''
    if 'course_number' in request.GET \
        and 'course_name' in request.GET:
        context['course_number'] = request.GET['course_number']
        context['course_name'] = request.GET['course_name']

    return render(request, 'index.html', context)


def register_for_course(request):
    context = {}
   
    context['andrew_id'] = ''
    context['course_name'] = ''
    if 'andrew_id' in request.GET \
        and 'course_name' in request.GET:
        context['andrew_id'] = request.GET['andrew_id']
        context['course_name'] = request.GET['course_name']

    return render(request, 'index.html', context)
