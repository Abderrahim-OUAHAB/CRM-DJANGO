import django_filters
from .models import Produit

class ProduitFilter(django_filters.FilterSet):
    class Meta:
        model=Produit
        fields ="__all__"
        exclude=['date_ajout']