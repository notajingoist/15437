from django import forms
from models import *

class CreateStudentForm(forms.Form):
	andrew_id = forms.CharField(max_length=20)
	first_name = forms.CharField(max_length=40)
	last_name = forms.CharField(max_length=40)

	def clean(self):
		cleaned_data = super(CreateStudentForm, self).clean()

		andrew_id = cleaned_data.get('andrew_id')
		first_name = cleaned_data.get('first_name')
		
		return cleaned_data

	def clean_andrew_id(self):
		andrew_id = self.cleaned_data.get('andrew_id')
		if Student.objects.filter(andrew_id__exact=andrew_id):
			raise forms.ValidationError("A student with Andrew ID %s already exists." % 
                      andrew_id)
		return andrew_id

class CreateCourseForm(forms.Form):
	course_name = forms.CharField(max_length=255)
	course_number = forms.CharField(max_length=40)
	instructor = forms.CharField(max_length=255)

	def clean(self):
		cleaned_data = super(CreateCourseForm, self).clean()

		course_name = cleaned_data.get('course_name')
		course_number = cleaned_data.get('course_number')
		instructor = cleaned_data.get('instructor')

		return cleaned_data

	def clean_course_number(self):
		course_number = self.cleaned_data.get('course_number')
		if Course.objects.filter(course_number__exact=course_number):
			raise forms.ValidationError("Course %s already exists." % 
                      course_number)
		return course_number






