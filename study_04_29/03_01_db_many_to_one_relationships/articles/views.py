from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ArticleForm, CommentForm
from .models import Article, Comment


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comment_form = CommentForm()
    # 현재 게시글에 작성된 모든 댓글을 조회(역참조, 1=> N)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    return redirect('articles:index')


@login_required
def update(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


# 댓글 작성  view

def comments_create(request, article_id):
    # 1. 어떤 게시글에 작성되는 건지 게시글을 먼저 조회
    article = Article.projects.get(pk=article_id)

    # 2. 사용자로부터 입력받은 댓글 내용을 확인
    comments_form = CommentForm(request.POST)

    # 3. 유효성 검사
    if comments_form.is_valid():
        # + 우리에게 필요한 건 댓글이 실제 db에 저장되기 전에 외래키 데이터가 채워져야 함
        #   그런데 외래키 데이터를 넣으려면 댓글 객체가 필요함
        #   하지만 댓글 객체는
        #   그래서 django modelfom save 매서드는 우리에게 옵셥(commit)을 하나 줌
        # save의 commit 옵션을 false로 변경하면
        # => 우리에게 댓글 객체 인스턴스는 제공은 하되, 아직 db에 최종 저장 요청은 하지 않음
        comment = comments_form.save(commit=False)

        #외래키 데이터 준비
        comment.article = article
    # 4. 저장
        comments_form.save()
        # 5. 저장 후 detail 페이지로 리다이렉트
        return redirect('articles:detail', article.pk)
    
    #6. 유효성검사가 실패했다면 에러메세지와 함쎄 상세 페이지를 다시 리다이렉트
    context = {
        'comments_form' : comments_form,
        'article': article
    }
    return render(request, 'artcles/detail.html', context)


# 댓글 삭제
def comments_delete(request, article_id, comment_id):
    # 1. 몇번 댓글 지우는지 조회
    comment = Comment.objects.get(pk=comment_id)

    article_id = comment.article.pk

    # 2. 조회한 댓글 삭제
    comment.delete()

    # 3. 삭제 후 게시글 상세 페이지로 이동 redirect
    return redirect('articles:detail', article_id)