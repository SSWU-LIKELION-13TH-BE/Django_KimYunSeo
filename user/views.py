from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import SignUpForm, PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from post.models import Post 
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash

User = get_user_model()  # 유저 모델 가져오기

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

def home_view(request):
    return render(request, 'home.html')

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 성공적으로 완료되었습니다!')
            return redirect('login')  # 로그인 페이지로 리디렉션
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# 로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 후 홈 페이지로 이동
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})

    return render(request, 'login.html')

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('login')  # 로그아웃 후 로그인 페이지로 이동

# 비밀번호 찾기 (아이디와 이메일을 입력받고 비밀번호 변경)
def password_reset_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            # 사용자가 입력한 username과 email로 유저 찾기
            user = User.objects.get(username=username, email=email)

            # 비밀번호 유효성 검사를 여기에 추가 가능
            if len(new_password) < 8:
                messages.error(request, '비밀번호는 최소 8자 이상이어야 합니다.')
                return redirect('password_reset')

            # 비밀번호 변경
            user.set_password(new_password)  # 비밀번호 변경
            user.save()

            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('login')  # 로그인 페이지로 리디렉션

        except User.DoesNotExist:
            messages.error(request, '아이디와 이메일이 일치하지 않습니다.')
            return redirect('password_reset')

    return render(request, 'password_reset.html')

@login_required
def mypage_view(request):
    user = request.user
    posts = Post.objects.filter(author=user)

    if request.method == 'POST':
        # 회원 정보 수정
        if 'update_info' in request.POST:
            new_username = request.POST.get('username')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')

            if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
                messages.error(request, '이미 존재하는 아이디입니다.')
            else:
                user.username = new_username
                user.nickname = nickname
                user.email = email
                user.save()
                messages.success(request, '회원 정보가 수정되었습니다.')
                return redirect('mypage')

        # 비밀번호 변경
        elif 'change_password' in request.POST:
            new_pw = request.POST.get('new_password')
            confirm_pw = request.POST.get('confirm_password')

            if new_pw != confirm_pw:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
            elif len(new_pw) < 8:
                messages.error(request, '비밀번호는 8자 이상이어야 합니다.')
            else:
                user.set_password(new_pw)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 변경되었습니다.')
                return redirect('mypage')

    return render(request, 'mypage.html', {'user': user, 'posts': posts})