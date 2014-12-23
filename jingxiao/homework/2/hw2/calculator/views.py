from django.shortcuts import render
import re

def calculate(request):
	divide_by_zero_error = 'Divide by zero error. Calculator has been reset.'
	invalid_input_error = 'Invalid input error. Calculator has been reset.'
	malformed_input_error = 'Malformed data received. Calculator has been reset.'
	calculation_error = 'Calculation error. Calculator has been reset.'

	context = {}

	context['answer_display'] = ''
	context['answer_arg1'] = ''
	context['answer_op'] = ''
	context['answer_arg2'] = ''
	context['answer_equals'] = ''
	context['error_message'] = ''

	operators = ['/', '*', '-', '+', '=']
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	# use regex/check operator list to validate the hidden field inputs
	# then set context['error_message'] = malformed_input_error any field is invalid
	# without setting any of the hidden fields
	# and return page to be rendered

	if 'display' in request.GET:
		display = request.GET['display']
		try: 
			if len(display) > 0:
				re.match(r'^-?[0-9]+$', display).group()
			context['answer_display'] = display
		except AttributeError:
			# reset everything
			context['answer_display'] = ''
			context['answer_arg1'] = ''
			context['answer_op'] = ''
			context['answer_arg2'] = ''
			context['error_message'] = malformed_input_error
			return render(request, 'index.html', context)
		
	if 'arg1' in request.GET:
		arg1 = request.GET['arg1']
		try: 
			if len(arg1) > 0:
				re.match(r'^-?[0-9]+$', arg1).group()
			context['answer_arg1'] = arg1
		except AttributeError:
			# reset everything
			context['answer_display'] = ''
			context['answer_arg1'] = ''
			context['answer_op'] = ''
			context['answer_arg2'] = ''
			context['error_message'] = malformed_input_error
			return render(request, 'index.html', context)

	if 'op' in request.GET:
		op = request.GET['op']
		if len(op) > 0:
			if op not in operators:
				# reset everything
				context['answer_display'] = ''
				context['answer_arg1'] = ''
				context['answer_op'] = ''
				context['answer_arg2'] = ''
				context['error_message'] = malformed_input_error
				return render(request, 'index.html', context)
		context['answer_op'] = op

	if 'arg2' in request.GET:
		arg2 = request.GET['arg2']
		try: 
			if len(arg2) > 0:
				re.match(r'^-?[0-9]+$', arg2).group()
			context['answer_arg2'] = arg2
		except AttributeError:
			# reset everything
			context['answer_display'] = ''
			context['answer_arg1'] = ''
			context['answer_op'] = ''
			context['answer_arg2'] = ''
			context['error_message'] = malformed_input_error
			return render(request, 'index.html', context)

	if 'input' in request.GET:
		user_input = request.GET['input']

		if user_input in operators:
			# case: arg1, op, arg2 all exist -> evaluate
			if 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op'] \
				and 'arg2' in request.GET and request.GET['arg2']:
				arg1 = str(int(request.GET['arg1']))
				op = request.GET['op']
				arg2 = str(int(request.GET['arg2']))

				if op == '/' and arg2 == '0':
					# reset everything
					context['answer_display'] = ''
					context['answer_arg1'] = ''
					context['answer_op'] = ''
					context['answer_arg2'] = ''
					context['error_message'] = divide_by_zero_error
					return render(request, 'index.html', context)
				elif op == '=':
					# reset everything
					context['answer_display'] = ''
					context['answer_arg1'] = ''
					context['answer_op'] = ''
					context['answer_arg2'] = ''
					context['error_message'] = invalid_input_error
					return render(request, 'index.html', context)
				else:
					try: 
						context['answer_display'] = eval(arg1 + op + arg2)
					except:
						# reset everything
						context['answer_display'] = ''
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
						context['error_message'] = calculation_error
						return render(request, 'index.html', context)
					context['answer_arg1'] = context['answer_display'] #set answer to be new arg1
					context['answer_arg2'] = '' #reset arg2

					if user_input != '=':
						context['answer_op'] = user_input #set new op
					else:
						context['answer_op'] = ''
						context['answer_equals'] = 'equals' #indicate op is =

			# case: arg1, op exist -> replace op
			elif 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op']:
				arg1 = str(int(request.GET['arg1']))
				op = request.GET['op']

				if user_input != '=':
					context['answer_display'] = context['answer_display'] # don't change display
					context['answer_op'] = user_input #set new op
				else:
					if op == '/' and arg1 == '0':
						# reset everything
						context['answer_display'] = ''
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
						context['error_message'] = divide_by_zero_error
						return render(request, 'index.html', context)
					elif op == '=':
						# reset everything
						context['answer_display'] = ''
						context['answer_arg1'] = ''
						context['answer_op'] = ''
						context['answer_arg2'] = ''
						context['error_message'] = invalid_input_error
						return render(request, 'index.html', context)
					else:
						context['answer_display'] = context['answer_display']
						context['answer_op'] = op #keep old op

			# case: arg1 exists -> save op
			elif 'arg1' in request.GET and request.GET['arg1']:
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
			if 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op'] \
				and 'arg2' in request.GET and request.GET['arg2']:
				arg2 = str(int(request.GET['arg2']))

				if arg2 == '0':
					context['answer_display'] = user_input
					context['answer_arg2'] = user_input
				else:
					context['answer_display'] += user_input
					context['answer_arg2'] += user_input

			# case: arg1, op exist -> starting arg2
			elif 'arg1' in request.GET and request.GET['arg1'] \
				and 'op' in request.GET and request.GET['op']:
				context['answer_display'] = user_input
				context['answer_arg2'] = user_input

			# case: arg1 exists -> continuing arg1
			elif 'arg1' in request.GET and request.GET['arg1']:
				if 'equals' in request.GET:
					context['answer_display'] = user_input
					context['answer_arg1'] = user_input
				else:
					arg1 = str(int(request.GET['arg1']))

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
			# reset everything
			context['answer_display'] = ''
			context['answer_arg1'] = ''
			context['answer_op'] = ''
			context['answer_arg2'] = ''
			context['error_message'] = invalid_input_error
			return render(request, 'index.html', context)


	return render(request, 'index.html', context)