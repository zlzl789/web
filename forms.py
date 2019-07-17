from django import forms

class PersonForm(forms.Form):
    title = forms.CharField(label='URL', max_length=300)

class Key(forms.Form):
    keyword = forms.CharField(label='키워드', max_length=300)

class Key1(forms.Form):
    keyword1 = forms.CharField(label='키워드', max_length=300)