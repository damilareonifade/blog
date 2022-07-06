from this import d
from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField
from .models import Category


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})

        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('post','parent', 'content')
        widget = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
    

class PostSearchForm(forms.Form):
    q = forms.CharField(label='Search Text')
    c = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'))

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = ''
        self.fields['q'].label = 'Search For'
        self.fields['c'].required = False
        self.fields['q'].widget.attrs.update(
            {'class':'form-control','data-toggle':'dropdown'}
        )
        