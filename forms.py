from django import forms

class PersonForm(forms.Form):
    title = forms.CharField(label='URL', max_length=300)
