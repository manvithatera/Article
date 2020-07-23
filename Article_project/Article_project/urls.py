"""Article_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app_article import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('article_list/', views.ArticleList.as_view()),
    path('article_preview/<int:pk>/', views.ArticlePreView.as_view(), name ='article_preview'),
    path('article_create/', views.ArticleCreateView.as_view(), name='article_create'),

    path('author_filter_list/', views.AuthorFilter),

    path('article/update/<int:pk>/', views.ArticleUpdate.as_view(),name='article_update'),
    path('article/delete/<int:pk>/', views.ArticleDelete.as_view(),name='article_delete'),


    path('/', views.IndexView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login_view/', views.LoginView.as_view(), name='login_view'),
    path('login_post_view/', views.LoginUser.as_view(), name='login_post_view'),
    path('password_reset_form/', views.PasswordResetForm.as_view(), name='password_reset_form'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/<uuid:token>/',views.Reset.as_view(), name ='password_reset/<uuid:token>/'),
    path('password_reset/done/', views.Password_Reset_Done.as_view(), name = 'password_reset/done/'),

    path('profile_view/', views.ProfileView.as_view(), name='profile_view'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('update_profile/', views.UpdateProfile.as_view(), name='update_profile'),

    path('dashboard/', views.Dashboard.as_view(), name ='dashboard'),

]
