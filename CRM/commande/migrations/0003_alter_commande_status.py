# Generated by Django 5.0.6 on 2024-06-12 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("commande", "0002_rename_date_ajout_commande_date_commande_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commande",
            name="status",
            field=models.CharField(
                choices=[
                    ("En attente", "En attente"),
                    ("En traitement", "En traitement"),
                    ("Annulée", "Annulée"),
                    ("Terminée", "Terminée"),
                ],
                max_length=200,
                null=True,
            ),
        ),
    ]
