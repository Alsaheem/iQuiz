from quiz.views import *
from django.urls import path

app_name = 'quiz'

urlpatterns = [
    
    path('',HomeView.as_view(), name='home'),
    path('about/',AboutView.as_view(), name='about'),
    path('contact/',ContactView.as_view(), name='contact'),
    path('subjects/',SubjectList.as_view(), name='subjects'),
    path('<slug:subject_slug>/questions/',Questions,name='questions'),
    path('leaderboard/',LeaderBoard.as_view(), name='leaderboard'),
    path('<slug:subject_slug>/score/',ScoreView, name='score'),

]