from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Setting, Page, Link
from .forms import SettingForm, AddPageForm, DelPageForm

import requests, json, markdown


def login(request):
    return HttpResponseRedirect(reverse('blogger:index'))


def index(request):
    if request.method == 'POST':
        if 'setting_form' in request.POST:
            form = SettingForm(request.POST, instance=Setting.objects.all()[0])
            if form.is_valid():
                form.save()
        elif 'add_page_form' in request.POST:
            id = request.POST['id']
            form = AddPageForm(request.POST)
            if form.is_valid():
                p = form.save()
                p.save()
                Link(source=id, target=p.id, color='green').save()
        elif 'del_page_form' in request.POST:
            id = request.POST['id']
            form = DelPageForm(request.POST)
            if form.is_valid():
                Page.objects.get(id=id).delete()
                l_set = Link.objects.filter(source=id) | Link.objects.filter(target=id)
                for link in l_set:
                    link.delete()
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
                'id': page.id,
                'name': page.title,
                'color': page.color,
                'innerHTML': markdown.markdown(page.description, safe_mode=True),
            }

            if page.title == 'index':
                node_data['deletable'] = 'false'
            else:
                node_data['innerHTML'] += '<a href=' + reverse('blogger:page', args=(page.id,)) + '> Visit page </a>'

            data['nodes_data'].append(node_data)

        for link in Link.objects.all():
            link_data = {
                'source': link.source,
                'target': link.target,
                'color': link.color,
            }

            data['links_data'].append(link_data)

        return JsonResponse(data)


def page(request, id):
    if request.method == 'POST':
        p = get_object_or_404(Page, id=id)
        # there has to be a more efficient way of doing this but idk
        p.title = request.POST['title']
        p.description = request.POST['description']
        p.content = request.POST['content']
        p.color = request.POST['color']
        p.desc_color = request.POST['desc-color']
        p.save()
        return HttpResponseRedirect(reverse('blogger:page', args=(id,)))
    else:
        p = get_object_or_404(Page, id=id)
        return render(request, 'blogger/page.html', {
                'id': id,
                'title': p.title,
                'description': markdown.markdown(p.description, safe_mode=True),
                'content': markdown.markdown(p.content, safe_mode=True),
                'color': p.color,
                'desc_color': p.desc_color,
            })
