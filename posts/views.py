# from urllib import quote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def index(request):
	context = {'title': 'Index'}
	return HttpResponse('<h1>Welcome to home page!</h1><br><p>goto /posts to see list of posts</p>')


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404 # so only staff or admin can add post

	# if not request.user.is_authenticated:
	# 	raise Http404 # so only staff or admin can add post
		# both does the same thing


	form = PostForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {'form': form,}
	return render(request, 'post_form.html', context)


def post_detail(request, id):
	# instance = Post.objects.get(id=10)
	instance = get_object_or_404(Post, id=id)
	# share_string = quote_plus(instance.content)

	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	context = {
		'title': instance.title, 
		'instance':instance}
	return render(request, 'post_detail.html', context)


def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.filter(draft=False).filter(publish__lte=timezone.now()) #.all().order_by("-timestamp")

	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
		).distinct()

	paginator = Paginator(queryset_list, 10) # show 25 contacts per page

	page_request_var = 'my-page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		# if page is out of range (e.g 999), deliver last page of result
		queryset = paginator.page(paginator.num_pages)
	context = {
		'object_list':queryset, 
		'title': 'List',
		'page_request_var':page_request_var,
		'today': today,
	}
	return render(request, 'post_list.html', context)



def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Updated!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'title': instance.title, 
		'instance': instance,
		'form': form,
	}
	return render(request, 'post_form.html', context)


def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('posts:list')