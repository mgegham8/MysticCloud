from django import forms
from menu.models import MenuItem, BarItem, Category, BarCategory

class MenuItemForm(forms.ModelForm):
    """
    Form for creating and updating food menu items.
    """
    class Meta:
        model = MenuItem
        fields = ("name", "price", "description", "image", "category")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class BarItemForm(forms.ModelForm):
    """
    Form for creating and updating bar menu items.
    """
    class Meta:
        model = BarItem
        fields = ("name", "price", "description", "image", "category")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """
    Form for creating food categories.
    """
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BarCategoryForm(forms.ModelForm):
    """
    Form for creating bar categories.
    """
    class Meta:
        model = BarCategory
        fields = ("name", "category")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }