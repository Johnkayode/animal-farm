# Generated by Django 3.2.9 on 2021-12-02 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_vendor_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='address',
        ),
        migrations.AddField(
            model_name='vendor',
            name='state',
            field=models.CharField(max_length=250, null=True, verbose_name='state'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='street',
            field=models.CharField(max_length=250, null=True, verbose_name='street'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='city',
            field=models.CharField(max_length=250, null=True, verbose_name='city'),
        ),
    ]