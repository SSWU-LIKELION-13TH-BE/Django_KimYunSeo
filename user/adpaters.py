# filepath: c:\Users\Administrator\Django_KimYunSeo\user\adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # 필수 필드 채우기
        user.phone_number = data.get('phone_number', '')  # 기본값 설정
        return user