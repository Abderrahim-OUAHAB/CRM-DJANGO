from django.urls import path
from . import views
urlpatterns = [
    path('Client_<str:pk>/',views.list_client,name='client'),
    path('page_cli/', views.page_cli, name='page_cli'),
    path('add_client/', views.add_client, name='add_client'),
    path('supprimer_client/client_<str:pk>', views.supprimer_client,name='supprimer_client'),
    path('update_client/client_<str:pk>', views.update_client, name='update_client'),
path('exporter-clients-csv/', views.exporter_clients_csv, name='exporter_clients_csv'),
path('exporter_clients_pdf/', views.exporter_clients_pdf, name='exporter_clients_pdf'),
    path('facture/<int:pk>', views.getFacture_csv, name='getFacture_csv'),
    path('eetFacture_pdf/<int:pk>', views.getFacture_pdf, name='getFacture_pdf'),
    path('client_dashboard_view/', views.client_dashboard_view, name='client_dashboard_view'),
]
