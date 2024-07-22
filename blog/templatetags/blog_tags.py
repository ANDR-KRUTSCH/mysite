import markdown

from django import template
from django.db.models.aggregates import Count
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.utils.safestring import SafeText

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts() -> int:
    return Post.published.count()

@register.inclusion_tag(filename='blog/post/latest_posts.html')
def show_latest_posts(count: int = 5) -> dict:
    latest_posts = Post.published.order_by('-publish')[:count]
    return dict(latest_posts=latest_posts)

@register.simple_tag
def get_most_commented_posts(count: int = 3) -> QuerySet:
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text: str) -> SafeText:
    return mark_safe(markdown.markdown(text=text))