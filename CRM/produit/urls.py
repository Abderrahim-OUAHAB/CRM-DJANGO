from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('page_prod',views.page_prod,name='page_prod'),
    path('add_produit/', views.add_produit, name='add_produit'),
    path('update_produit/produit_<str:pk>', views.update_produit, name='update_produit'),
    path('supprimer_produit/produit_<str:pk>', views.supprimer_produit, name='supprimer_produit'),
    path('exporter-produits-csv/', views.exporter_produits_csv, name='exporter_produits_csv'),
    path('exporter_produits_pdf/', views.exporter_produits_pdf, name='exporter_produits_pdf'),
    path('dash_prod/', views.dash_prod, name='dash_prod'),

]
