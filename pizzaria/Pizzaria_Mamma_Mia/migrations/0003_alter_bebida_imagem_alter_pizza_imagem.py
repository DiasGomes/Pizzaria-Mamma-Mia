# Generated by Django 4.2.2 on 2023-06-10 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Pizzaria_Mamma_Mia", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bebida",
            name="imagem",
            field=models.ImageField(null=True, upload_to="media/imagens/"),
        ),
        migrations.AlterField(
            model_name="pizza",
            name="imagem",
            field=models.ImageField(null=True, upload_to="media/imagens/"),
        ),
    ]
