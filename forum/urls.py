from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post_question/', views.post_question, name='post_question'),
    path('view_question/<int:question_id>/', views.view_question, name='view_question'),
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('comment_answer/<int:answer_id>/', views.comment_answer, name='comment_answer'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('answer/<int:answer_id>/like_dislike/', views.like_dislike_answer, name='like_dislike_answer'),
    path('answer/<int:answer_id>/comment/', views.comment_on_answer, name='comment_on_answer'),
    path('my-questions/', views.my_questions, name='my_questions'),
]
