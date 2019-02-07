from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse

from django.contrib.postgres.search import SearchVector
from .models import Post
from django.contrib.auth.models import User
from .forms import AddPost

# getting article details for my index
def index_article(request):
	post = Post.objects.get(id=1)
	return render(request, 'CairoPost/index.html', {'post': post})

# post all articles in one page
def article(request):
	article = Post.objects.all()
	return render(request, 'CairoPost/articles.html', {'article': article})


# redirect reader to the full post page
def article_details(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'CairoPost/details.html', {'post': post})

# add new article view
def new_article(request):
	if request.method == 'POST':
		form = AddPost(request.POST)
		if form.is_valid():
			# commit = False to prevent the save of form without the athor and publish date
			post = form.save(commit=False)
			post.author = request.user
			post.pub_date = timezone.now()
			post.save()
			return redirect('article_details', pk=post.pk)
	else:
		form = AddPost()
	return render(request, 'CairoPost/new.html', {'form': form})

def article_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = AddPost(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			author = request.user
			pub_date = timezone.now()
			form.save()
			return redirect('article_details', pk=post.pk)
	else:
		form = AddPost(instance=post)
	return render(request, 'CairoPost/edit.html', {'form': form})

# user login
def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("index")
		else:
			return render(request, 'CairoPost/login.html', {'message': 'invalid username or password'})
	else:
		return render(request, 'CairoPost/login.html')


# user logout
def logout_view(request):
	logout(request)
	return redirect('login')

# register new user
def register(request):
	if request.method == 'POST':
		email = request.POST["email"]
		username = request.POST["username"]
		password = request.POST["password"]
		user = User.objects.create_user(username, email, password)
		user.save()
		return redirect('login')
	else:
		return render(request, 'CairoPost/register.html')

# search inside blog
def search(request):
	if request.method == "POST":
		userinput = request.POST['userinput']
		results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=userinput)
		return render(request, 'CairoPost/search.html', {'results': results})
	else:
		return redirect('index')