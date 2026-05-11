from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 팔로우 기능을 위한 MTM 필드를 정의
    # symmetrical=False: 맞 팔로우관계가 아닐수도 있음 설정
    # related_name='followers': 
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)






    # def __str__(self):
    #     return self.username
