from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    # 외래키는 필드 어디에 두어도 실제 테이블에서는 마지막에 위치함
    # 외래키 이름을 상대 클래스 이름으로 지은 이유
    # => 장고는 fk에 자동으로 _id를 붙임
    # 외래키 이름을 단수형으로 지은 이유 => N에서 1을 참조하는 것을 명시하기 위함
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# comment.article = article(게시글 객체 덩어리를 통째로 넣음)  => 권장
# comment.article_id = article.pk(정확하게 객체의 pk타입을 추출해서 넣음)
# => 객체의pk만 넣는다는 말은 다른 어떠한 객체의 pk도 들어갈수 있다는 말=>book.pk도 넣을 수 잇다는 말