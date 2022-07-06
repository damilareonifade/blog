from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .form import UserLoginForm,PwdResetForm,PwdConfirmForm,ChangePassword

app_name = 'accounts'

urlpatterns = [
    path('login',auth_views.LoginView.as_view(template_name='registration/login.html',authentication_form = UserLoginForm),name='login'),
    path('register',views.register,name="register"),
    path('profile',views.profile,name='profile'),
    path("activate/<slug:uidb64>/<slug:token>/",views.activate,name='activate'),
    path('password-reset',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',form_class=PwdResetForm),name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',form_class= PwdConfirmForm),name='password_confirm'),
    path('edit-profile',views.edit_profile,name='edit'),
    path('delete-user',views.delete_user,name="delete_user"),
    path('fav/<int:id>/',views.favourite_add,name='favourite_add'),
    path('favourites/',views.favourite_list,name='favourite_list'),
    path('password-changed/',auth_views.PasswordChangeView.as_view(form_class=ChangePassword,template_name='registration/password_change.html'),name='password_changed'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'),name = 'logout'),
    path('thumbs/',views.thumbs,name ='thumbs'),
    path('like/',views.likes, name='like'),
]
