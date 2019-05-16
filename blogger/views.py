from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
# from .forms import
# from .models import

# Create your views here.
def index(request):
    return HttpResponse('you did it')
