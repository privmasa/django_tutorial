from django.test import TestCase
from polls.models import Question
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import resolve_url
from unittest import mock
# Create your tests here.


def dummy_api_func():
    return 'dummy api response'


def api_func():
    return 'api response'


class PollsTest(TestCase):

    def test_was_published_recentrly(self):
        # 1日よりも少しだけ古い
        obj = Question(pub_date=timezone.now() - timedelta(days=1, minutes=1))
        self.assertFalse(obj.was_published_recently(), '1日と1分前に公開')

        # 1日よりも少しだけ新しい
        obj = Question(
            pub_date=timezone.now() - timedelta(days=1) + timedelta(minutes=1))
        self.assertTrue(obj.was_published_recently(), '1日と1分後に公開')

        # つい最近公開
        obj = Question(pub_date=timezone.now() - timedelta(minutes=1))
        self.assertTrue(obj.was_published_recently(), '1分前に公開')

        # もうちょっとしたら公開
        obj = Question(pub_date=timezone.now() + timedelta(minutes=1))
        self.assertFalse(obj.was_published_recently(), '1分後に公開')

    def test_mocked_api(self):
        ret = api_func()
        print('ret:', ret)
        with mock.patch('polls.tests.api_func', dummy_api_func):
            ret = api_func()
            print('mocked_ret:', ret)

    @mock.patch('polls.tests.api_func', dummy_api_func)
    def test_mocked_api_with_decorator(self):
        ret = api_func()
        print('decoretor:', ret)


class ViewTest(TestCase):

    def test_index(self):
        response = self.client.get(resolve_url('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['questions'].count())

        Question.objects.create(
            question='aaa',
            pub_date=timezone.now(),
        )
        response = self.client.get(resolve_url('polls:index'))
        self.assertEqual(1, response.context['questions'].count())

        self.assertEqual('aaa', response.context['questions'].first().question)
