# Generated by Django 4.2 on 2023-04-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0008_offer_alter_componenteorden_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('1', 'Enviada'), ('2', 'No enviada')], default='2', max_length=2, verbose_name='Estado'),
        ),
    ]
