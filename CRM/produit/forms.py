from django.forms import ModelForm
from .models import Produit

class ProduitForm(ModelForm):
    class Meta:
        model=Produit
        fields=["designation", "prix", "quantite_stock", "categorie","tag",'image_url']

