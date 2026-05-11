from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_safe, require_POST

from .forms import ArticleForm, CommentForm
from .models import Article, Comment


@require_safe
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comment_form = CommentForm()
    # 현재 게시글에 작성된 모든 댓글을 조회 (역참조, 1 ==> N)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@login_required
@require_POST
def delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


# 댓글 작성 view
@login_required
@require_POST
def comments_create(request, article_id):
    # 1. 어떤 게시글에 작성되는 건지 게시글을 먼저 조회
    article = Article.objects.get(pk=article_id)

    # 2. 사용자로부터 입력받은 댓글 내용을 확인
    comment_form = CommentForm(request.POST)

    # 3. 유효성 검사
    if comment_form.is_valid():
        # 우리에게 필요한건 댓글이 실제 db에 저장되기 전에 외래 키 데이터가 채워져야 함
        # 그런데 외래 키 데이터를 넣으려면 댓글 객체가 필요함.
        # 하지만 댓글 객체는 save 이후에 생성됨. 그런데 우리는 save 전에 처리를 해야 함
        # 그래서 django modelform의 save메서드는 우리에게 옵션(commit)을 하나 줌
        # save의 commit옵션을 False로 변경하면
        #  ==> 우리에게 댓글 객체 인스턴스는 제공은 하되, 아직 db에 최종 저장 요청은 하지 않음
        comment = comment_form.save(commit=False)

        # 외래 키 데이터를 준비
        comment.article = article
        comment.user = request.user

        # 4. 저장
        comment.save()
        # 5. 저장 후 detail 페이지로 리다이렉트
        return redirect('articles:detail', article.pk)
    # 6. 유효성 검사가 실패했다면 에러메세지와 함께 상세 페이지를 다시 응답
    context = {
        'comment_form': comment_form,
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


# 댓글 삭제 view
@login_required
@require_POST
def comments_delete(request, article_id, comment_id):
    # 1. 몇번 댓글 지우는지 조회
    comment = Comment.objects.get(pk=comment_id)

    if request.user == comment.user:
        # 2. 조회한 댓글 삭제
        comment.delete()

    # 3. 삭제 후 게시글 상세 페이지로 redirect
    return redirect('articles:detail', article_id)


# 좋아요
def likes(request, article_id):
    # 1. 어떤 게시글에 좋아요를 누르는건지 조회
    article = Article.objects.get(pk=article_id)

    # 2. 좋아요 기능 구현 (다대다 관계 추가/삭제)
    # 2.1 게시글과 유저간 다대다 관계 여부에 따라 좋아요 추가/취소할지 결정
    # 좋아요를 누르는 유저가 해당 게시글의 좋아요를 누른 유저 목록에 이미 포함이 되어있다면? ==> 좋아요 취소(관계 삭제)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        # request.user.like_articles.remove(article)
    # 그런데 좋아요를 누르는 유저가 해당 게시글의 좋아요를 누른 유저 목록에 없다면? ==> 좋아요 등록(관계 추가)
    else:
        article.like_users.add(request.user)
        # request.user.like_articles.remove(article)
    return redirect('articles:index')
        
