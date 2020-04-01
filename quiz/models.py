from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

class Subject(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Subject"))
    slug = models.SlugField(unique=True)
    overview = models.CharField(max_length=400,verbose_name=_("Overview"))
    duration = models.CharField(max_length=20,verbose_name=_("Duration"))

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Subject,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quiz:questions', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='question_subject')
    question_text = models.CharField(max_length=250,verbose_name=_("Question Text"))
    # question_image = models.ImageField(upload_to='')
    position = models.IntegerField()

    def __str__(self):
        return self.question_text

    class Meta:
        unique_together = [
            # no duplicated position per question 
            ("question_text", "position") 
        ]
        ordering = ("position",)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_choice = models.CharField(max_length=50,verbose_name=_("Answer_Choice"))
    correct_answer = models.BooleanField(default=False)


    def __str__(self):
        return self.answer_choice

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "answer_choice")
        ]


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Subject)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Activities(models.Model):
    student = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    score = models.IntegerField()
    taken_date = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    # time_taken = models.CharField(null=True,blank=True)

    def __str__(self):
        return self.student.username
    
    class Meta():
        ordering = ['-score']


    