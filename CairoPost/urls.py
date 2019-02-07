from django.urls import path

from . import views

urlpatterns = [
	path('', views.index_article, name='index'),
	path('article/<pk>', views.article_details, name='article_details'),
	path('articles', views.article, name="articles"),
	path('addarticle', views.new_article, name='new_article'),
	path('article/<pk>/editarticle', views.article_edit, name='article_edit'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('search', views.search, name='search'),
]