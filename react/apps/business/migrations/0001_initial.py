# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=b'255', verbose_name='name')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'first_name', models.CharField(max_length=b'750', verbose_name='first_name')),
                (b'last_name', models.CharField(max_length=b'750', verbose_name='last_name')),
                (b'email', models.EmailField(unique=True, max_length=75, verbose_name='email')),
                (b'company', models.ForeignKey(to=b'business.Company', to_field='id', verbose_name='company')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
            bases=(models.Model,),
        ),
    ]
