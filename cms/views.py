from django.shortcuts import render, redirect, reverse
from django.views import View
from front.models import UserExtension, Article, Comment
from django.http import HttpResponse
from django.template.loader import render_to_string
from front.forms import ArticleForm


# Create your views here.

class IndexView(View):
    def get(self, request):
        user = UserExtension.objects.get(user_id=request.user_id)
        if user.user.is_staff:
            return render(request, 'cms/index.html', context={'title': '后台管理系统'})
        else:
            return HttpResponse('你好！你不是管理员无法管理后台哦！', status=404)

    def post(self, request):
        manage_type = request.POST.get('manage_type')
        user = UserExtension.objects.get(user_id=request.user_id)
        if not user.user.is_staff:
            return HttpResponse('你好！你不是管理员无法管理后台哦！', status=404)
        context = {}
        if manage_type == 'user':
            context['users'] = UserExtension.objects.all()
            return HttpResponse(render_to_string('cms/user_data.html', context=context))
        elif manage_type == 'article':
            context['articles'] = Article.objects.all()
            return HttpResponse(render_to_string('cms/articles_data.html', context=context))
        elif manage_type == 'comment':
            context['comments'] = Comment.objects.all()
            return HttpResponse(render_to_string('cms/comment_data.html', context=context))
        else:
            return HttpResponse('参数错误！', status=404)


class Manage(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        article_id = request.GET.get('article_id')
        comment_id = request.GET.get('comment_id')
        context = {'forms': ArticleForm(), 'title': '用户管理系统'}
        if user_id:
            context['user_manage'] = UserExtension.objects.get(pk=user_id)
            return render(request, 'cms/user_manage.html', context=context)
        elif article_id:
            context['article_manage'] = Article.objects.get(pk=article_id)
            return render(request, 'cms/article_manage.html', context=context)
        elif comment_id:
            context['comment_manage'] = Comment.objects.get(pk=comment_id)
            return render(request, 'cms/comment_manage.html', context=context)
        else:
            return HttpResponse('参数错误！', status=404)

    def post(self, request):
        manage_type = int(request.POST.get('type', 100))
        if manage_type == 0:
            username = request.POST.get('username')
            pk = request.POST.get('pk')
            email = request.POST.get('email')
            is_super = request.POST.get('is_super')
            is_staff = request.POST.get('is_staff')
            is_active = request.POST.get('is_active')
            user = UserExtension.objects.get(pk=pk)
            user.user.username = username
            user.user.email = email
            user.user.is_super = is_super
            user.user.is_staff = is_staff
            user.user.is_active = is_active
            user.user.save()
            return redirect(reverse('cms:index'))
        elif manage_type == 1:
            pk = request.POST.get('pk')
            title = request.POST.get('title')
            content = request.POST.get('content')
            is_active = request.POST.get('is_active')
            article = Article.objects.get(pk=pk)
            article.title = title
            article.content = content
            article.is_active = is_active
            article.save()
            return redirect(reverse('cms:index'))
        else:
            return HttpResponse('参数错误！', status=404)