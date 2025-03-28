from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CommandeForm
from .models import Commande,Client,Produit
from django.contrib.auth.decorators import login_required
from commande.filters import CommandeFilter
import csv
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Commande
from django.core.exceptions import ValidationError
from django.contrib import messages
# Create your views here.

@login_required(login_url="acces")
def list_commande(request):
    commandes = Commande.objects.all()
    MyFilter = CommandeFilter(request.GET, queryset=commandes)
    commandes = MyFilter.qs
    context = {'commandes': commandes,'MyFilter':MyFilter}
    return render(request,'commande/list_commande.html',context)

# Create your views here.
@login_required(login_url="acces")
def add_commande(request):
    form = CommandeForm()
    if request.method == "POST":
        form = CommandeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Commande ajoutée avec succès.")
                return redirect("list_commande")
            except ValidationError as e:
                messages.error(request, e.message)
    context = {'form': form}
    return render(request, 'commande/add_commande.html', context)
# Create your views here.
@login_required(login_url="acces")
def update_commande(request,pk):
    commande=Commande.objects.get(id=pk)
    form=CommandeForm(instance=commande)
    if request.method=="POST":
        form=CommandeForm(request.POST,instance=commande)
        if form.is_valid():
            form.save()
            return redirect("list_commande")
    context={'form':form}
    return render(request,'commande/add_commande.html',context)
# Create your views here.
@login_required(login_url="acces")
def supprimer_commande(request,pk):
    commande = Commande.objects.get(id=pk)
    if request.method == "POST":
        commande.delete()
        return redirect("list_commande")
    context={'item':commande}
    return render(request,'commande/supprimer_commande.html',context)

def exporter_commandes_csv(request):
    # Créer une réponse HTTP de type CSV avec encodage UTF-8
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="commandes.csv"'
    response.write('\ufeff'.encode('utf8'))  # Ajouter BOM pour Excel

    # Créer un écrivain CSV
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Écrire les en-têtes de colonnes dans le fichier CSV
    writer.writerow(
        ['ID', 'Client', 'Produit', 'Quantité','Status', 'Date de commande'])

    # Récupérer tous les clients depuis la base de données
    commandes = Commande.objects.all()

    # Parcourir chaque client et écrire ses données dans le fichier CSV
    for commande in commandes:
        date_a = commande.date_commande.strftime('%Y/%m/%d')
        writer.writerow(
            [commande.id, commande.client, commande.produit, commande.quantite, commande.status, date_a])

    # Retourner la réponse HTTP avec le fichier CSV
    return response




def exporter_commandes_pdf(request):
    # Créer un buffer en mémoire pour le PDF
    buffer = BytesIO()

    # Créer le PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Liste des Commandes")

    # Définir les coordonnées de départ
    y = 750
    x = 50

    # Ajouter le titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(x, y, "Liste des Commandes")
    y -= 30  # Déplacement vertical

    # Ajouter les en-têtes des colonnes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "ID")
    p.drawString(x + 50, y, "Client")
    p.drawString(x + 180, y, "Produit")
    p.drawString(x + 250, y, "Quantité")
    p.drawString(x + 350, y, "Status")
    p.drawString(x + 450, y, "Date")
    y -= 20

    # Récupérer toutes les commandes depuis la base de données
    commandes = Commande.objects.all()

    # Ajouter les données des commandes
    p.setFont("Helvetica", 10)
    for commande in commandes:
        p.drawString(x, y, str(commande.id))
        p.drawString(x + 50, y, str(commande.client))
        p.drawString(x + 180, y, str(commande.produit))
        p.drawString(x + 250, y, str(commande.quantite))
        p.drawString(x + 350, y, str(commande.status))
        p.drawString(x + 450, y, commande.date_commande.strftime('%Y/%m/%d'))
        y -= 20
        if y < 50:  # Créer une nouvelle page si nécessaire
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x, y, "ID")
            p.drawString(x + 50, y, "Client")
            p.drawString(x + 180, y, "Produit")
            p.drawString(x + 250, y, "Quantité")
            p.drawString(x + 350, y, "Status")
            p.drawString(x + 450, y, "Date")
            y = 730

    # Fermer le PDF
    p.showPage()
    p.save()

    # Revenir au début du buffer
    buffer.seek(0)

    # Créer une réponse HTTP avec le fichier PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="commandes.pdf"'

    return response



def commande_dashboard_view(request):
    produits = Produit.objects.all()
    produit_names = [f"{prod.designation}" for prod in produits]
    prod_total_amounts = []
    prod_order_counts = []

    for prod in produits:
        total_amount = sum(commande.montant_total for commande in Commande.objects.filter(produit=prod))
       # order_count = Commande.objects.filter(produit=prod).count()
        qte=0
        for c in Commande.objects.filter(produit=prod):
            qte+=c.quantite
        order_count=qte
        prod_total_amounts.append(total_amount)
        prod_order_counts.append(order_count)

    context = {
        'client_names': produit_names,
        'client_total_amounts': prod_total_amounts,
        'client_order_counts': prod_order_counts,
    }
    return render(request, 'commande/commande_dashboard.html', context)