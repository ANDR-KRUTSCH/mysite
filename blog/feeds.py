import markdown

from datetime import datetime

from django.utils.safestring import SafeText
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.db.models.query import QuerySet

from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self) -> QuerySet:
        return Post.published.all()[:3]
    
    def item_title(self, item: Post) -> SafeText:
        return item.title
    
    def item_description(self, item: Post) -> str:
        return truncatewords_html(markdown.markdown(item.body), arg=30)
    
    def iten_pubdate(self, item: Post) -> datetime:
        return item.publish