# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import codenerix.fields
import codenerix.lib.helpers


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('digital_sign', codenerix.fields.ImageAngularField(max_length=200, upload_to=codenerix.lib.helpers.upload_path, null=True, verbose_name='Digital sign', blank=True)),
                ('company_seal', codenerix.fields.ImageAngularField(max_length=200, upload_to=codenerix.lib.helpers.upload_path, null=True, verbose_name='Company seal', blank=True)),
                ('company_logo', codenerix.fields.ImageAngularField(max_length=200, upload_to=codenerix.lib.helpers.upload_path, null=True, verbose_name='Company logo', blank=True)),
                ('public', models.BooleanField(default=False, verbose_name='Public')),
            ],
            options={
                'permissions': [('list_corporateimage', 'Can list corporateimage'), ('detail_corporateimage', 'Can view corporateimage')],
            },
        ),
    ]
