# Generated by Django 3.0.6 on 2020-05-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='company',
            name='balanse',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
