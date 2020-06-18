from django.contrib import admin
from posts.models import Post

# Register your models here.

# specifically t cusomize the "admin" through frontend
class PostModelAdmin(admin.ModelAdmin):
	
	list_display = ['title', 'updated', 'timestamp']
	list_display_links = ['updated']
	list_filter = ['title', 'updated', 'timestamp']
	search_fields = ['title', 'content']
	list_editable = ['title']
	class Meta:
		model = Post


# register model to admin
admin.site.register(Post, PostModelAdmin)