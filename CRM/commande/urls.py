from django.urls import path
from . import views
urlpatterns = [
    path('',views.list_commande,name='list_commande'),
    path('add_commande/', views.add_commande,name='add_commande'),
    path('update_commande/commande_<str:pk>', views.update_commande, name='update_commande'),
    path('supprimer_commande/commande_<str:pk>', views.supprimer_commande,name='supprimer_commande'),
    path('exporter_commandes_csv/', views.exporter_commandes_csv, name='exporter_commandes_csv'),
    path('exporter_commandes_pdf/', views.exporter_commandes_pdf, name='exporter_commandes_pdf'),
    path('commande_dashboard_view/', views.commande_dashboard_view, name='commande_dashboard_view'),
]
