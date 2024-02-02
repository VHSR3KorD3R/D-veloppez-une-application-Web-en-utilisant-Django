"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import LITRevu.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('home/', LITRevu.views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path("create_ticket/", LITRevu.views.ticket_form, name="ticket_form"),
    path('ticket/<int:ticket_id>/edit', LITRevu.views.edit_ticket, name='edit_ticket'),
    path('create_review/', LITRevu.views.review_form, name="review_form"),
    path('review/<int:review_id>/edit', LITRevu.views.edit_review, name='edit_review'),
    path('posts/', LITRevu.views.all_posts, name='posts'),
    path('subscribe/', LITRevu.views.subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>', LITRevu.views.unsubscribe, name='unsubscribe'),
    path('create_review_with_ticket/<int:ticket_id>/edit', LITRevu.views.create_review_with_ticket, name='create_review_with_ticket'),
    path('delete_review/<int:review_id>/delete', LITRevu.views.delete_review, name='delete_review'),
    path('delete_ticket/<int:ticket_id>/delete', LITRevu.views.delete_ticket, name='delete_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
