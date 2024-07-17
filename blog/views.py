from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# Create your views here.
def post_list(request: HttpRequest) -> HttpResponse:
    posts_list = Post.objects.all()

    paginator = Paginator(object_list=posts_list, per_page=3)
    
    page_number = request.GET.get(key='page', default=1)

    try:
        posts = paginator.page(number=page_number)
    except EmptyPage:
        posts = paginator.page(number=paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(number=1)

    context = dict(
        posts=posts,
    )

    return render(request=request, template_name='blog/post/list.html', context=context)


def post_detail(request: HttpRequest, year: int, month: int, day: int, slug: str) -> HttpResponse:
    post = get_object_or_404(klass=Post, publish__year=year, publish__month=month, publish__day=day, slug=slug, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)

    form = CommentForm()
    
    context = dict(
        post=post,
        comments=comments,
        form=form,
    )

    return render(request=request, template_name='blog/post/detail.html', context=context)


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = '{} {} recommends you read {}'.format(cleaned_data.get('name'), cleaned_data.get('email'), post.title)
            message = 'Read {} at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cleaned_data.get('name'), cleaned_data.get('comments'))

            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cleaned_data.get('to')])
            
            sent = True
    else:
        form = EmailPostForm()

    context = dict(
        post=post,
        form=form,
        sent=sent,
    )

    return render(request=request, template_name='blog/post/share.html', context=context)


@require_POST
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=post_id, status=Post.Status.PUBLISHED)

    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = dict(
        post=post,
        comment=comment,
        form=form,
    )

    return render(request=request, template_name='blog/post/comment.html', context=context)