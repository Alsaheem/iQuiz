from django.shortcuts import render,get_object_or_404,redirect,get_list_or_404
from .models import *
from django.views.generic import ListView,TemplateView
from django.contrib.auth.decorators import login_required
# Create your views here.

class SubjectList(ListView):
    model = Subject
    template_name = 'quiz/subjects.html'
    context_object_name = 'subjects'

@login_required
def Questions(request,subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    questions = Question.objects.filter(subject=subject)
    template_name = 'quiz/questions.html'
    context = {'questions':questions,'subject':subject}
    return render(request,template_name,context)

class LeaderBoard(ListView):
    model = Activities
    template_name = 'quiz/leaderboard.html'
    context_object_name = 'leaderboards'

@login_required
def ScoreView(request,subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    if request.method == 'POST':
        all_questions = get_list_or_404(Question,subject=subject)
        score = 0
        for question in all_questions:
            try:
                selected_answer = question.answer_set.get(pk=request.POST.get(str(question.question_text)))
                if selected_answer.correct_answer == True:
                    score += 1
                else:
                    pass
            except Answer.DoesNotExist:
                print('user didnt pick an answer')
        # calculate the time taken for user to finish the test
        # ...Todo later
        print('your score is ',score)
        # create a leaderboard entry
        activity = Activities.objects.create(student=request.user,score=score,subject=subject)
        activity.save()
        # check if the score is the highest in that subject
        all_scores = []
        subject_activities = Activities.objects.filter(subject=subject)
        # print(subject_activities)
        for activity_score in subject_activities:
            # if the id changes , theyll be an error lol....ill come back to this
            act = Activities.objects.get(id=activity_score.id)
            ac_score = act.score
            all_scores.append(ac_score)
        print(all_scores)
        highest_activity_score = max(all_scores)
        if score > highest_activity_score:
            print('youre now the highest person to have ever taken this test ,Youre the new King')
            # email
        elif (score == highest_activity_score):
            print('you got the same score as the former highest , you can do better')
            # send email to user with badge
    context = {'score':score,'subject':subject,'user':request.user,'highest_score':highest_activity_score}
    template_name = 'quiz/scores.html'
    return render(request,template_name,context)

class AboutView(TemplateView):
    template_name = "about.html"

class HomeView(TemplateView):
    template_name = "index.html"

class ContactView(TemplateView):
    template_name = "contact.html"