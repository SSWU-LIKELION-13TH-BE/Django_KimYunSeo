from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import GuestbookEntry
from django.contrib.auth import get_user_model

User = get_user_model()

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        if request.user.is_authenticated and request.user != profile_user:
            content = request.POST.get('content')
            if content:
                GuestbookEntry.objects.create(owner=profile_user, author=request.user, content=content)
                return redirect('profile_view', username=profile_user.username)

    return render(request, 'user_profile/profile.html', {'profile_user': profile_user})

@login_required
def my_guestbook_view(request):
    guestbook_entries = GuestbookEntry.objects.filter(owner=request.user)
    return render(request, 'user_profile/my_guestbook.html', {
        'guestbook_entries': guestbook_entries,
    })
