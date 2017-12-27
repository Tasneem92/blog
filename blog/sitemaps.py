from django.contrib.sitemaps import Sitemap
from . models import Post

# A sitemap is an XML file that tells search engines the page of your website, their relevance & how frequently they are updated
# By using sitemap, you'll help crawlers indexing your wbesite's content
# The Django sitemao framework depends on django.contrib.sites, which allows you to associate objects to
# particualr websites  that are running with your project. This comes handy when you want to run multiple sites using a single Django
# project. To install the sitemap framework, we need to activate both the sites and the sitemap apps in our project

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = '0.9'

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish

# The changefreq & priority attributes inidicate the change frequency of your post pages
# Both can be attributes or methods
# & their relevance in your website (maximum value is 1)
# The items() method returns the QuerySet of bjects to include in this sitemap
# By default, Django calls the get_absolute_url() method on each object to retrieve it's URL
# The domain used to build the URLs is example.com.
# This domain comes from a Site object stored in the databse
# This object has been created when we synced the sites framework with out database
