from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Question, Choice


# Get Question and display them
def index(request):
    latest_question_lists = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_lists': latest_question_lists}
    return render(request, 'polls/index.html', context);


# This will show specifi question details
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', { 'question': question })


# Get question and dispaly results
def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        print('Coming in error')
        return render(request, 'polls/detail.html',{ 
            'question': question, 
            'error_message': 'You Haven\'t selected any choice' 
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


    