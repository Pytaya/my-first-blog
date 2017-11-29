from django.shortcuts import render, get_object_or_404,redirect, render_to_response
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .pagin_class import PageClass
from markdown2 import markdown
from django.utils.encoding import force_text
# from django.utils.safestring import mark_safe
# import json

# Create your views here.
def post_list(request, current_page=1):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # return render(request, 'blog/post_list.html', {'posts': posts})
    
    current_page = int(current_page)
    # per_item = 3  # 每页条数
    per_item = int(request.COOKIES.get('pager_num',3))
    
    show_page_cout = 5  # 想要展示的页数
    
    # PageClass参数: app_name  models.class_name  current_page
    pageclass = PageClass('blog','Post',current_page)
    result,count,all_page_count = pageclass.data_DataCount_AllPageCount(per_item)
    page_list = pageclass.pageList(all_page_count,show_page_cout)
    pre_page,nex_page = pageclass.prePage_NexPage(all_page_count)
    
    if current_page > all_page_count:
        return redirect('post_list', current_page=all_page_count)
    ret = {
    'posts':result,
    # 'count':count,
    'page_list':page_list,
    'last_page':all_page_count,
    'pre_page':pre_page,
    'nex_page':nex_page,
    'current_page':current_page,
    }
    
    response = render(request, 'blog/post_list.html',ret)
    return response


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.text = mark_safe(markdown(post.text))
    txt = ""
    for line in post.text.strip().split("\r\n"):
        txt += line +"  \r\n"
    post.text = markdown(force_text(txt),
                        extras=["fenced-code-blocks", "cuddled-lists", "metadata", "tables", "spoiler",],)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)





