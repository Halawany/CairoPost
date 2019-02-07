from django import forms 

from .models import Post

# define form for new post
class AddPost(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title', 'body']