"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from band import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    #path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('about/', views.about, name='about'),
    path('listen/', views.listen, name='listen'),
    path('gallery/', views.gallery, name='gallery'),
    
    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('concert/index/', views.concert_index, name='concert_index'),
    path('concert/list/', views.concert_list, name='concert_list'),
    path('concert/create/', views.concert_create, name='concert_create'),
    path('concert/edit/<int:id>/', views.concert_edit, name='concert_edit'),
    path('concert/delete/<int:id>/', views.concert_delete, name='concert_delete'),
    path('concert/read/<int:id>/', views.concert_read, name='concert_read'),

    path('ticket/index/', views.ticket_index, name='ticket_index'),
    path('ticket/list/', views.ticket_list, name='ticket_list'),
    #path('concert/ticket/', views.ticket_list, name='ticket_list'),
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('ticket/edit/<int:id>/', views.ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:id>/', views.ticket_delete, name='ticket_delete'),
    path('ticket/read/<int:id>/', views.ticket_read, name='ticket_read'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

