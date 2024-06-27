from django import forms
from .models import query,comment

class PostForm(forms.ModelForm):
    class Meta:
        model = query
        fields = ('name','body')

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control','margin':'10px'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'})
        }
