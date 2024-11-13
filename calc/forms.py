 # calc/forms.py
from django import forms
from .models import *
from .models import Question
from django.contrib.auth.forms import UserCreationForm 
from django import forms  
from django.contrib.auth.models import User 

# class SurveyResponseForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         survey_questions = kwargs.pop('survey_questions')
#         super().__init__(*args, **kwargs)
#         for question in survey_questions:
#             self.fields[f'question_{question.id}'] = forms.ChoiceField(
#                 label=question.text,
#                 choices=[
#                     ('A', question.option_a),
#                     ('B', question.option_b),
#                     ('C', question.option_c),
#                     ('D', question.option_d)
#                 ],
#                 widget=forms.RadioSelect
#             )

from django import forms

class SurveyResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        survey_questions = kwargs.pop('survey_questions')
        super().__init__(*args, **kwargs)

        for question in survey_questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[(i, str(i)) for i in range(1, 6)],  # Scale from 1 to 5
                label=question.text,
                widget=forms.RadioSelect
            )


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        #fields = ['survey', 'text']
        fields = ['text']
        #fields = ['survey', 'text', 'option_a', 'option_b', 'option_c', 'option_d']


class CreateUserForm(UserCreationForm): 
    class Meta: 
        model=User 
        fields=["username","email","password1","password2"]