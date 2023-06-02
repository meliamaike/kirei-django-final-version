from django import forms
from .models import Service, CategoryService


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].label = "Servicio"
        self.fields["category"].label = "Categoría"
        self.fields["description"].label = "Descripción"
        self.fields["duration"].label = "Duración"
        self.fields["price"].label = "Precio"

    class Meta:
        model = Service
        fields = ("service", "category", "description", "duration", "price")


class CategoryServiceForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_category"].label = "Categoría"

    class Meta:
        model = CategoryService
        fields = []

    def clean_new_category(self):
        new_category = self.cleaned_data.get("new_category")
        existing_category = CategoryService.objects.filter(
            category__iexact=new_category
        ).exists()

        print("existing category: ", existing_category)
        if existing_category:
            print("if existing category: ", existing_category)
            # raise forms.ValidationError('Category already exists.')
        else:
            return new_category

    def save(self, commit=True):
        category_service = super().save(commit=False)
        category_service.category = self.cleaned_data["new_category"]
        if commit:
            category_service.save()
        return category_service


class CategoryServiceEditForm(forms.ModelForm):
    category = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].label = "Categoría"

    class Meta:
        model = CategoryService
        fields = ("category",)
