from django import forms
from .models import Category, Genre, Platform

class AddProductForm(forms.Form):
    name = forms.CharField(max_length=200)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    platform = forms.ModelChoiceField(queryset=Platform.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    image = forms.ImageField(required=False)
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price