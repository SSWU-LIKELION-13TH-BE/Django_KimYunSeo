from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')  
        tech_stack = request.POST.get('tech_stack')
        github_link = request.POST.get('github_link')

        Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            image=image,
            tech_stack=tech_stack,
            github_link=github_link
        )
        return redirect('post_list')
    
    return render(request, 'post/post_create.html')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent=None)
    return render(request, 'post/post_detail.html', {
        'post': post,
        'comments': comments
    })

def add_comment(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        content = request.POST['content']
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(pk=parent_id) if parent_id else None
        Comment.objects.create(post=post, user=request.user, content=content, parent=parent_comment)
        return redirect('post_detail', pk=pk)
    
@login_required
def toggle_post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


@login_required
def toggle_comment_like(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})
