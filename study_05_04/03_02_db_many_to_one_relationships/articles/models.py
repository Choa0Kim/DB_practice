from django.db import models
from accounts.models import User
from django.conf import settings


# Create your models here.
class Article(models.Model):
    # 여기서 User 클래스를 직접 작성하지 않는다.
    #  왜냐? Article 클래스가 실행될 때 User 클래스가 존재하지 않을수도 있기 때문에
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Use모델의 pk를  fk로
    #'accounts.User' 라는 문자열만 들고 있다가, 나중에 모든 모델이
    # 다 로드된 이후에 진짜 User 클래스를 찾아서 연결
    # ==> "지연 평가" 
    # 지연 평가는 ORM에서도 쓰임. Article.objects.all() 자체는 DB에 요청을 보내지 않음
    # 언제 요청을 보내냐면, list() 형변환 하거나 for로 반복하거나, 이렇게 실제 데이터를 활용할 때 평가 진행 
    # => 효율 최적화를 위해
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # settings.AUTH_USER_MODEL: settings.py 에 정의된 AUTH_USER_MODEL 설정 값을 가져옴
    # 반환값: 'accounts.User'(문자열)
    # models.py에서 User 모델을 참조할 때 사용
    # get_user_model(): ettings.py 에 정의되어 활성화된 User 모델을 가져옴
    # 반환값: 'User object'(객체)
    # models.py를 제외한 다른 모든 위치에서 사용. ex)forms.py
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    # 외래 키는 필드 어디에 두어도 실제 테이블에서는 마지막에 위치함
    # 외래 키 이름을 이렇게 상대방 클래스 이름으로 지은 이유
    # django가 최종적으로 설계도를 만들때 외래 키 필드 이름에 _id를 자동으로 붙이기 때문
    # 외래 키 이름을 단수형으로 지은 이유는
    #   N에서 1을 참조하는 것을 명시하기 위함.
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


