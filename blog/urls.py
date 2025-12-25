from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('blog_detail/<int:blog_id>',views.blog_detail,name='blog_detail'),
    path('pub_blog',views.pub_blog,name='pub_blog'),
    path('pub_comment',views.pub_comment,name='pub_comment'),
    path('search',views.search,name='search'),
]