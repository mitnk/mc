from django import forms
from mitnkcom.public.models import Article, Tag
from django.contrib.admin.widgets import FilteredSelectMultiple

class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
            widget=FilteredSelectMultiple("Tags",False,attrs={'rows':'6'}))

    class Meta:
        model = Article
