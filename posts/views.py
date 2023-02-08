from django.views.generic import ListView
from .models import Post
from django.views.generic import ListView, CreateView  # new
from django.urls import reverse_lazy  
from .forms import PostForm  # new
from .models import Post
from .learning import *
import os
from django.http import HttpResponse
from pathlib import Path
from .learning import *
from django.shortcuts import render

x = False

class HomePageView(ListView):
    model = Post
    template_name = "home.html"

def index2(request):
  context = {
    'result1': 'result 1',
    'result2': 'result 2',
    'result3': 'result 3',
    'result4': 'result 4'
  }
  return render(request, 'display.html', context)

def index(request):
  img_path = 'media/images/pict1.png'
  img_path2 = 'media/images/pict2.png'
  img_path3 = 'media/images/pict3.png'
  img_path4 = 'media/images/pict4.png'
  context = {
    'result1': 'result 1',
    'result2': 'result 2',
    'result3': 'result 3',
    'result4': 'result 4'
  }
  if os.path.exists(img_path) == True & os.path.exists(img_path2) == True & os.path.exists(img_path3) == True & os.path.exists(img_path4) == True:
    run_all(img_path, 1)
    run_all(img_path2, 2)
    run_all(img_path3, 3)
    run_all(img_path4, 4)
    return render(request, 'display.html', context)
  else :
    return HttpResponse("<h1>File is Not Found</h1>")


class CreatePostView(CreateView):  # new
    model = Post
    form_class = PostForm
    template_name = "index.html"
    success_url = reverse_lazy("home")


def calculate(n):
  return n*100

