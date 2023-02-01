from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

# from django.shortcuts import render
# from django.http import Http404
# from django.template import loader

from .models import Question
# Create your views here.
class IndexView(generic.ListView):
  # latest_question_list = Question.objects.order_by('-pub_date')[:5]
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'
  
  def get_queryset(self):
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
    
  
class DetailView(generic.ListView):
  model = Question
  template_name = 'polls/detail.html'
  def get_queryset(self):
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class ResultsView(generic.ListView):
  model = Question
  template_name = 'polls/detail.html'

def vote(request,question_id):
  question = get_object_or_404(Question,pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except(KeyError,Choice.DoesNotExist):
    return render(request,'polls/detail.html',{
      'question':question,
      'error_message':"You didn't selext a choice"
    })
  else:
    selected_choice.vote += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results',arg=(question_id,)))
  # return HttpResponse("You're looking %s." % question_id)
