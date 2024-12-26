from django import forms


class PubDatasetForm(forms.Form):
    name = forms.CharField(max_length=200, min_length=2)
    content = forms.CharField(min_length=2)
    category = forms.IntegerField()
    file = forms.FileField(required=True)
