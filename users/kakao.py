import requests
from django.http import JsonResponse

class KakaoAPI:
    def __init__(self, kakao_token):
        self.kakao_token = kakao_token
        self.user_url    = 'https://kapi.kakao.com/v2/user/me'

    def kakao_user(self):
        headers     = {'Authorization' : f'Bearer {self.kakao_token}'}
        response = requests.get(self.user_url, headers=headers, timeout=3)

        if not response.status_code == 200: 
            return JsonResponse({'message' : 'Invalid token'}, status=401)

        return response.json()
