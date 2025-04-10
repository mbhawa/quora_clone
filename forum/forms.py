from django import forms
from django.contrib.auth.models import User
from .models import Question, Answer, Comment

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
