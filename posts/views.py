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
import glob
from .fuzzy import *

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
  img_path4 = 'media/images/pict0.png'

  img_result = 'media/images/result1.jpg'
  img_result2 = 'media/images/result2.jpg'
  img_result3 = 'media/images/result3.jpg'
  img_result4 = 'media/images/result0.jpg'

  context = {
    'result1': 'result 1',
    'result2': 'result 2',
    'result3': 'result 3',
    'result4': 'result 4'
  }
  if os.path.exists(img_path) == True & os.path.exists(img_path2) == True & os.path.exists(img_path3) == True & os.path.exists(img_path4) == True:
    input_img_1 = run_all(img_path, 1)
    input_img_2 = run_all(img_path2, 2)
    input_img_3 = run_all(img_path3, 3)
    input_img_4 = run_all(img_path4, 0)

    print(input_img_1[0], input_img_1[1])
    print(input_img_2[0], input_img_2[1])
    print(input_img_3[0], input_img_3[1])
    print(input_img_4[0], input_img_4[1])

    
    # result1 from img1 and img2
    context['duration1'] = input_from_image(input_img_1[0], input_img_1[1], input_img_2[0], input_img_2[1])
    print(context['duration1'])
    # result2 from img2 and img3
    context['duration2'] = input_from_image(input_img_2[0], input_img_2[1], input_img_3[0], input_img_3[1])
    print(context['duration2'])

    # result3 from img3 and img4
    context['duration3'] = input_from_image(input_img_3[0], input_img_3[1], input_img_4[0], input_img_4[1])
    print(context['duration3'])

    # result4 from img4 and img1
    context['duration4'] = input_from_image(input_img_4[0], input_img_4[1], input_img_1[0], input_img_1[1])
    print(context['duration4'])


    # deleting all uploaded images
    for i in range(0, 4):
      os.remove("media/images/pict" + str(i) + ".png")

    return render(request, 'display.html', context)
  elif (os.path.exists(img_result) == True & os.path.exists(img_result2) == True & os.path.exists(img_result3) == True & os.path.exists(img_result4) == True): 
    return render(request, 'display.html', context)
  else :
    return HttpResponse("<h1>FILE NOT FOUND BITCH</h1>")


class CreatePostView(CreateView):  # new
    model = Post
    form_class = PostForm
    template_name = "index.html"
    success_url = reverse_lazy("home")


def calculate(n):
  return n*100

