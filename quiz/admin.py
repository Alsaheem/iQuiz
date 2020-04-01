from django.contrib import admin
from quiz.models import *

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'subject','position')
    fieldsets =  [
                (None, {'fields': ['question_text','subject','position']}),
                ]
    inlines = [AnswerInline]

class SubjectAdmin(admin.ModelAdmin):
    # this below code is to prepopulate the slug with a name already
    prepopulated_fields = {'slug':('name',)}

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_choice','question','correct_answer')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('student','score','taken_date')

# Register your models here.
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(Activities,ActivityAdmin)