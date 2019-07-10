from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Post
from .forms import PostForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def post_list(request):
	username = None
	if request.user.is_authenticated:
		user= request.user.id
		posts = Post.objects.filter(author=user).order_by('-created_date')
		return render(request, 'blog/post_list.html', {'posts': posts})
	else:
		return render(request, 'blog/post_list.html', {'posts': None})

def post_detail(request, pk):
	if request.user.is_authenticated:
		user_posts = Post.objects.filter(author=request.user.id)
		post = get_object_or_404(user_posts, pk=pk)
		return render(request, 'blog/post_detail.html', {'post': post})
	else:
		return render(request, 'blog/post_detail.html', {'post': None})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def send_email(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			subject = form.cleaned_data['title']
			to_email = user.cleaned_data['email']
			message = form.cleaned_data['text']
			try:
				send_mail(subject, message, ['admin@example.com'], to_email)
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('emailsuccess')
	return render(request, 'socialmedia/send_email.html', {'post': post})

def emailsuccessView(request):
	return HttpResponse('¡Éxito! Mensaje enviado.')