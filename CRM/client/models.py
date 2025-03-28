from django.db import models

# Create your models here.
class Client(models.Model):
    nom=models.CharField(max_length=200,null=True)
    prenom = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100,unique=True,null=True)
    telephone=models.CharField(max_length=200,null=True,blank=True)
    addresse = models.TextField(max_length=100,blank=True,null=True)
    societe= models.CharField(max_length=100, blank=True,null=True)
    date_ajout= models.DateTimeField(auto_now_add=True)
    dernier_modif = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom+" "+self.prenom



