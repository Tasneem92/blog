from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from . models import Post

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # Retrieving the objects to be included in the feed
    def items(self):
        return Post.published.all()[:5]

    # The next 2 methods, recieve each object returned by items()
    # & return the title & description for each item
    def item_title(self, item):
        return item.title

    # We use the truncatewords to build th description of the blog post
    # with the first 30 words
    def item_description(self, item):
        return truncatewords(item.body, 30)

# With RSS it is possible to distribute up-to-date web content from one website
# to thousands of other websites around the world.
# RSS allows fast browsing for news and updates.

#    RSS stands for Really Simple Syndication
#    RSS allows you to syndicate your site content
#    RSS defines an easy way to share and view headlines and content
#    RSS files can be automatically updated
#    RSS allows personalized views for different sites
#    RSS is written in XML

# Without RSS, users will have to check your site daily for new updates.
# This may be too time-consuming for many users. With an RSS feed
# (RSS is often called a News feed or RSS feed)
# they can check your site faster using an RSS aggregator
# (a site or program that gathers and sorts out RSS feeds).
# title, link and descriptions are RSS elements
