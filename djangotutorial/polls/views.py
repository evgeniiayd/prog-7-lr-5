from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Исключает любые вопросы, которые еще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] возвращает ID выбранного варианта в виде строки
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Переотобразить форму вопроса с сообщением об ошибке
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Используем F() для избежания состояния гонки (race condition)
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Всегда возвращайте HttpResponseRedirect после успешной обработки POST данных.
        # Это предотвращает повторную отправку данных, если пользователь нажал кнопку "Назад".
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def create_poll(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')  # Переадресация на список опросов
    else:
        form = QuestionForm()
    return render(request, 'polls/create_poll.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import render
from polls.models import Question
from django.db.models import Q

def analytics_page(request):
    return render(request, 'polls/analytics.html')

def search_votes(request):
    query = request.GET.get('q', '')
    if query:
        questions = Question.objects.filter(question_text__icontains=query)
        return JsonResponse({'questions': list(questions)})
