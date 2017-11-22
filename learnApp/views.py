# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseServerError

from learnApp.models import *
from learnApp.forms import *
import random, json
import re
# Create your views here.

@login_required
def home(request):
	context = {}
	allc = Course.objects.all()
	if Course.objects.count()<3:
		context['courses'] = allc
	else:
		c = []
		rand = random.sample(range(0, Course.objects.count()), 3)
		c.append(allc[rand[0]])
		c.append(allc[rand[1]])
		c.append(allc[rand[2]])
		context['courses'] = c
	context['search'] = SearchForm()
	return render(request, 'learnApp/home.html', context)

@login_required
def myRegisteredCourses(request):
	context = {}
	context['courses'] = request.user.reg_courses.all()
	context['search'] = SearchForm()
	context['reg'] = 1
	return render(request, 'learnApp/courseView.html', context)

@login_required
def myOwnedCourses(request):
	context = {}
	context['courses'] = request.user.owned_courses.all()
	context['search'] = SearchForm()
	return render(request, 'learnApp/courseView.html', context)

def searchPage(request):
	context = {}
	context['search'] = SearchForm()
	context['searchCat'] = SearchCategoryForm()
	context['register'] = RegistrationForm()
	context['login'] = LoginForm()
	if request.user.is_authenticated():
		context['islogin'] = 1
		context['extend'] = "learnApp/loggedinBase.html"
	else:
		context['register'] = RegistrationForm()
		context['login'] = LoginForm()
		context['extend'] = "learnApp/loggedoutBase.html"
	return render(request, 'learnApp/searchView.html', context)

def search(request):
	context = {}
	context['search'] = SearchForm()
	context['register'] = RegistrationForm()
	context['login'] = LoginForm()
	if request.user.is_authenticated():
		context['islogin'] = 1
		context['extend'] = "learnApp/loggedinBase.html"
	else:
		context['register'] = RegistrationForm()
		context['login'] = LoginForm()
		context['extend'] = "learnApp/loggedoutBase.html"

	sform = SearchForm(request.POST)
	context['sform'] = sform
	if not sform.is_valid():
		return render(request, 'learnApp/searchResult.html', context)
	else:
		c = Course.objects.filter(course_name__contains=sform.cleaned_data['keyword'])
		context['courses'] = c
	return render(request, 'learnApp/searchResult.html', context)

def searchCategory(request):
	context = {}
	context['search'] = SearchForm()
	context['register'] = RegistrationForm()
	context['login'] = LoginForm()
	if request.user.is_authenticated():
		context['islogin'] = 1
		context['extend'] = "learnApp/loggedinBase.html"
	else:
		context['register'] = RegistrationForm()
		context['login'] = LoginForm()
		context['extend'] = "learnApp/loggedoutBase.html"

	sform = SearchCategoryForm(request.POST)
	context['sform'] = sform
	print("hi")
	if not sform.is_valid():
		category = request.POST['category']
		c = Course.objects.filter(category=category)
		print(category)
	else:
		category = request.POST['category']
		print(sform.cleaned_data['keyword'])
		c = Course.objects.filter(course_name__contains=sform.cleaned_data['keyword'], category=category)

	context['courses'] = c
	return render(request, 'learnApp/searchResult.html', context)


def loginApp(request):
	context = {}
	allc = Course.objects.all()
	if Course.objects.count()<3:
		context['courses'] = allc
	else:
		c = []
		rand = random.sample(range(0, Course.objects.count()), 3)
		c.append(allc[rand[0]])
		c.append(allc[rand[1]])
		c.append(allc[rand[2]])
		context['courses'] = c
	if request.method == 'GET':
		context['login'] = LoginForm()
		context['register'] = RegistrationForm()
		context['search'] = SearchForm()
		return render(request, 'learnApp/index.html', context)
	form = LoginForm(request.POST)
	context['login'] = form
	context['register'] = RegistrationForm()
	context['search'] = SearchForm()
	if not form.is_valid():
		return render(request, 'learnApp/index.html', context)
	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	usr = User.objects.get(username__exact=username)
	u = authenticate(username=username,
					password=password)
	if not u == None:
		login(request, u)
		return render(request, 'learnApp/home.html', context)
	else:
		return render(request, 'learnApp/index.html', context)

@login_required
def courseCreate(request):
	context = {}
	context['search'] = SearchForm()
	context['form'] = CourseCreationForm()
	return render(request, 'learnApp/CreateCourse.html', context)

@login_required
def saveCourse(request):
	context = {}
	form = CourseCreationForm(request.POST, request.FILES)
	context['form'] = form
	if not form.is_valid():
		context['search'] = SearchForm()
		return render(request, 'learnApp/CreateCourse.html', context)
	course_name = form.cleaned_data['course_name']
	overview = form.cleaned_data['overview']
	course_image = form.cleaned_data['course_image']


	print(request.POST)
	category = request.POST['category']

	course = Course(course_name=course_name, description=overview, owner=request.user, image=course_image, category=category)

	context['search'] = SearchForm()
	course.save()

	context['courses'] = request.user.owned_courses.all()
	return render(request, 'learnApp/courseView.html', context)

@login_required
def edit(request, name):
	context = {}
	course = Course.objects.get(course_name=name)
	form = CourseEditForm(request.POST, request.FILES)
	context['form'] = form
	context['course'] = course
	if not form.is_valid():
		context['search'] = SearchForm()
		form = CourseEditForm(initial={'overview': course.description, 'course_image' : course.image})
		context['form'] = form
		return render(request, 'learnApp/editCourse.html', context)

	overview = form.cleaned_data['overview']
	course_image = form.cleaned_data['course_image']
	les = Course.lesson_set.all()
	context['search'] = SearchForm()


	course.description = overview
	course.image = course_image
	lesson_saved = Lesson(info = lesson_text,course=course)
	lesson_saved.save()
	course.save()

	context['courses'] = request.user.owned_courses.all()
	return render(request, 'learnApp/courseView.html', context)

@login_required
def editCourse(request, name):
	context = {}
	course = Course.objects.get(course_name=name)
	form = CourseEditForm(initial={'overview': course.description, 'course_image' : course.image})
	context['form'] = form
	context['search'] = SearchForm()
	context['course'] = course
	context['quizzes'] = course.quiz_set.all()
	context['lessons'] = course.lesson_set.all()
	return render(request, 'learnApp/editCourse.html', context)

@login_required
def addLesson(request, name, lesson_id=None):
	context = {}
	#form = CourseCreationForm(request.POST)
	context['lesson_text'] = request.POST['lesson_text']
	course = Course.objects.get(course_name=name)

	lesson_text = context['lesson_text']
	lesson_text = re.sub('<[^>]*>', '', lesson_text)
	lesson_saved = Lesson(info=lesson_text, course=course)

	print(name)
	print(context['lesson_text'])
	print(lesson_text)
	form = CourseEditForm(initial={'overview': course.description, 'course_image' : course.image})

	les = course.lesson_set.all()
	print(les)

	lesson_saved = Lesson(info = lesson_text,course=course)
	lesson_saved.save()
	course.save()
	context['course'] = course
	context['lessons'] = course.lesson_set.all()

	for i in course.lesson_set.all():
		print(i.info)
	return render(request, 'learnApp/editCourse.html', context)

@login_required
def editLesson(request, name, lesson_id=None):
	context = {}
	#form = CourseCreationForm(request.POST)
	context['lesson_text'] = request.POST['lesson_text']
	course = Course.objects.get(course_name=name)

	print(name)
	print(context['lesson_text'])
	print(lesson_text)
	form = CourseEditForm(initial={'overview': course.description, 'course_image' : course.image})



	les = course.lesson_set.all()
	print(les)

	lesson_saved = Lesson(info = lesson_text,course=course)
	lesson_saved.save()
	course.save()
	context['course'] = course
	context['lessons'] = course.lesson_set.all()

	for i in course.lesson_set.all():
		print(i.info)
	return render(request, 'learnApp/editCourse.html', context)


@login_required
def registerCourse(request, name):
	context = {}
	course = Course.objects.get(course_name=name)
	context['search'] = SearchForm()
	course.students.add(request.user)
	course.save()
	context['courses'] = request.user.reg_courses.all()
	context['reg'] = 1

	return render(request, 'learnApp/courseView.html', context)

@login_required
def viewCourse(request, name):
	context = {}
	course = Course.objects.get(course_name=name)
	context['search'] = SearchForm()
	context['course'] = course
	context['quizzes'] = course.quiz_set.all()
	context['lessons'] = course.lesson_set.all()
	return render(request, 'learnApp/lessonView.html', context)

@login_required
def deleteLesson(request, course_name, lesson_id=None):
	context={}
	print(course_name)
	print(lesson_id)
	course = Course.objects.get(course_name=course_name)

	les = course.lesson_Set.all()
	for i in course.lesson_set.all():
		if i.id==lesson_id:
			i.delete()
			course.save()

	context['course'] = course
	context['quizzes'] = course.quiz_set.all()
	context['lessons'] = course.lesson_set.all()
	return render(request, 'learnApp/editCourse.html', context)


@login_required
def editQuiz(request, course_name, quiz_id=None):
	context = {}
	context['search'] = SearchForm()
	print(course_name, quiz_id)
	course = Course.objects.get(course_name=course_name)

	if quiz_id == None:
		quiz = Quiz(title="New Quiz" , course=course)
		quiz.save()
		quiz_id = quiz.id

	quiz = Quiz.objects.get(id=quiz_id)

	quiz_json = {'title': quiz.title, 'questions': []}

	for question in quiz.mcquestion_set.all():
		question_json = {'question_text': question.question, 'answers': []}

		for answer in question.choice_set.all():
			answer_json = {'is_correct': answer.isAnswer, 'answer_text': answer.choice}
			question_json['answers'].append(answer_json)

		quiz_json['questions'].append(question_json)

	context['quiz_json'] = json.dumps(quiz_json)
	context['quiz_id'] = quiz_id

	return render(request, 'learnApp/editQuiz.html', context)

@login_required
def saveQuiz(request, quiz_id):

	if request.method != 'POST':
		return HTTPResponseServerError("Must POST")

	quiz = Quiz.objects.get(id=quiz_id)

	old_questions = quiz.mcquestion_set.all()
	old_questions.delete()


	print(request.body)
	quiz_json = json.loads(request.body.decode('utf-8'))

	if len(quiz_json) == 0:
		quiz.delete()
		return HttpResponse("{quiz_id} deleted")

	try:
		quiz.title = quiz_json['title']
		quiz.save()

		for question_json in quiz_json['questions']:
			question = MCQuestion(question = question_json['question_text'], quiz = quiz)
			question.save()

			for answer_json in question_json['answers']:
				answer = Choice(choice = answer_json['answer_text'], isAnswer = answer_json['is_correct'], question = question)
				answer.save()


	except Exception as e:
		print(e)
		return HttpResponseServerError("Malformed Data")

	return HttpResponse("OK")

@login_required
def takeQuiz(request, quiz_id):
	context = {}
	context['search'] = SearchForm()

	quiz = Quiz.objects.get(id=quiz_id)
	co = quiz.course
	context['course'] = co
	if not request.POST:
		context['quiz'] = TakeQuizForm(quiz=quiz)
		context['id'] = quiz_id
		return render(request, 'learnApp/takeQuiz.html', context)
	else:
		quiz_form = TakeQuizForm(request.POST, quiz=quiz)
		context['quiz'] = quiz_form
		if quiz_form.is_valid():
			context['score'] = quiz_form.cleaned_data['score']*100
			grade = QuizGrade(grade=quiz_form.cleaned_data['score'], quiz=quiz, user=request.user, course=co)
			grade.save()
			context['graded'] = QuizGrade.objects.filter(course=co, user=request.user)
			return redirect('/grades/'+co.course_name)


@login_required
def grades(request, name):
	context = {}
	context['search'] = SearchForm()
	c = Course.objects.get(course_name=name)
	context['course'] = c
	context['graded'] = QuizGrade.objects.filter(course=c, user=request.user)
	return render(request, 'learnApp/grades.html', context)


def register(request):
	context = {}
	form = RegistrationForm(request.POST)
	context['login'] = LoginForm()
	context['register'] = form
	context['search'] = SearchForm()
	if not form.is_valid():

		return render(request, 'learnApp/home.html', context)

	new_user = (User.objects.create_user(username=form.cleaned_data['username'],
										password=form.cleaned_data['password1'],
										first_name=form.cleaned_data['firstname'],
										last_name=form.cleaned_data['lastname'],
										email=form.cleaned_data['email']))
	new_user.save()
	new_user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password1'])

	login(request, new_user)
	return redirect('/')
