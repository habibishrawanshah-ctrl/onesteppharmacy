from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import BlogPost


class BlogFeed(Feed):
    title = 'OneStep Pharmacy - Health Blog'
    link = '/health/blog/'
    description = 'Latest health tips, wellness guides, and medical advice from OneStep Pharmacy'

    def items(self):
        return BlogPost.objects.filter(is_published=True)[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content[:200]

    def item_pubdate(self, item):
        return item.published_at
