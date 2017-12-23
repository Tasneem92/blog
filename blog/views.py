from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Post, Comment
from . forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # posts = Post.published.all()

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def post_list(request, category=None):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# The post_list view takes the request object as the only parameter,
# retrieving all the posts with the published status using the published manager we created previously
# The render() to render the list of posts with the given template
# This function takes the request object as parameter, the template path & variables to render the given template.
# It return an HttpResponse object with the rendered text (normally HTML code)
# The render() takes the request context into account, so any variable set by template context processors is accessible by the given template


def post_share(request, post_id):
    # Retrieves post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # retrieving the absolute path of the post to include a link to the post in the email
            # We use this path as input for request.build_absolute_uri() to build a complete URL including HTTP schema and hostname

            # We build the subject & the message body of the email using the cleaned data of the validated form
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
            # .. send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
