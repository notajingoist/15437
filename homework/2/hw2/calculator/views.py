from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'index.html', {})

def calculate(request):
	divide_by_zero_error = 'divide by zero error'
	invalid_input_error = 'invalid input error'

	context = {}

	context['answer_display'] = ''
	context['answer_arg1'] = ''
	context['answer_op'] = ''
	context['answer_arg2'] = ''
	context['answer_equals'] = ''

	operators = ['/', '*', '-', '+', '=']
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	if 'display' in request.POST:
		context['answer_display'] = request.POST['display']

	if 'arg1' in request.POST:
		context['answer_arg1'] = request.POST['arg1']

	if 'op' in request.POST:
		context['answer_op'] = request.POST['op']

	if 'arg2' in request.POST:
		context['answer_arg2'] = request.POST['arg2']

	if 'input' in request.POST:
		user_input = request.POST['input']

		if user_input in operators:
			# case: arg1, op, arg2 all exist -> evaluate
			if 'arg1' in request.POST and request.POST['arg1'] \
				and 'op' in request.POST and request.POST['op'] \
				and 'arg2' in request.POST and request.POST['arg2']:
				arg1 = str(int(request.POST['arg1']))
				op = request.POST['op']
				arg2 = str(int(request.POST['arg2']))

				if op == '/' and arg2 == '0':
					context['answer_display'] = divide_by_zero_error #divide by zero
					
					# reset everything
					context['answer_arg1'] = ''
					context['answer_op'] = ''
					context['answer_arg2'] = ''
				elif op == '=':
					context['answer_display'] = invalid_input_error #divide by zero
					
					# reset everything
					context['answer_arg1'] = ''
					context['answer_op'] = ''
					context['answer_arg2'] = ''
				else:
					context['answer_display'] = eval(arg1 + op + arg2)
					context['answer_arg1'] = context['answer_display'] #set answer to be new arg1
					context['answer_arg2'] = '' #reset arg2

					if user_input != '=':
						context['answer_op'] = user_input #set new op
					else:
						context['answer_op'] = ''
						context['answer_equals'] = 'equals' #indicate op is =

			# case: arg1, op exist -> replace op
			elif 'arg1' in request.POST and request.POST['arg1'] \
				and 'op' in request.POST and request.POST['op']:
				arg1 = str(int(request.POST['arg1']))
				op = request.POST['op']

				if user_input != '=':
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = user_input #set new op
				else:
					if op == '/' and arg1 == '0':
						context['answer_display'] = divide_by_zero_error #divide by zero

						# reset everything
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
					elif op == '=':
						context['answer_display'] = invalid_input_error #divide by zero
						
						# reset everything
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
					else:
						context['answer_display'] = eval(arg1 + op + arg1)
						context['answer_op'] = op #keep old op

			# case: arg1 exists -> save op
			elif 'arg1' in request.POST and request.POST['arg1']:
				if user_input != '=':
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = user_input #set op
				else:
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = ''
					context['answer_equals'] = 'equals' #indicate op is =

			# case: no arg exists -> use 0 as arg1
			else:
				if user_input != '=':
					context['answer_arg1'] = '0'
					context['answer_op'] = user_input

		elif user_input in digits: #not an operator
			# case: arg1, op, arg2 all exist -> continuing arg2
			if 'arg1' in request.POST and request.POST['arg1'] \
				and 'op' in request.POST and request.POST['op'] \
				and 'arg2' in request.POST and request.POST['arg2']:
				arg2 = str(int(request.POST['arg2']))

				if arg2 == '0':
					context['answer_display'] = user_input
					context['answer_arg2'] = user_input
				else:
					context['answer_display'] += user_input
					context['answer_arg2'] += user_input

			# case: arg1, op exist -> starting arg2
			elif 'arg1' in request.POST and request.POST['arg1'] \
				and 'op' in request.POST and request.POST['op']:
				context['answer_display'] = user_input
				context['answer_arg2'] = user_input

			# case: arg1 exists -> continuing arg1
			elif 'arg1' in request.POST and request.POST['arg1']:
				if 'equals' in request.POST:
					context['answer_display'] = user_input
					context['answer_arg1'] = user_input
				else:
					arg1 = str(int(request.POST['arg1']))

					if arg1 == '0':
						context['answer_display'] = user_input
						context['answer_arg1'] = user_input
					else:
						context['answer_display'] += user_input
						context['answer_arg1'] += user_input

			# case: no arg exists -> starting arg1
			else:
				context['answer_display'] = user_input
				context['answer_arg1'] = user_input

		else:
			context['answer_display'] = invalid_input_error
			
			# reset everything
			context['answer_arg1'] = ''
			context['answer_op'] = ''
			context['answer_arg2'] = ''


	return render(request, 'index.html', context)