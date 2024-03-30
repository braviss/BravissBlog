from django import forms
from blog.models import Article
from tinymce.widgets import TinyMCE


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body', 'image', 'category')
        widgets = {'body': TinyMCE(attrs={'cols': 80, 'rows': 30})}
