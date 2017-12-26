from django import template

register = template.Library()

from .. models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

@register.simple_tag
def total_posts():
    return Post.published.count()

# Create a simple tag to retrieve the total posts published so far in the blog
# Each template tags module needs to contain a variable called register to be a valid tag library
# The variable is an instance of template.Library & it's used to register your own template tags & filters
# Defining a tag called total_posts with a Python function & using @register.simple_tag to define the function as a
# simple tag & register it, Django will use function's name as the tag name
# If you want to specify it with a different name you can specify a name attribute
# like @register.simple_tag(name='my_tag')
# Before using custom tags, make them available for the template using {% load %} tag


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# Create another tag to display the latest posts in the siebar of our blog.
# Using inclusion tag, you can render a template with context variables
# returned by your template tag
# we specified the template that has to be renduered with the returned values
# with blog/post/latest_posts.html
# count = 5 spceifies the number of comments we want to display, we use it to limit
# the results of the query Post.published.order_by('-publish')[:count]
# Inclusion tags return a dictionary of values used as the context to render the specified template


@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments = Count('comments')
                ).order_by('-total_comments')[:count]

# This QuerySet uses the annotate() function for query aggregation
# using the Count aggregation function.
# We build a QuerySet aggregating the total number of comments for each post
# in a total_comments field and we order the QuerySet by this field
# count is an option variable to limit the total number of objects returned to a given value

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# We use the mark_safe function provided by Django to mark the result as safe HTML
# to be rendered in the template. By default Django will not trust any HTML code
# & will escape it before placing it into the output/
# The only except are variables that are marked safe from escaping
# This prevents Django from outputting potentially dangerous HTML &
# allows you to create exceptions when you know you are returning safe HTML
