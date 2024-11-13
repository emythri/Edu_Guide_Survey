from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('surveys/', survey_list, name='survey_list'),
    path('survey/<int:survey_id>/', survey_detail, name='survey_detail'),
    path('survey/create/', create_survey, name='create_survey'),
    path('survey/edit/<int:survey_id>/', edit_survey, name='edit_survey'),
    path('survey/delete/<int:survey_id>/', delete_survey, name='delete_survey'),
    path('survey/<int:survey_id>/question/create/', create_question, name='create_question'),
    path('question/edit/<int:question_id>/', edit_question, name='edit_question'),
    path('question/delete/<int:question_id>/', delete_question, name='delete_question'),
    path('login/',views.loginPage, name='login'), 
    path('logout/',views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

]
