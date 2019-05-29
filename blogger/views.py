from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Setting, Page, Link, User
from .forms import SettingForm, AddPageForm, DelForm, DelFormPassword, LoginForm, CreateForm, ChangeNameForm, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import hashers

import requests, json, markdown


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']):
                messages.error(request, 'Username not found')
                return HttpResponseRedirect(reverse('blogger:login'))
            u = User.objects.get(username=form.cleaned_data['username'])
            if hashers.check_password(form.cleaned_data['password'], u.password):
                request.session['user'] = u.id
                messages.success(request, 'Welcome ' + u.name + '!')
                return HttpResponseRedirect(reverse('blogger:index'))
            else:
                messages.error(request, 'Incorrect password')
                return HttpResponseRedirect(reverse('blogger:login'))
    request.session['helped'] = False
    login_form = LoginForm()
    return render(request, 'blogger/login.html', {
        'login_form': login_form,
    })


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']):
                messages.error(request, 'Username already taken')
                return HttpResponseRedirect(reverse('blogger:create'))
            u = form.save()
            u.password = hashers.make_password(u.password)
            u.save()
            request.session['user'] = u.id
            messages.success(request, 'Welcome ' + u.name + '!')
            if request.session['helped'] == True:
                return HttpResponseRedirect(reverse('blogger:index'))
            else:
                request.session['helped'] = True
                return HttpResponseRedirect(reverse('blogger:help'))
    create_form = CreateForm()
    return render(request, 'blogger/create.html', {
        'create_form': create_form,
    })


def help(request):
    temp = request.session['helped']
    request.session['helped'] = True
    return render(request, 'blogger/help.html', {'helped': temp})


def index(request):
    u = User.objects.get(id=request.session['user'])
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
                messages.success(request, 'Page added successfully')
        elif 'del_page_form' in request.POST:
            id = request.POST['id']
            form = DelForm(request.POST)
            if form.is_valid():
                Page.objects.get(id=id).delete()
                l_set = Link.objects.filter(source=id) | Link.objects.filter(target=id)
                for link in l_set:
                    link.delete()
                messages.success(request, 'Page deleted successfully')
        return HttpResponseRedirect(reverse('blogger:index'))
    else:
        setting_form = SettingForm()
        add_page_form = AddPageForm()
        del_page_form = DelForm()
        return render(request, 'blogger/index.html', {
                'setting_form': setting_form,
                'add_page_form': add_page_form,
                'del_page_form': del_page_form,
            })


def profile(request):
    u = User.objects.get(id=request.session['user'])
    if request.method == 'POST':
        if 'name_form' in request.POST:
            form = ChangeNameForm(request.POST, instance=u)
            if form.is_valid():
                form.save()
                messages.success(request, 'Display name changed successfully')
        elif 'password_form' in request.POST:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['old_password'] != u.password:
                    messages.error(request, 'Incorrect old password')
                else:
                    u.password = form.cleaned_data['new_password']
                    messages.success(request, 'Password changed successfully')
        return HttpResponseRedirect(reverse('blogger:profile'))
    change_name_form = ChangeNameForm()
    change_password_form = ChangePasswordForm()
    return render(request, 'blogger/profile.html', {
        'name': u.name,
        'username': u.username,
        'name_form': change_name_form,
        'password_form': change_password_form,
    })


def delete(request):
    if request.method == 'POST':
        u = User.objects.get(id=request.session['user'])
        form = DelFormPassword(request.POST)
        if form.is_valid():
            if not hashers.check_password(form.cleaned_data['field'], u.password):
                messages.error(request, 'Incorrect password')
                return HttpResponseRedirect(reverse('blogger:delete'))
            u.delete()
            request.session.flush()
            messages.success(request, 'User deleted successfully')
            return HttpResponseRedirect(reverse('blogger:login'))
    del_user_form = DelFormPassword()
    return render(request, 'blogger/delete.html', {
        'del_user_form': del_user_form,
    })


def link(request):
    return HttpResponse('hi')


def logout(request):
    request.session.flush()
    messages.success(request, 'Logout successful')
    return HttpResponseRedirect(reverse('blogger:login'))


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
