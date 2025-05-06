from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.db.models import Q 
from django.db.models import Count
from django.contrib import messages
from .models import Post
from .forms import PostForm


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
    sort = request.GET.get('sort', '')
    q = request.GET.get('q', '')

    if q == "None":
        q = ""

    posts = Post.objects.all()

    # 검색어가 있으면 제목 기준 필터링
    if q:
        posts = posts.filter(title__icontains=q)

    # 정렬 처리
    if sort == 'popular':
        posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'post/post_list.html', {'posts': posts, 'sort': sort, 'q': q})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    session_key = f'viewed_post_{pk}'
    if not request.session.get(session_key, False):
        post.view_count += 1
        post.save()
        request.session[session_key] = True

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


@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시물이 수정되었습니다.')
            return redirect('post_list')  # 수정 후 게시물 목록으로 리디렉션
    else:
        form = PostForm(instance=post)

    return render(request, 'post/post_edit.html', {'form': form, 'post': post})

# 게시물 삭제
@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시물이 삭제되었습니다.')
        return redirect('post_list')  # 삭제 후 게시물 목록으로 리디렉션

    return render(request, 'post/post_confirm_delete.html', {'post': post})