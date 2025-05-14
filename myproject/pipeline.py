from django.contrib.auth import get_user_model

User = get_user_model()

def create_custom_user(strategy, details, backend, user=None, *args, **kwargs):
    print("==== SOCIAL LOGIN DETAILS ====")
    print("backend:", backend.name)
    print("details:", details)
    print("kwargs:", kwargs)

    if user:
        return {'user': user}

    email = details.get('email')
    nickname = details.get('nickname') or '소셜사용자'

    if backend.name == 'naver':
        nickname = details.get('nickname') or '네이버사용자'
    elif backend.name == 'kakao':
        nickname = details.get('nickname') or '카카오사용자'

    user_id = kwargs.get('uid') or email or strategy.session_get('user_id_fallback')

    if not user_id:
        raise ValueError('소셜 로그인에 필요한 사용자 ID가 누락되었습니다.')

    # username을 설정 (예: 닉네임을 사용)
    username = nickname

    # 사용자 생성
    try:
        user = User.objects.create_user(
            username=username,
            email=email or '',
            password=None,  # 소셜 로그인에서는 비밀번호를 설정하지 않음
        )
        print(f"User created: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")
        raise e

    return {'user': user}

