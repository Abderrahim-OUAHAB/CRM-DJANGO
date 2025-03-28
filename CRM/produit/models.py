from django.db import models

# Create your models here.
class Tag(models.Model):
    designation = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.designation
class Produit(models.Model):
    designation=models.CharField(max_length=200,null=True)
    prix=models.FloatField(null=True)
    quantite_stock=models.IntegerField(null=True)
    categorie = models.CharField(max_length=50, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=200,null=True)
    tag=models.ManyToManyField(Tag)


    def __str__(self):
        return self.designation