from django import forms
from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet
from learnApp.models import *

# Create your forms here

class RegistrationForm(forms.Form):
	firstname = forms.CharField(max_length=200,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	lastname = forms.CharField(max_length=200,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	username = forms.CharField(max_length=20,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
	email = forms.CharField(max_length=100,
							widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password1 = forms.CharField(max_length=20,
								widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	password2 = forms.CharField(max_length=20,
								widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match.")

		return cleaned_data

	def clean_username(self):

		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		return username

	def clean_email(self):

		email = self.cleaned_data.get('email')
		if User.objects.filter(email__exact=email):
			raise forms.ValidationError("Email has already been used for an account.")
		return email

class LoginForm(forms.Form):

	username = forms.CharField(max_length=20,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
	password = forms.CharField(max_length=20,
								widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		return cleaned_data

	def clean_username(self):

		username = self.cleaned_data.get('username')
		if not User.objects.filter(username__exact=username).exists():
			raise forms.ValidationError("No such username exists.")
		return username

class SearchForm(forms.Form):

	keyword = forms.CharField(max_length=40,
							label='',
							widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search Catalog'}))

	def clean(self):
		cleaned_data = super(SearchForm, self).clean()
		return cleaned_data

class SearchCategoryForm(forms.Form):
	
	keyword = forms.CharField(max_length=40, required=False,
							label='',
							widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search'}))

	def clean(self):
		cleaned_data = super(SearchCategoryForm, self).clean()
		return cleaned_data		


class TakeQuizForm(forms.Form):
	def __init__(self, data=None, quiz=None, *args, **kwargs):
		super(TakeQuizForm, self).__init__(data, *args, **kwargs)
		if quiz:
			questions = quiz.mcquestion_set.all()
			for question in questions:
				choices = []
				for choice in question.choice_set.all():
					choices.append((choice.pk, choice.choice))

				field = forms.ChoiceField(label=question.question, required=True,
											choices=choices, widget=forms.RadioSelect)
				field_name = "question_{}".format(question.pk)

				self.fields[field_name] = field

	def clean(self):
		cleaned_data = super(TakeQuizForm, self).clean()
		print(cleaned_data)

		num_correct = 0
		num_questions = 0

		for q_str in cleaned_data.keys():
			split = q_str.split('_')
			if "question" == split[0]:
				q_pk = int(split[1])
				c_pk = int(cleaned_data[q_str])
				question = MCQuestion.objects.get(pk=q_pk)
				choice = Choice.objects.get(pk=c_pk)

				num_questions+=1
				if choice.isAnswer:
					num_correct+=1
				# else:
				# 	self._errors[q_str] = self.error_class(["Incorrect"])

		cleaned_data['score'] = float(num_correct)/num_questions
		return cleaned_data


class CourseCreationForm(forms.Form):
	course_name = forms.CharField(max_length=200,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Course Name'}))
	overview = forms.CharField(max_length=1000,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Course Overview'}))
	course_image = forms.ImageField()
	#category = forms.ChoiceField(choices = ["Machine Learning", "Cloud Computing","Computer Systems"])



	def clean(self):
		cleaned_data = super(CourseCreationForm, self).clean()

	def clean_course_name(self):
		course_name = self.cleaned_data.get('course_name')
		if Course.objects.filter(course_name__exact=course_name):
			raise forms.ValidationError("Course Name is not Unique. Please provide another Course Name.")
		return course_name

	def clean_course_image(self):
		image_file = self.cleaned_data.get('course_image')
		if not image_file.name.endswith(".jpg"):
			raise forms.ValidationError("Only jpg files accepted.")
		return image_file

class CourseEditForm(forms.Form):

	overview = forms.CharField(max_length=1000,
								widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Course Overview'}))
	course_image = forms.ImageField()


	def clean(self):
		cleaned_data = super(CourseEditForm, self).clean()

	def clean_course_image(self):
		image_file = self.cleaned_data.get('course_image')
		if not image_file.name.endswith(".jpg"):
			raise forms.ValidationError("Only jpg files accepted.")
		return image_file
