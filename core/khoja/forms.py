from django import forms
from django.contrib.auth.models import User

from .models import Category, Page, UserProfile

#Userform
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

#UserProfile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=100, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text='Please enter the URL of the page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        url = self.cleaned_data.get('url')
        #if url is not empty and doesn't start with 'http://',
        #then prepend 'http'
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            self.cleaned_data['url'] = url
        return self.cleaned_data
        
    class Meta:
        model = Page
        fields = ('title', 'url', 'views')