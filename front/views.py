from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm, LoginForm
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Article, UserExtension, Collect, Comment, Likes, Image
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
import os
from .forms import ArticleForm, CommentForm


# Create your views here.
class IndexView(View):
    def get(self, request):
        articles = Article.objects.all()
        is_staff = False
        if request.user:
            is_staff = request.user.is_staff
        return render(request, 'front/index.html', {'title': '主页', 'username': request.username, 'articles': articles,
                                                    'is_staff': is_staff})


class ArticleView(View):
    def get(self, request):
        article_id = request.GET.get('article')
        try:
            article = Article.objects.get(pk=article_id)
            if not article.is_active:
                collect_exist = 'active-style' if bool(
                    Collect.objects.filter(article=article, collect_user_id=request.user_id)) else ''
                likes_exist = 'active-style' if bool(
                    Likes.objects.filter(article=article, likes_user_id=request.user_id)) else ''
                Article.objects.filter(pk=request.GET.get('article')).update(view_times=F('view_times') + 1)
                comments = Comment.objects.filter(article_id=article.pk)
                return render(request, 'front/article-details.html',
                              {'title': article.title,
                               'username': request.username,
                               'user': request.user,
                               'article': article,
                               'collect': collect_exist,
                               'likes': likes_exist,
                               'comments': comments,
                               'comment_form': CommentForm()})
            else:
                return HttpResponse('文章不见了！！！！！！', status=404)
        except:
            return HttpResponse('文章不见了！！！！！！', status=404)



class RegisterView(View):
    def post(self, request):
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.objects.filter(email=email).exists():
                return HttpResponse(json.dumps({'email': ['邮箱已经被注册了']}), status=404)
            try:
                User.objects.create_user(username=username, email=email, password=password)
                return HttpResponse("OK")
            except Exception:
                return HttpResponse(json.dumps({'username': ['账号已经被注册了']}), status=404)
        else:
            return HttpResponse(json.dumps(forms.get_errors()), status=404)


class LoginView(View):
    def post(self, request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email=email)
            if not user.is_active:
                error_info = {'email': ['你的账号已经被封禁！']}
                return JsonResponse(error_info, status=404)
            if not user:
                error_info = {'email': ['邮箱或密码错误']}
                return JsonResponse(error_info, status=404)
            exist = authenticate(username=user.username, password=password)
            if not exist:
                error_info = {'email': ['邮箱或密码错误']}
                return JsonResponse(error_info, status=404)
            else:
                request.session['user_id'] = user.id
                return HttpResponse("OK")
        else:
            return JsonResponse(forms.get_errors(), status=404)


class PostingView(View):
    def get(self, request):
        if request.username:
            return render(request, 'front/posting.html',
                          {'title': '%s正在写贴中' % request.username,
                           'username': request.username,
                           'ueditor': ArticleForm()})
        else:
            return HttpResponse('error', status=404)

    def post(self, request):
        article_content = request.POST.get('content')
        article_title = request.POST.get('article_title')
        share_url = request.POST.get('share_url')
        if len(article_title) < 6:
            return JsonResponse({'error': '标题长度不能小于6'}, status=404)
        if len(article_content) < 20:
            return JsonResponse({'error': '请勿水贴，多写点东西吧'}, status=404)
        user_id = request.session.get('user_id')
        user = User.objects.filter(id=user_id).first()
        tags = '<a href="%s"><span class="badge">转载</span></a>' % share_url if share_url else '<span class="badge">原创</span>'
        try:
            article = Article.objects.create(content=article_content, title=article_title, auth_id=user.id, tags=tags)
            # return redirect(reverse('front:article') + "?article=%s" % article.pk)
            return JsonResponse({'success': '发布成功', 'id': article.pk})
        except Exception as e:
            if "UNIQUE" in str(e):
                return JsonResponse({'error': '标题重复了，亲！'}, status=404)
            else:
                return JsonResponse({'error': '你还有登录怎么可以发帖呢？'}, status=404)


class LoginOutView(View):
    def get(self, request):
        request.session.flush()
        return redirect(reverse('front:index'))


class UserManageView(View):
    def get(self, request):
        articles = Article.objects.filter(auth_id=request.user_id)
        return render(request, 'front/user-manage.html',
                      {'title': '%s的管理中心' % request.username,
                       'username': request.username,
                       'user': request.user,
                       'articles': articles})


@method_decorator(csrf_exempt, name='dispatch')
class CkImageUploadView(View):
    def post(self, request, *args, **kwargs):
        error_info = {'error': {'message': ''}}
        head_img_photo = request.FILES.get('photo')
        head_img_upload = request.FILES.get('upload')
        head_img = head_img_photo if head_img_photo else head_img_upload
        if 1024 * 1024 * 10 < head_img.size:
            error_info['uploaded'] = False
            error_info['error']['message'] = '图片大小不能超过10m'
            return JsonResponse(error_info, status=404)
        img_types = ['image/gif', "image/png", 'image/jpeg']
        if head_img.content_type not in img_types:
            error_info['uploaded'] = False
            error_info['error']['message'] = '图片格式支持 jpeg/png/gif'
            return JsonResponse(error_info, status=404)
        filename_, type_ = os.path.splitext(head_img.name)
        head_img.name = '%s%s' % (time.time(), type_)
        if head_img_photo:
            user = UserExtension.objects.get(user_id=request.user_id)
            user.head_img = head_img
            user.save()
            error_info['uploaded'] = True
            error_info['url'] = user.head_img.url
            return JsonResponse(error_info)
        else:
            img = Image(img=head_img)
            img.img = head_img
            img.save()
            error_info['uploaded'] = True
            error_info['url'] = img.img.url
            return JsonResponse(error_info)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CollectView(View):
    def post(self, request):
        if not request.user_id:
            return JsonResponse({'error': '请先登录再收藏'}, status=404)
        collect_id = request.POST.get('collect_id')
        try:
            article = Article.objects.get(id=collect_id)
        except Exception as e:
            print(e)
            return JsonResponse({'error': '文章不存在无法收藏'}, status=404)
        if article.auth.user == request.user:
            return JsonResponse({'error': '不可收藏自己的文章'}, status=404)
        exist = Collect.objects.filter(article=article, collect_user_id=request.user_id)
        if exist:
            exist.delete()
            return JsonResponse({'success': '取消收藏成功', 'status': 0})
        else:
            Collect(article=article, collect_user_id=request.user_id).save()
            return JsonResponse({'success': '恭喜你收藏成功', 'status': 1})


from django.db.utils import IntegrityError


class SetView(View):
    def post(self, request):
        re_username = request.POST.get('re_username')
        if re_username:
            print(re_username)
            user = User.objects.get(id=request.user_id)
            user.username = re_username
            try:
                user.save()
            except IntegrityError:
                return JsonResponse({'error': '这个名字已经被别人注册了，你不能注册了哦'}, status=404)
            return JsonResponse({'success': '修改成功'})
        else:
            return JsonResponse({'error': '参数错误'}, status=404)


class CommentView(View):
    def post(self, request):
        try:
            comment_id = request.POST.get('comment_id')
            comment_count = request.POST.get('comment_count')
            if len(comment_count) < 15:
                return JsonResponse({'error': '评论过短（必须长于15个字符）'}, status=404)
            Comment(article_id=comment_id, comment_content=comment_count, comment_user_id=request.user_id).save()
            return JsonResponse({'success': '评论成功'})
        except:
            return JsonResponse({'error': '请先登录，无法评论'}, status=404)


class LikeView(View):
    def post(self, request):
        try:
            like_id = request.POST.get('like_id')
            exist = Likes.objects.filter(article_id=like_id, likes_user_id=request.user_id)
            if not exist:
                Likes.objects.create(article_id=like_id, likes_user_id=request.user_id)
                return JsonResponse({'success': '点赞成功'})
            else:
                exist.delete()
                return JsonResponse({'success': '取消成功'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': '请先登录，无法点赞'}, status=404)
