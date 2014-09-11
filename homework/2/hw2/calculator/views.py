from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'index.html', {})

def calculate(request):
	divide_by_zero_error = 'divide by zero error'

	context = {}

	context['answer_display'] = ''
	context['answer_arg1'] = ''
	context['answer_op'] = ''
	context['answer_arg2'] = ''
	context['answer_equals'] = ''
	

	operators = ['/', '*', '-', '+', '=']

	if 'display' in request.GET:
		context['answer_display'] = request.GET['display']

	if 'arg1' in request.GET:
		context['answer_arg1'] = request.GET['arg1']

	if 'op' in request.GET:
		context['answer_op'] = request.GET['op']

	if 'arg2' in request.GET:
		context['answer_arg2'] = request.GET['arg2']

	if 'input' in request.GET:
		user_input = request.GET['input']

		if user_input in operators:
			# case: arg1, op, arg2 all exist -> evaluate
			if 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op'] \
				and 'arg2' in request.GET and request.GET['arg2']:

				if request.GET['op'] == '/' and request.GET['arg2'] == '0':
					context['answer_display'] = divide_by_zero_error #divide by zero
					
					# reset everything
					context['answer_arg1'] = ''
					context['answer_op'] = ''
					context['answer_arg2'] = ''
				else:
					context['answer_display'] = eval(request.GET['arg1'] \
									+ request.GET['op'] \
									+ request.GET['arg2'])

					context['answer_arg1'] = context['answer_display'] #set answer to be new arg1
					context['answer_arg2'] = '' #reset arg2

					if user_input != '=':
						context['answer_op'] = user_input #set new op
					else:
						context['answer_op'] = ''
						# context['answer_equals'] = 'equals'

			# case: arg1, op exist -> replace op
			elif 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op']:
				if user_input != '=':
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = user_input #set new op
				else:
					if request.GET['op'] == '/' and request.GET['arg1'] == '0':
						context['answer_display'] = divide_by_zero_error #divide by zero

						# reset everything
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
					else:
						context['answer_display'] = eval(request.GET['arg1'] \
									+ request.GET['op'] \
									+ request.GET['arg1'])

						context['answer_op'] = request.GET['op'] #keep old op

			# case: arg1 exists -> save op
			elif 'arg1' in request.GET and request.GET['arg1']:
				if user_input != '=':
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = user_input #set op
				else:
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = ''
					# context['answer_equals'] = 'equals'

			# case: no arg exists -> use 0 as arg1
			else:
				if user_input != '=':
					context['answer_arg1'] = '0'
					context['answer_op'] = user_input

		else: #not an operator
			# case: arg1, op, arg2 all exist -> continuing arg2
			if 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op'] \
				and 'arg2' in request.GET and request.GET['arg2']:
				context['answer_display'] += user_input
				context['answer_arg2'] += user_input

			# case: arg1, op exist -> starting arg2
			elif 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op']:
				context['answer_display'] = user_input
				context['answer_arg2'] = user_input

			# case: arg1 exists, op was equals -> starting arg2
			elif 'arg1' in request.GET and request.GET['arg1'] \
				and 'equals' in request.GET and request.GET['equals']:
				context['answer_display'] = user_input
				context['answer_arg2'] = user_input
				# context['answer_equals'] = ''

			# case: arg1 exists -> continuing arg1
			elif 'arg1' in request.GET and request.GET['arg1']:
				context['answer_display'] += user_input
				context['answer_arg1'] += user_input

			# case: no arg exists -> starting arg1
			else:
				context['answer_display'] = user_input
				context['answer_arg1'] = user_input


	return render(request, 'index.html', context)

	# if 'answer_state' in request.GET:
	# 	request.GET