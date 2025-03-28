from django.shortcuts import render,redirect
from django.http import HttpResponse
from commande.models import Commande
from client.models import Client
from produit.models import Produit
from .forms import ProduitForm
from produit.filters import ProduitFilter
from django.contrib.auth.decorators import login_required
import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db.models import Sum,Count
# Create your views here.
@login_required(login_url="acces")
def home(request):
    commandes=Commande.objects.all()
    clients=Client.objects.all()
    produits = Produit.objects.all()
    total_produits = produits.count()
    total_commandes=commandes.count()
    total_clients=clients.count()
    derniers_produits = Produit.objects.order_by('-date_ajout')[:4]
    context={'commandes':commandes,'clients':clients,
             'produits': produits,''
            'total_produits':total_produits,
             'total_commandes':total_commandes,
             'total_clients': total_clients,
             'nouveaux_produits': derniers_produits
             }
    return render(request,'produit/acceuil.html',context)

def page_prod(request):
    produits= Produit.objects.all()
    MyFilter = ProduitFilter(request.GET, queryset=produits)
    produits = MyFilter.qs
    context = {'produits': produits,'MyFilter':MyFilter}
    return render(request,"produit/page_prod.html",context)

@login_required(login_url="acces")
def add_produit(request):
    form=ProduitForm()
    if request.method=="POST":
        form=ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("page_prod")
    context={'form':form}
    return render(request,'produit/add_produit.html',context)
# Create your views here.
@login_required(login_url="acces")
def update_produit(request,pk):
    produit=Produit.objects.get(id=pk)
    form=ProduitForm(instance=produit)
    if request.method=="POST":
        form=ProduitForm(request.POST,instance=produit)
        if form.is_valid():
            form.save()
            return redirect("page_prod")
    context={'form':form}
    return render(request,'produit/add_produit.html',context)
# Create your views here.
@login_required(login_url="acces")
def supprimer_produit(request,pk):
    produit = Produit.objects.get(id=pk)
    if request.method == "POST":
        produit.delete()
        return redirect("page_prod")
    context={'item':produit}
    return render(request,'produit/supprimer_produit.html',context)

def exporter_produits_csv(request):
    # Créer une réponse HTTP de type CSV avec encodage UTF-8 et BOM pour Excel
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'
    response.write('\ufeff'.encode('utf8'))  # Ajouter BOM pour Excel

    # Créer un écrivain CSV
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Écrire les en-têtes de colonnes dans le fichier CSV
    writer.writerow(['ID', 'Désignation', 'Prix', 'Quantité en Stock', 'Catégorie', 'Tags', 'Date d\'ajout'])

    # Récupérer tous les produits depuis la base de données
    produits = Produit.objects.all()

    # Parcourir chaque produit et écrire ses données dans le fichier CSV
    for produit in produits:
        tags = '- '.join([tag.designation for tag in produit.tag.all()])
        date_ajout = produit.date_ajout.strftime('%Y/%m/%d')
        # Assurez-vous que les données sont correctement encodées en UTF-8
        writer.writerow([
            produit.id,
            produit.designation,
            produit.prix,
            produit.quantite_stock,
            produit.categorie,
            tags,
            date_ajout
        ])

    # Retourner la réponse HTTP avec le fichier CSV
    return response


def exporter_produits_pdf(request):
    # Créer un buffer en mémoire pour le PDF
    buffer = BytesIO()

    # Créer le PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Liste des Produits")

    # Définir les coordonnées de départ
    y = 750
    x = 50

    # Ajouter le titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(x, y, "Liste des Produits")
    y -= 30  # Déplacement vertical

    # Ajouter les en-têtes des colonnes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "ID")
    p.drawString(x + 50, y, "Désignation")
    p.drawString(x + 150, y, "Prix")
    p.drawString(x + 250, y, "Quantité en Stock")
    p.drawString(x + 400, y, "Catégorie")
    p.drawString(x + 500, y, "Tags")
    y -= 20

    # Récupérer tous les produits depuis la base de données
    produits = Produit.objects.all()

    # Ajouter les données des produits
    p.setFont("Helvetica", 10)
    for produit in produits:
        tags = ', '.join(tag.designation for tag in produit.tag.all())
        p.drawString(x, y, str(produit.id))
        p.drawString(x + 50, y, produit.designation)
        p.drawString(x + 150, y, str(produit.prix))
        p.drawString(x + 250, y, str(produit.quantite_stock))
        p.drawString(x + 400, y, produit.categorie)
        p.drawString(x + 500, y, tags)
        y -= 20
        if y < 50:  # Créer une nouvelle page si nécessaire
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x, y, "ID")
            p.drawString(x + 50, y, "Désignation")
            p.drawString(x + 150, y, "Prix")
            p.drawString(x + 250, y, "Quantité en Stock")
            p.drawString(x + 400, y, "Catégorie")
            p.drawString(x + 500, y, "Tags")
            y = 730

    # Fermer le PDF
    p.showPage()
    p.save()

    # Revenir au début du buffer
    buffer.seek(0)

    # Créer une réponse HTTP avec le fichier PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produits.pdf"'

    return response


def dash_prod(request):
    produits = Produit.objects.all()

    # Calcul des statistiques
    total_produits = produits.count()
    produits_par_categorie = produits.values('categorie').annotate(total=Count('id'))

    # Récupération des prix et des quantités en stock
    prix_produits = list(produits.values_list('prix', flat=True))
    quantite_stock_produits = list(produits.values_list('quantite_stock', flat=True))
    designations_produits = list(produits.values_list('designation', flat=True))

    context = {
        'total_produits': total_produits,
        'produits_par_categorie': produits_par_categorie,
        'prix_produits': prix_produits,
        'quantite_stock_produits': quantite_stock_produits,
        'designations_produits': designations_produits,
        'produits':produits,
    }
    return render(request,"produit/dash_prod.html",context)