# Generated by Django 4.2.7 on 2023-11-01 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bistrooapp_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category_sort_id'], 'verbose_name_plural': 'categori_names'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='category_name',
        ),
    ]
