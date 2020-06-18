from django.urls import path
from posts.views import *

app_name = 'posts'

urlpatterns = [
	path('', post_list, name='list'),
	path('create/', post_create, name='create'),
	path('<int:id>/', post_detail, name='detail'),
	path('<int:id>/edit/', post_update, name='update'),
	path('<int:id>/delete/', post_delete, name='delete'),
]