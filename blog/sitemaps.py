from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models.query import QuerySet

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self) -> QuerySet:
        return Post.published.all()
    
    def lastmod(self, item: Post) -> datetime:
        return item.updated