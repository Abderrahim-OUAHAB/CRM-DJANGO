from django.db import models
from client.models import Client
from produit.models import Produit
from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
# Create your models here.

class Commande(models.Model):
    STATUS=(('En attente','En attente'),
            ('En traitement', 'En traitement'),
            ('Annulée','Annulée'),
            ('Terminée','Terminée')
            )
    client=models.ForeignKey(Client,null=True,on_delete=models.SET_NULL)
    produit = models.ForeignKey(Produit,null=True ,on_delete=models.SET_NULL)
    quantite = models.IntegerField(null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)

    def __str__(self):
        return f"Commande {self.id} par {self.client}"

    def calculer_montant_total(self):
        self.montant_total = self.produit.prix * self.quantite

    def save(self, *args, **kwargs):
        self.calculer_montant_total()
        self.clean()  # Appeler la méthode clean() pour vérifier les contraintes
        super().save(*args, **kwargs)

    def update_stock(self, delta):
        if self.produit.quantite_stock + delta < 0:
            raise ValidationError("Stock insuffisant pour cette quantité.")
        self.produit.quantite_stock += delta
        self.produit.save()

    def clean(self):
        # Vérification de la quantité en stock avant de sauvegarder
        if self.produit.quantite_stock < self.quantite:
            raise ValidationError("Stock insuffisant pour cette quantité.")

    def recalculate_client_total(self):
        client_commandes = Commande.objects.filter(client=self.client)
        total_montant_client = sum(commande.produit.prix * commande.quantite for commande in client_commandes)
        for commande in client_commandes:
            commande.montant_total = total_montant_client
            commande.save(update_fields=['montant_total'])

@receiver(pre_save, sender=Commande)
def adjust_stock_on_update(sender, instance, **kwargs):
    if instance.pk:  # Vérifier si l'instance existe déjà en base de données
        old_instance = Commande.objects.get(pk=instance.pk)
        delta = old_instance.quantite - instance.quantite
        try:
            instance.update_stock(delta)
        except ValidationError as e:
            raise e

@receiver(post_save, sender=Commande)
def update_stock_on_create(sender, instance, created, **kwargs):
    if created:
        try:
            instance.update_stock(-instance.quantite)
        except ValidationError as e:
            raise e

@receiver(post_save, sender=Commande)
def recalculer_montant_total(sender, instance, created, **kwargs):
    if created:
        instance.recalculate_client_total()