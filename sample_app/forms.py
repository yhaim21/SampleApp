from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=80)
    file = forms.FileField()