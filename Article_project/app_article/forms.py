from django import forms
from .models import ArticleModel


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = "__all__"