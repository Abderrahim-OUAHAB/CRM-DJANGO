from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Client
from commande.models import Commande
from commande.filters import CommandeFilter
from .forms import ClientForm
from django.contrib.auth.decorators import login_required
import csv
from reportlab.lib.pagesizes import letter
from django.template.loader import render_to_string
import io
from io import BytesIO
from reportlab.pdfgen import canvas
from client.filters import ClientFilter
# Create your views here.

@login_required(login_url="acces")
def list_client(request,pk):
    client=Client.objects.get(id=pk)
    commande=client.commande_set.all()
    commande_tot=commande.count()
    latest_commande = client.commande_set.order_by('-date_commande').first()
    montant = latest_commande.montant_total if latest_commande else 0
    context={'client':client,'commande':commande,'commande_tot':commande_tot,"montant":montant}
    return render(request,'client/list_client.html',context)

@login_required(login_url="acces")
def page_cli(request):
    client = Client.objects.all()
    MyFilter = ClientFilter(request.GET, queryset=client)
    client = MyFilter.qs
    context = {'clients': client,"MyFilter":MyFilter}
    return render(request,'client/page_cli.html',context)

@login_required(login_url="acces")
def add_client(request):
    form=ClientForm()
    if request.method=="POST":
        form=ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("page_cli")
    context={'form':form}
    return render(request,'client/add_client.html',context)

@login_required(login_url="acces")
def supprimer_client(request,pk):
    client = Client.objects.get(id=pk)
    if request.method == "POST":
        client.delete()
        return redirect("page_cli")
    context={'item':client}
    return render(request,'client/supprimer_client.html',context)

@login_required(login_url="acces")
def update_client(request,pk):
    client=Client.objects.get(id=pk)
    form=ClientForm(instance=client)
    if request.method=="POST":
        form=ClientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            return redirect("page_cli")
    context={'form':form}
    return render(request,'client/add_client.html',context)


def exporter_clients_csv(request):
    # Créer une réponse HTTP de type CSV avec encodage UTF-8
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    response.write('\ufeff'.encode('utf8'))  # Ajouter BOM pour Excel

    # Créer un écrivain CSV
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Écrire les en-têtes de colonnes dans le fichier CSV
    writer.writerow(
        ['ID', 'Nom', 'Prenom', 'Email', 'Telephone', 'Adresse', 'Societe', 'Date d\'ajout', 'Dernier Modification'])

    # Récupérer tous les clients depuis la base de données
    clients = Client.objects.all()

    # Parcourir chaque client et écrire ses données dans le fichier CSV
    for client in clients:
        date_a = client.date_ajout.strftime('%Y/%m/%d')
        date_m = client.dernier_modif.strftime('%Y/%m/%d')
        writer.writerow(
            [client.id, client.nom, client.prenom, client.email, client.telephone, client.addresse, client.societe,
             date_a, date_m])

    # Retourner la réponse HTTP avec le fichier CSV
    return response


def exporter_clients_pdf(request):
    # Créer un buffer en mémoire pour le PDF
    buffer = BytesIO()

    # Créer le PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Liste des Clients")

    # Définir les coordonnées de départ
    y = 750
    x = 50

    # Ajouter le titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(x, y, "Liste des Clients")
    y -= 30  # Déplacement vertical

    # Ajouter les en-têtes des colonnes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "ID")
    p.drawString(x + 50, y, "Nom")
    p.drawString(x + 150, y, "Prénom")
    p.drawString(x + 250, y, "Email")
    p.drawString(x + 450, y, "Téléphone")
    y -= 20

    # Récupérer tous les clients depuis la base de données
    clients = Client.objects.all()

    # Ajouter les données des clients
    p.setFont("Helvetica", 10)
    for client in clients:
        p.drawString(x, y, str(client.id))
        p.drawString(x + 50, y, client.nom)
        p.drawString(x + 150, y, client.prenom)
        p.drawString(x + 250, y, client.email)
        p.drawString(x + 450, y, client.telephone)
        y -= 20
        if y < 50:  # Créer une nouvelle page si nécessaire
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x, y, "ID")
            p.drawString(x + 50, y, "Nom")
            p.drawString(x + 150, y, "Prénom")
            p.drawString(x + 250, y, "Email")
            p.drawString(x + 350, y, "Téléphone")
            y = 730

    # Fermer le PDF
    p.showPage()
    p.save()

    # Revenir au début du buffer
    buffer.seek(0)

    # Créer une réponse HTTP avec le fichier PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clients.pdf"'

    return response

def getFacture_csv(request, pk):
    # Récupérer la commande et le client associé
    client = Client.objects.get(id=pk)
    commande = client.commande_set.all()
    # Assurez-vous que le modèle Commande a un champ client

    # Créer une réponse HTTP de type CSV avec encodage UTF-8
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Facture_client_{client.nom}_{client.prenom}.csv"'
    response.write('\ufeff'.encode('utf8'))  # Ajouter BOM pour Excel

    # Créer un écrivain CSV
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Écrire les en-têtes de colonnes dans le fichier CSV
    writer.writerow(['ID Commande','ID Client', 'Client', 'Produit', 'Quantité', 'Status', 'Date de commande'])

    # Ajouter les données de la commande
    for commande in commande:
          writer.writerow([commande.id, client.id,client, commande.produit, commande.quantite, commande.status, commande.date_commande.strftime('%Y/%m/%d')])

    # Retourner la réponse HTTP avec le fichier CSV
    return response


def getFacture_pdf(request,pk):
    client = Client.objects.get(id=pk)
    commande = client.commande_set.all()
    latest_commande = client.commande_set.order_by('-date_commande').first()
    montant = latest_commande.montant_total if latest_commande else 0
    # Créer un buffer en mémoire pour le PDF
    buffer = BytesIO()

    # Créer le PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("FACTURE")
    p.setFont("Helvetica", 10)
    p.drawString(250,778, f'Client N° {client.id} : {client.nom} {client.prenom}')
    # Définir les coordonnées de départ
    y = 750
    x = 50

    # Ajouter le titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(x, y, "FACTURE")
    y -= 30  # Déplacement vertical

    # Ajouter les en-têtes des colonnes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "ID Commande")
    p.drawString(x + 150, y, "Produit")
    p.drawString(x + 250, y, "Quantité")
    p.drawString(x + 350, y, "Status")
    p.drawString(x + 450, y, "Date commande")
    y -= 20



    # Ajouter les données des commandes
    p.setFont("Helvetica", 10)
    for commande in commande:
        p.drawString(x, y, str(commande.id))
        p.drawString(x + 150, y, str(commande.produit))
        p.drawString(x + 250, y, str(commande.quantite))
        p.drawString(x + 350, y, str(commande.status))
        p.drawString(x + 450, y, commande.date_commande.strftime('%Y/%m/%d'))
        y -= 20
        if y < 50:  # Créer une nouvelle page si nécessaire
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x, y, "ID Commande")
            p.drawString(x + 150, y, "Produit")
            p.drawString(x + 250, y, "Quantité")
            p.drawString(x + 350, y, "Status")
            p.drawString(x + 450, y, "Date de commande")
            y = 730
    p.setFont("Helvetica-Bold", 12)
    p.drawString(480,30 ,f'TOTAL :{montant} DH')
    # Fermer le PDF
    p.showPage()
    p.save()

    # Revenir au début du buffer
    buffer.seek(0)

    # Créer une réponse HTTP avec le fichier PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_N°{client.id}.pdf"'

    return response

def client_dashboard_view(request):
    clients = Client.objects.all()
    client_names = [f"{client.nom} {client.prenom}" for client in clients]
    client_total_amounts = []
    client_order_counts = []

    for client in clients:
        total_amount = sum(commande.montant_total for commande in Commande.objects.filter(client=client))
        order_count = Commande.objects.filter(client=client).count()
        client_total_amounts.append(total_amount)
        client_order_counts.append(order_count)

    context = {
        'client_names': client_names,
        'client_total_amounts': client_total_amounts,
        'client_order_counts': client_order_counts,
    }
    return render(request, 'client/client_dashboard.html', context)