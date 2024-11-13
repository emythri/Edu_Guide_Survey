from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control 
from .forms import CreateUserForm

def home(request):
    return render(request, 'home.html')

def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

# def survey_detail(request, survey_id):
#     survey = get_object_or_404(Survey, id=survey_id)
#     questions = survey.questions.all()

#     if request.method == 'POST':
#         form = SurveyResponseForm(request.POST, survey_questions=questions)
#         if form.is_valid():
#             score = calculate_score(form.cleaned_data)
#             return render(request, 'results.html', {'score': score})
#     else:
#         form = SurveyResponseForm(survey_questions=questions)

#     return render(request, 'survey_detail.html', {'survey': survey, 'form': form})


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        form = SurveyResponseForm(request.POST, survey_questions=questions)
        if form.is_valid():
            responses = form.cleaned_data
            score = calculate_score(responses)
            return render(request, 'results.html', {'score': score})
    else:
        form = SurveyResponseForm(survey_questions=questions)

    return render(request, 'survey_detail.html', {'survey': survey, 'form': form})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
# def create_survey(request):
#     if request.method == 'POST':
#         form = SurveyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('survey_list')
#     else:
#         form = SurveyForm()
#     return render(request, 'create_survey.html', {'form': form})
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Create a survey instance but don't save it to the database yet
            survey = form.save(commit=False)  # This creates an instance but does not save it
            
            # Assign the creator as the currently logged-in user
            survey.creator = request.user
            
            # Now save the survey to the database
            survey.save()
            
            return redirect('survey_list')  # Redirect to the survey list or another page
    else:
        form = SurveyForm()

    return render(request, 'create_survey.html', {'form': form})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    # #neww
    # if survey.creator != request.user:
    #     messages.error(request, "You are not authorized to edit this survey.")
    #     return redirect('survey_list') 
    # #ends here#
    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_list')
    else:
        form = SurveyForm(instance=survey)
    return render(request, 'edit_survey.html', {'form': form, 'survey': survey})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    #     #neww
    # if survey.creator != request.user:
    #     messages.error(request, "You are not authorized to delete this survey.")
    #     return redirect('survey_list') 
    # #ends here#
    if request.method == 'POST':
        survey.delete()
        return redirect('survey_list')
    return render(request, 'confirm_delete.html', {'object': survey, 'object_type': 'survey'})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def create_question(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    #     #neww
    # if survey.creator != request.user:
    #     messages.error(request, "You are not authorized to edit this survey by creating questions.")
    #     return redirect('survey_list') 
    # #ends here#
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('survey_detail', survey_id=survey.id)
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form, 'survey': survey})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    #     #neww
    # if survey.creator != request.user:
    #     messages.error(request, "You are not authorized to edit questions of this survey.")
    #     return redirect('survey_list') 
    # #ends here#
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('survey_detail', survey_id=question.survey.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'edit_question.html', {'form': form, 'question': question})

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    #     #neww
    # if survey.creator != request.user:
    #     messages.error(request, "You are not authorized to edit this survey by deleting questions.")
    #     return redirect('survey_list') 
    # #ends here#
    survey_id = question.survey.id
    if request.method == 'POST':
        question.delete()
        return redirect('survey_detail', survey_id=survey_id)
    return render(request, 'confirm_delete.html', {'object': question, 'object_type': 'question'})

# def calculate_score(data):
#     score = 0
#     for key, value in data.items():
#         if value == 'A':
#             score += 1
#         elif value == 'B':
#             score += 2
#         elif value == 'C':
#             score += 3
#         elif value == 'D':
#             score += 4
#     return score

def calculate_score(responses):
    score = 0
    for question_id, answer in responses.items():
        score =score + 5 *  int(answer)  # Convert the answer to an integer and add to the score
    return score


def loginPage(request): 
    if request.user.is_authenticated: 
        return redirect('home') 
    else: 
        if request.method=='POST': 
            username=request.POST.get('username') 
            password=request.POST.get('password') 
            print(username, password) 
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user) 
                return redirect('home') 
            else: 
                messages.success(request,"Username or Password is incorrect") 
        context={} 
        return render(request,'login.html',context)

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def logoutPage(request): 
    logout(request) 
    return redirect('login') 

def registerPage(request): 
    form=CreateUserForm() 
    if request.method=="POST": 
        form=CreateUserForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('login') 
        else: 
            messages.success(request,"Password does not follow the rules") 
    context={'form':form} 
    return render(request, 'register.html', context) 
