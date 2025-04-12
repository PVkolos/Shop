from django import forms
from .models import Products, Categories
from .views import get_categories_from_admin


class ProductsAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductsAdminForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = get_categories_from_admin()

    class Meta:
        model = Products
        fields = '__all__'

    category = forms.MultipleChoiceField(
        choices=(),
        widget=forms.SelectMultiple,
        required=False
    )

    def clean_category(self):
        categories = self.cleaned_data.get('category')
        if isinstance(categories, list):
            return '-=-'.join(categories)
        return categories

    def clean(self):
        cleaned_data = super().clean()
        # Удаляем валидацию для поля category
        if 'category' in cleaned_data:
            cleaned_data['category'] = self.clean_category()
        return cleaned_data


