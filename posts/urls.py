from django.urls import path

# from .views import HomePageView, CreatePostView, homePageView # new
from . import views

urlpatterns = [
    # path("post/", HomePageView.as_view(), name="add_post"),
    path('post/', views.index),
    path("", views.CreatePostView.as_view(), name="home")  # new
]
