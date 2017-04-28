# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=128, verbose_name='City')),
            ],
            options={
                'permissions': [('list_city', 'Can list city'), ('detail_city', 'Can view city')],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=128, verbose_name='Country')),
            ],
            options={
                'permissions': [('list_country', 'Can list country'), ('detail_country', 'Can view country')],
            },
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('postalcode', models.IntegerField(verbose_name='Postal Code')),
                ('city', models.ForeignKey(related_name='postalcodes', to='codenerix_extensions.City')),
            ],
            options={
                'permissions': [('list_postalcode', 'Can list postalcode'), ('detail_postalcode', 'Can view postalcode')],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=128, verbose_name='Province')),
            ],
            options={
                'permissions': [('list_province', 'Can list province'), ('detail_province', 'Can view province')],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=128, verbose_name='Region')),
                ('country', models.ForeignKey(related_name='countries', to='codenerix_extensions.Country')),
            ],
            options={
                'permissions': [('list_region', 'Can list region'), ('detail_region', 'Can view region')],
            },
        ),
        migrations.AddField(
            model_name='province',
            name='region',
            field=models.ForeignKey(related_name='regions', to='codenerix_extensions.Region'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(related_name='cities', to='codenerix_extensions.Province'),
        ),
    ]
