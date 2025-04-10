from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, LikeDislike, Comment
from .forms import UserLoginForm, UserRegisterForm, QuestionForm, AnswerForm, CommentForm

def home(request):
    questions = Question.objects.all()
    return render(request, 'forum/home.html', {'questions': questions})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'forum/post_question.html', {'form': form})

def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()

    for answer in answers:
        answer.like_count = answer.likes_dislikes.filter(is_like=True).count()
        answer.dislike_count = answer.likes_dislikes.filter(is_like=False).count()
        answer.comments_list = answer.comments.all()  # ✅ ADD THIS LINE

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('view_question', question_id=question_id)
    else:
        answer_form = AnswerForm()

    return render(request, 'forum/view_question.html', {
        'question': question,
        'answers': answers,
        'answer_form': answer_form
    })
@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    like, created = LikeDislike.objects.get_or_create(answer=answer, user=request.user)
    if like.is_like:
        like.is_like = False
    else:
        like.is_like = True
    like.save()
    return redirect('view_question', question_id=answer.question.id)

@login_required
def comment_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.answer = answer
            comment.save()
            return redirect('view_question', question_id=answer.question.id)
    else:
        form = CommentForm()
    return render(request, 'forum/comment_answer.html', {'form': form, 'answer': answer})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                print(1)
                login(request, user)
                print("login success")
                return redirect('home')  # Redirect to the homepage after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'forum/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'forum/register.html', {'form': form})


@login_required
def like_dislike_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    is_like = request.GET.get('is_like') == 'true'

    existing = LikeDislike.objects.filter(answer=answer, user=request.user).first()
    if existing:
        existing.is_like = is_like
        existing.save()
    else:
        LikeDislike.objects.create(answer=answer, user=request.user, is_like=is_like)

    return JsonResponse({
        'likes': answer.likes_dislikes.filter(is_like=True).count(),
        'dislikes': answer.likes_dislikes.filter(is_like=False).count()
    })


# Add a comment to an answer
@login_required
def comment_on_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    content = request.POST.get('content')

    if content:
        Comment.objects.create(answer=answer, user=request.user, content=content)
        print("Comment saved!")  # Debug print

    return redirect('view_question', question_id=answer.question.id)

@login_required
def my_questions(request):
    questions = Question.objects.filter(user=request.user)
    return render(request, 'forum/my_questions.html', {'questions': questions})
