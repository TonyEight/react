# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length='255', verbose_name=u'name')),
            ],
            options={
                u'verbose_name': u'Company',
                u'verbose_name_plural': u'Companies',
            },
            bases=(models.Model,),
        ),
    ]
