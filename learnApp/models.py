# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Course(models.Model):
	course_name = models.CharField(max_length=30, primary_key=True)
	students = models.ManyToManyField(User, related_name="reg_courses", blank=True)
	description = models.TextField()
	category = models.CharField(max_length=30, null=True)
	image = models.ImageField(blank=True, null=True, upload_to="course-images")
	owner = models.ForeignKey(User, null=True, related_name="owned_courses")


class Choice(models.Model):
	choice = models.CharField(max_length=200)
	isAnswer = models.BooleanField(blank=False, default=False)
	question = models.ForeignKey('MCQuestion', on_delete=models.CASCADE)


class MCQuestion(models.Model):
	question = models.CharField(max_length=200)
	quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)


class Quiz(models.Model):
	title = models.CharField(max_length=200, blank=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)


class FRQuestion(models.Model):
	question = models.CharField(max_length=200)
	answer = models.CharField(max_length=200)
	exam = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Lesson(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	course = models.ForeignKey(Course)
	#info = models.TextField(null=True)
	info = models.CharField(max_length=1000000000)

class Checkpoint(models.Model):
	question = models.OneToOneField(MCQuestion)
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class QuizGrade(models.Model):
	grade = models.DecimalField(max_digits=4, decimal_places=2)
	quiz = models.ForeignKey(Quiz, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, null=True)

class CourseGrade(models.Model):
	grade = models.DecimalField(max_digits=4, decimal_places=2)
	course = models.OneToOneField(Course)
	user = models.OneToOneField(User)
