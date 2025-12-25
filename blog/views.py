from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm
from django.db.models import Q


def index(request):
    pass

def blog_detail(request):
    pass

def pub_blog(request):
    pass

def pub_comment(request):
    pass

def search(request):
    pass

