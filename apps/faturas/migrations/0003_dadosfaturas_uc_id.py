# Generated by Django 3.2.6 on 2023-02-11 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps_clientes', '0001_initial'),
        ('apps_faturas', '0002_dadosfaturas'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosfaturas',
            name='uc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps_clientes.uc'),
        ),
    ]
