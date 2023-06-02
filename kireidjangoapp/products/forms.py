from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):
    image = forms.ImageField(label="Imagen")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nombre"
        self.fields["description"].label = "Descripción"
        self.fields["price"].label = "Precio"
        self.fields["stock"].label = "Stock"
        self.fields["image"].label = "Imagen"
        self.fields["category"].label = "Categoría"

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image", "category"]
