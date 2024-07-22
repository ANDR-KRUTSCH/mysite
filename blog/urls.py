from django.urls import path

from . import views, feeds

app_name = 'blog'

urlpatterns = (
    path(route='', view=views.post_list, name='post_list'),
    path(route='tag/<slug:tag_slug>/', view=views.post_list, name='post_list_by_tag'),
    path(route='<int:year>/<int:month>/<int:day>/<slug:slug>/', view=views.post_detail, name='post_detail'),
    path(route='<int:post_pk>/share/', view=views.post_share, name='post_share'),
    path(route='<int:post_pk>/comment/', view=views.post_comment, name='post_comment'),
    path(route='search/', view=views.post_search, name='post_search'),
    path(route='feed/', view=feeds.LatestPostsFeed(), name='post_feed'),
)