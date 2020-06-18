from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save # means, do something before saving model
from django.urls import reverse
from django.utils import timezone

from django.utils.text import slugify

# Create your models here.

class PostManager(models.Manager):
	# def all(self, *args, **kwargs):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='images/', 
		null=True, 
		blank=True,
		width_field='width_field',
		height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager() # objects is the convention/default

	def __str__(self):
		return self.title

	# def __unicode__(self):
	# 	return self.content

	def get_absolute_url(self):
		# return reverse('posts:detail', kwargs={'slug':self.slug})
		return reverse('posts:detail', kwargs={'id':self.id})

	class Meta:
		ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title) # turns title to slug
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = '%s-%s' %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)