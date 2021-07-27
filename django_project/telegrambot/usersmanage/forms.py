from django import forms
from .models import User, Product, Category, SubCategory


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'balance',
            'count_buy',
            'referral',
            'referral_percent',
            'agreement'
        )
        widgets = {
            'username': forms.TextInput,
            'user_id': forms.TextInput
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'product_this',
            'cost',
            'no_change',
            'description',
            'subcategory',
            'pair_eu',
            'no_limit'
        )
        widgets = {
            'name': forms.TextInput,
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = (
            'name',
            'category',
            'text_mode',
            'parse_type',
            'only_all'
        )
        widgets = {
            'name': forms.TextInput,
        }