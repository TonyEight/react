# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (b'business', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=b'750', verbose_name='name')),
                (b'client', models.ForeignKey(to=b'business.Contact', to_field='id', verbose_name='client')),
                (b'start', models.DateField(verbose_name='start')),
                (b'end', models.DateField(verbose_name='end')),
                (b'days', models.DecimalField(verbose_name='number of days', max_digits=6, decimal_places=2)),
                (b'actor', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id', verbose_name='actor')),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
            },
            bases=(models.Model,),
        ),
    ]
