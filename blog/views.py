from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models.aggregates import Count
from django.contrib.postgres.search import SearchVector

from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

# Create your views here.
def post_list(request: HttpRequest, tag_slug: str = None) -> HttpResponse:
    posts_list = Post.objects.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

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
        tag=tag,
    )

    return render(request=request, template_name='blog/post/list.html', context=context)


def post_detail(request: HttpRequest, year: int, month: int, day: int, slug: str) -> HttpResponse:
    post = get_object_or_404(klass=Post, publish__year=year, publish__month=month, publish__day=day, slug=slug, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)

    form = CommentForm()

    post_tags_ids = post.tags.values_list('pk', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(pk=post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    
    context = dict(
        post=post,
        comments=comments,
        form=form,
        similar_posts=similar_posts,
    )

    return render(request=request, template_name='blog/post/detail.html', context=context)


def post_share(request: HttpRequest, post_pk: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=post_pk, status=Post.Status.PUBLISHED)

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
def post_comment(request: HttpRequest, post_pk: int) -> HttpResponse | HttpResponseNotAllowed:
    post = get_object_or_404(klass=Post, pk=post_pk, status=Post.Status.PUBLISHED)

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

def post_search(request: HttpRequest) -> HttpResponse:
    form = SearchForm()
    query = None
    results = list()

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=query)

    context = dict(
        form=form,
        query=query,
        results=results,
    )

    return render(request=request, template_name='blog/post/search.html', context=context)