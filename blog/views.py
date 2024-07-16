from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Post

# Create your views here.
def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request=request, template_name='blog/post/list.html', context=context)

def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=id, status=Post.Status.PUBLISHED)
    
    context = {
        'post': post
    }

    return render(request=request, template_name='blog/post/detail.html', context=context)