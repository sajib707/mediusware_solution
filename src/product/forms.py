from django import forms
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from product.models import Product, Variant, ProductImage, ProductVariantPrice


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'
        widgets = {
            'file_path': TextInput(attrs={'class': 'form-control'}),
            'thumbnail': TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'sku', 'description']

class ProductVariantPriceForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = '__all__'
        widgets = {
            'price': TextInput(attrs={'class': 'form-control'}),
            'stock': TextInput(attrs={'class': 'form-control'}),
        }