from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'index.html', {})

def calculate(request):
	context = {}

	

	context['answer_state'] = ''
	context['answer_display'] = ''
	context['answer_mode'] = '' 

	context['answer_arg1'] = ''
	context['answer_arg2'] = ''
	context['answer_op'] = ''





	return render(request, 'index.html', context)

	# if 'answer_state' in request.GET:
	# 	request.GET