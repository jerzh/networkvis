from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Setting, Page, Link, User
from .forms import SettingForm, AddPageForm, DelForm, DelFormPassword, LoginForm, CreateForm, ChangeNameForm, ChangePasswordForm, AddLinkForm
# framework for sending alerts to users
from django.contrib import messages
# hashing passwords!
from django.contrib.auth import hashers

import requests, json, markdown


# login page
def login(request):
    # process login form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # check if username exists
            if not User.objects.filter(username=form.cleaned_data['username']):
                # messages is a framework that sends alert(s) to the user
                messages.error(request, 'Username not found')
                return HttpResponseRedirect(reverse('blogger:login'))
            # check password
            u = User.objects.get(username=form.cleaned_data['username'])
            if hashers.check_password(form.cleaned_data['password'], u.password):
                # this is how we know which user is logged in
                request.session['user'] = u.id
                # this stuff is to determine which button(s) to display on the
                # 'help' page
                request.session['helped'] = 'index'
                messages.success(request, 'Welcome ' + u.name + '!')
                return HttpResponseRedirect(reverse('blogger:index'))
            else:
                messages.error(request, 'Incorrect password')
                return HttpResponseRedirect(reverse('blogger:login'))
    request.session['helped'] = 'login'
    login_form = LoginForm()
    return render(request, 'blogger/login.html', {
        'login_form': login_form,
    })


# create new user page
def create(request):
    # process create user form
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            # check if username has been taken
            if User.objects.filter(username=form.cleaned_data['username']):
                messages.error(request, 'Username already taken')
                return HttpResponseRedirect(reverse('blogger:create'))
            u = form.save()
            u.password = hashers.make_password(u.password)
            u.save()
            # this is how we know which user is logged in
            request.session['user'] = u.id
            messages.success(request, 'Welcome ' + u.name + '!')
            # go to 'index' if user has already seen 'help' page, 'help' otherwise
            if request.session['helped'] == 'helped':
                return HttpResponseRedirect(reverse('blogger:index'))
            else:
                request.session['helped'] = 'helped'
                return HttpResponseRedirect(reverse('blogger:help'))
    create_form = CreateForm()
    return render(request, 'blogger/create.html', {
        'create_form': create_form,
    })


# help page
def help(request):
    temp = request.session['helped']
    # bug: if the user reloads the page, the button will change from 'Get started'
    # to 'Onward!'
    request.session['helped'] = 'helped'
    return render(request, 'blogger/help.html', {'helped': temp})


# index page (displays network)
def index(request):
    # request.session['page'] tells us which page to go back to if the user got
    # to a page via another
    request.session['page'] = None
    # determine which button(s) to display on the 'help' page
    if request.session['helped'] == 'helped':
        request.session['helped'] = 'index'
    u = User.objects.get(id=request.session['user'])
    # process form, whichever was submitted
    if request.method == 'POST':
        # process setting_form
        if 'setting_form' in request.POST:
            # via Django ModelForm we can modify models easily
            # this says to change the model instance according to the form
            form = SettingForm(request.POST, instance=Setting.objects.all()[0])
            if form.is_valid():
                form.save()
        # process add_page_form
        elif 'add_page_form' in request.POST:
            id = request.POST['id']
            form = AddPageForm(request.POST)
            if form.is_valid():
                # this says to save a new model instance according to the form
                p = form.save()
                # add user to p.authors
                p.authors = [u.id]
                p.save()
                # add new link based on the node that the add_page_form was
                # submitted from
                Link(source=id, target=p.id, color='green').save()
                messages.success(request, 'Page added successfully')
        # process del_page_form
        elif 'del_page_form' in request.POST:
            id = request.POST['id']
            form = DelForm(request.POST)
            if form.is_valid():
                # delete page and all links that include the page
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


# profile page
def profile(request):
    u = User.objects.get(id=request.session['user'])
    if request.method == 'POST':
        # process name_form
        if 'name_form' in request.POST:
            # change the user instance according to the form
            form = ChangeNameForm(request.POST, instance=u)
            if form.is_valid():
                form.save()
                messages.success(request, 'Display name changed successfully')
        # process password_form
        elif 'password_form' in request.POST:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                # if old password matches, set password to new password
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
        'change': True,
        'page': request.session['page'],
        'name_form': change_name_form,
        'password_form': change_password_form,
    })


# view user page (similar to profile page but with no edit capabilities)
def user(request, id):
    # if it's the user that's logged in, just redirect to their profile page
    if id == request.session['user']:
        return HttpResponseRedirect(reverse('blogger:profile'))
    u = User.objects.get(id=id)
    return render(request, 'blogger/profile.html', {
        'name': u.name,
        'username': u.username,
        'change': False,
        'page': request.session['page'],
    })


# delete user confirmation page
def delete(request):
    # process delete user confirmation form
    if request.method == 'POST':
        u = User.objects.get(id=request.session['user'])
        form = DelFormPassword(request.POST)
        if form.is_valid():
            # if password is wrong, redirect
            if not hashers.check_password(form.cleaned_data['field'], u.password):
                messages.error(request, 'Incorrect password')
                return HttpResponseRedirect(reverse('blogger:delete'))
            # else delete + logout
            u.delete()
            request.session.flush()
            messages.success(request, 'User deleted successfully')
            return HttpResponseRedirect(reverse('blogger:login'))
    del_user_form = DelFormPassword()
    return render(request, 'blogger/delete.html', {
        'del_user_form': del_user_form,
    })


# add link page
def add_link(request):
    # process add link form
    if request.method == 'POST':
        form = AddLinkForm(request.POST)
        if form.is_valid():
            l = form.save()
            if (not Page.objects.filter(title=l.source)) or (not Page.objects.filter(title=l.target)):
                messages.error(request, 'Page(s) not found')
                return HttpResponseRedirect(reverse('blogger:add_link'))
            else:
                l.source = Page.objects.get(title=l.source).id
                l.target = Page.objects.get(title=l.target).id
                l.save()
                return HttpResponseRedirect(reverse('blogger:index'))
    add_link_form = AddLinkForm()
    return render(request, 'blogger/add_link.html', {
        'add_link_form': add_link_form,
    })


# page displaying a link
def link(request, id):
    return HttpResponse('hi')


# logout page (not actually a page, just redirects)
def logout(request):
    request.session.flush()
    messages.success(request, 'Logout successful')
    return HttpResponseRedirect(reverse('blogger:login'))


# returns the json representing the network
def network_json(request):
    # if setting is unset, set it to 'empty'
    if not Setting.objects.all():
        s = Setting(setting='empty')
        s.save()
    setting = Setting.objects.all()[0].setting

    # if 'empty', return nothing
    if setting == 'empty':
        return JsonResponse({})

    # if 'sample', return sample data
    elif setting == 'sample':
        with open('blogger/test_data.json') as f:
            test_data = json.load(f)
        return JsonResponse(test_data)

    # if 'main', collect data about pages
    elif setting == 'main':
        data = {
            'nodes_data': [],
            'nodes_all': {
                'addable': 'true',
                'deletable': 'true'
            },
            'links_data': []
        }

        # if 'index' node doesn't exist, create it (because I was too lazy to
        # add it manually)
        if not Page.objects.filter(title='index'):
            p = Page(title='index', description='index', color='blue', content='')
            p.save()

        # iterate through pages, insert contents into nodes
        for page in Page.objects.all():
            node_data = {
                'id': page.id,
                'name': page.title,
                'color': page.color,
                'innerHTML': markdown.markdown(page.description, safe_mode=True),
            }

            # you can't delete 'index'
            if page.title == 'index':
                node_data['deletable'] = 'false'
            # put 'Visit page' link
            else:
                node_data['innerHTML'] += '<a href=' + reverse('blogger:page', args=(page.id,)) + '> Visit page </a>'

            data['nodes_data'].append(node_data)

        # iterate through links, insert contents into links
        for link in Link.objects.all():
            link_data = {
                'source': link.source,
                'target': link.target,
                'color': link.color,
            }

            data['links_data'].append(link_data)

        return JsonResponse(data)


# display a page
def page(request, id):
    request.session['page'] = id
    # when 'save changes' is clicked
    if request.method == 'POST':
        p = get_object_or_404(Page, id=id)
        # save all of the changes
        p.title = request.POST['title']
        p.description = request.POST['description']
        p.content = request.POST['content']
        p.color = request.POST['color']
        p.desc_color = request.POST['desc-color']
        # add new author if it was added
        if request.POST['author'] != '+':
            if not User.objects.filter(username=request.POST['author']):
                messages.error(request, 'User not found')
            else:
                user_id = User.objects.get(username=request.POST['author']).id
                if user_id in p.authors:
                    messages.error(request, 'User is already an author')
                else:
                    p.authors.append(user_id)
        p.save()
        return HttpResponseRedirect(reverse('blogger:page', args=(id,)))
    else:
        p = get_object_or_404(Page, id=id)

        # p.authors contains User id's, so turn them into User objects
        # decide whether page should be editable based on whether there are
        # 'admin' or 'admin-frozen' authors
        authors = []
        admin_frozen = False
        admin = False
        editable = False
        addable = True
        if not p.authors:
            p.authors.append('admin')
        for author in p.authors:
            if author == 'admin-frozen':
                admin_frozen = True
            elif author == 'admin':
                admin = True
            else:
                if int(author) == request.session['user']:
                    editable = True
                authors.append(get_object_or_404(User, id=author))
        if admin_frozen:
            editable = False
            addable = False
        elif admin:
            editable = True
            addable = False
        return render(request, 'blogger/page.html', {
                'id': id,
                'title': p.title,
                'admin': admin,
                'authors': authors,
                'description': markdown.markdown(p.description, safe_mode=True),
                'content': markdown.markdown(p.content, safe_mode=True),
                'color': p.color,
                'desc_color': p.desc_color,
                'editable': editable,
                'addable': addable,
            })
