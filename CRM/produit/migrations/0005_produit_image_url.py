# Generated by Django 5.0.6 on 2024-06-25 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produit", "0004_alter_produit_quantite_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="image_url",
            field=models.URLField(null=True),
        ),
    ]
