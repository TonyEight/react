# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length='750', verbose_name=u'first_name')),
                ('last_name', models.CharField(max_length='750', verbose_name=u'last_name')),
                ('e_mail', models.EmailField(max_length=75, verbose_name=u'email')),
                ('company', models.ForeignKey(to='business.Company', to_field=u'id', verbose_name=u'company')),
            ],
            options={
                u'verbose_name': u'Contact',
                u'verbose_name_plural': u'Contacts',
            },
            bases=(models.Model,),
        ),
    ]
