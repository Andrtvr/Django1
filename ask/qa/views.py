from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .models import Question, Answer, QuestionManager
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator


def new_quest(request):

    qs = QuestionManager()
    qs = qs.new()
    page, paginator = paginate(request,qs)
    paginator.baseurl = '?page='

    return render(request, 'qa/new_quest.html', {
        'quest': page.object_list,
        'page': page,
        'paginator': paginator,
    })
'''
def question_list(request):
    qs = Question.objects.all()
    qs = qs.order_by('-added_at')
    page, paginator = paginate(request, qs)
    paginator.baseurl = reverse('question_list') + '?page='

    return render(request, 'list.html', {
        'questions': page.object_list,
        'page': page,
        'paginator': paginator,
    })
'''
def popular(request):
    quest = QuestionManager()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(quest.popular(), limit)
    paginator.baseurl = 'popular/?page='
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'qa/popular.html', {
        'quest': page.object_list,
        'paginator': paginator, 'page': page,
    })

def question(request, slug):
    q = QuestionManager()
    a = Answer()
    quest = q.quest(slug=slug)
    if quest == None:
        raise Http404

    else:
        return render(request, 'qa/quest.html', {
        'quest': quest,
   #     'answer': a.id(),
    })

def qa(request, *args, **kwargs):
    return HttpResponse('qa')
