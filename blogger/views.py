from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Setting, Page
from .forms import SettingForm, AddPageForm, DelPageForm

import requests, json, markdown

# Create your views here.
def index(request):
    if request.method == 'POST':
        if 'setting_form' in request.POST:
            form = SettingForm(request.POST)
            if form.is_valid():
                s = Setting.objects.all()[0]
                s.setting = form.cleaned_data['setting']
                s.save()
                return HttpResponseRedirect(reverse('blogger:index'))
        elif 'add_page_form' in request.POST:
            form = AddPageForm(request.POST)
            if form.is_valid():
                p = Page(title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    color=form.cleaned_data['color'],
                    content=form.cleaned_data['content'])
                p.save()
                return HttpResponseRedirect(reverse('blogger:index'))
        elif 'del_page_form' in request.POST:
            form = DelPageForm(request.POST)
            if form.is_valid():
                print(request.POST)
                return HttpResponseRedirect(reverse('blogger:index'))
    else:
        setting_form = SettingForm()
        add_page_form = AddPageForm()
        del_page_form = DelPageForm()
        return render(request, 'blogger/index.html', {
                'setting_form': setting_form,
                'add_page_form': add_page_form,
                'del_page_form': del_page_form,
            })

def network_json(request):
    if not Setting.objects.all():
        s = Setting(setting='empty')
        s.save()
    setting = Setting.objects.all()[0].setting
    if setting == 'empty':
        return JsonResponse({})
    elif setting == 'sample':
        with open('blogger/test_data.json') as f:
            test_data = json.load(f)
        return JsonResponse(test_data)
    elif setting == 'main':
        data = {
            'nodes_data': [],
            'nodes_all': {
                'addable': 'true',
                'deletable': 'true'
            },
            'links_data': []
        }

        if not Page.objects.filter(title='index'):
            p = Page(title='index', description='index', color='blue', content='')
            p.save()

        for page in Page.objects.all():
            node_data = {
                'name': page.title,
                'color': page.color,
                'innerHTML': '<p>' + page.description + '</p>',
            }

            if page.title == 'index':
                node_data['deletable'] = 'false'
            else:
                node_data['innerHTML'] += '<a href=' + reverse('blogger:page', args=(page.title,)) + '> Visit page </a>'

            data['nodes_data'].append(node_data)

        return JsonResponse(data)

def page(request, title):
    p = get_object_or_404(Page, title=title)
    return render(request, 'blogger/page.html', {
            'title': title,
            'description': p.description,
            'content': markdown.markdown(p.content, safe_mode=True),
        })
