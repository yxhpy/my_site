from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name = "front"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/', views.ArticleView.as_view(), name='article'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('posting/', views.PostingView.as_view(), name='posting'),
    path('loginOut/', views.LoginOutView.as_view(), name='loginOut'),
    path('userManage/', views.UserManageView.as_view(), name='userManage'),
    path('uplaodImage/', views.CkImageUploadView.as_view(), name='uplaodImage'),
    path('collect/', views.CollectView.as_view(), name='collect'),
    path('set/', views.SetView.as_view(), name='set'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('like/', views.LikeView.as_view(), name='like'),
]