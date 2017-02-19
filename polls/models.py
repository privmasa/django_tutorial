from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class QuestionQuerySet(models.query.QuerySet):

    def is_published(self):
        return self.filter(pub_date__lte=timezone.now())


class Question(models.Model):

    class Meta:
        verbose_name = '質問'
        verbose_name_plural = '質問の複数形'
        ordering = ['-pub_date']

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    print('*********** class Qestion')

    objects = models.Manager.from_queryset(QuestionQuerySet)()

    @classmethod
    def get_published_data(cls):
        return cls.objects.is_published()

    def __str__(self):
        print('*********** class Qestion:def __str___')
        return self.question

    def was_published_recently(self):
        print('*********** class Qestion:def was_published_recently')
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_oreder_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    print('*********** class Qestion:def after was_published_recently')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
