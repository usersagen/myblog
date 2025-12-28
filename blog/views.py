from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm
from django.db.models import Q
from django.contrib import messages


# 首页
def index(request):
    blogs = Blog.objects.all()
    context = {"blogs": blogs}
    return render(request, 'index.html', context=context)

# 博客详情页
def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog=None
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context=context)

# 发布博客
@require_http_methods(['GET','POST'])
@login_required
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        context = {"categories": categories}
        return render(request, 'pub_blog.html', context=context)
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            category = BlogCategory.objects.filter(id=category_id).first()
            blog = Blog.objects.create(title=title,content=content,category=category, author=request.user)
            context = {"blog_id": blog.id}
            messages.success(request, '博客发布成功！')
            return JsonResponse({
                'code':200,
                'message':'博客发布成功！',
                'context':context
            })
        else:
            messages.error(request, '参数错误！')
            return JsonResponse({
                'code':400,
                'message':'参数错误！'
            })

# 发表评论
@require_POST
@login_required
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content,blog_id=blog_id,author=request.user)
    messages.success(request, '评论成功！')
    # 重载详情页
    return  redirect(reverse('blog:blog_detail',kwargs={'blog_id': blog_id}))

# 搜索博客
def search(request):
    word = request.GET.get('q','')
    blogs = Blog.objects.none()
    if word:
        blogs = Blog.objects.filter(Q(title__icontains=word)|Q(content__icontains=word))
        messages.success(request, f'搜索到{blogs.count()}条博客')
    else:
        messages.error(request, '请输入搜索关键词后再查询')
    context = {'blogs':blogs}
    return render(request, 'index.html', context=context)


