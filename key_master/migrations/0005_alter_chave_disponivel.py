# Generated by Django 4.2.2 on 2023-06-14 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_master', '0004_alter_aluguel_data_aluguel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chave',
            name='disponivel',
            field=models.BooleanField(default=True, verbose_name='Disponivel'),
        ),
    ]
