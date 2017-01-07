from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import Http404
# from django.template import loader

from .models import Question
from .forms import MyForm
from .models import Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

#     template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
#     return HttpResponse(template.render(context, request))


def detail(request, pk):
    #     try:
    #         question = Question.objects.get(pk=pk)
    #     except Question.DoesNotExist:
    #         raise Http404("Question does not exist")

    obj = get_object_or_404(Question, pk=pk)

    return render(request, 'polls/detail.html', {'question': obj})


def results(request, pk):
    obj = get_object_or_404(Question, pk=pk)
    return render(request, 'polls/results.html', {
        'question': obj,
    })


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', pk)


def form_test(request):
    if request.method == "POST":
        form = MyForm(data=request.POST)
        if form.is_valid():
            pass
    else:
        form = MyForm()

    return render(request, 'polls/form.html', {
        'form': form,
    })
