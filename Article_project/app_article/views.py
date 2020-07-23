from django.contrib.auth import authenticate,login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import TemplateView
# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, TemplateView

from django import http
from .models import Token,ArticleModel
from .sendingemail import send_mail
from .forms import ArticleModelForm

class IndexView(TemplateView):
    template_name = 'register.html'


class RegisterView(View):
    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        queryset=User.objects.filter(Q(username=username)|Q(first_name=first_name))
        if queryset:
            for i in queryset:
                if i.username==username:
                    return render(request, 'register.html',{'message' : 'invalid username'})
                if i.first_name==first_name:
                    return render(request, 'register.html', {'message' : 'invalid first_name'})
        else:
            password = request.POST.get('password')
            if password:
                user = User.objects.create(first_name=first_name, last_name=last_name,username=username, email=email)
                user.set_password(password)
                user.save()
                return render(request, 'register.html',{'message':'Successfully registered'})
            else:
                return render(request, 'register.html',{'message':'Please enter the password'})


class LoginView(TemplateView):
    template_name = 'login.html'


class LoginUser(View):
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            try:
                user_object = User.objects.get(username=username)
                if user_object:
                    authenticated = authenticate(request, username=username, password=password)
                    if authenticated is not None:
                        login(request, authenticated)
                        return redirect('/article_create/')
                    else:
                        message = 'invalid password'
                        return render(request, "login.html", {'message': message})
            except ObjectDoesNotExist:
                error = "Given Username does not match"
                return render(request, 'login.html', {'message1': error})
        else:
            message2 = "must enter username and password in the fields"
            return render(request, 'login.html', {'message2': message2})


class PasswordResetForm(TemplateView):
    template_name = 'password_reset_form.html'


class PasswordReset(View):
    model = Token

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        queryset = User.objects.filter(email=email)
        if queryset is not None:
            token = Token.objects.create(user=request.user)
            message1 = 'Subject: {}\n\n{}'.format("Reset Password Link",
                                                  'http://127.0.0.1:8000/password_reset/')
            message = message1 + str(token.token)
            send_mail(message)
            m1 = "password reset link sent to your email id please check inbox else spam in your email"
            return render(request, 'password_reset_form.html', {"data": m1})
        else:
            m2 = "please enter valid email"
            return redirect('/thanks/', {"data1": m2})

class Reset(TemplateView):
    template_name = 'password_reset_email.html'


class Password_Reset_Done(View):
    model = Token

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        token = request.GET.get('token')
        print(token)

        if password1 == password2:
            user =User.objects.get(username = request.user)
            user.set_password(password1)
            user.save()
            print(request.user)
            token = Token.objects.create(user = request.user,is_expired = True)
            token.save()
            return render(request, 'password_reset_complete.html')
        else:
            # user = User.objects.get(username=request.user)
            return redirect('password_reset_email.html',{'name':username})


class ProfileView(TemplateView):
    template_name = 'profile_view.html'

class ProfileEditView(View):

    def post(self,request, *args, **kwargs):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user=User.objects.filter(email=email)
            # username=""
            # first_name=""
            # last_name=""
            if user:
                for x in user:
                    username=x.username
                    first_name=x.first_name
                    last_name=x.last_name

          #  print(username,first_name,last_name)

        #     username = request.POST.get("username")
        #     email = request.POST.get("email")
        #     first_name = request.POST.get('first_name')
        #     last_name = request.POST.get('last_name')
        # res = User.objects.get(username=username)
        # if email == res.email:
        #     User(first_name=first_name, last_name=last_name, email=email, username=username,).save()
        #     message = "profile updated sucessfully"
        return render(request, 'profile_edit.html',{'username':username,'first_name':first_name,'last_name':last_name} )

class UpdateProfile(View):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        print(first_name,last_name,username)
        data=User.objects.filter(username=username).update(first_name=first_name,last_name=last_name)

        return render(request, 'profile_edit.html',{'message':'successfully updated'})

