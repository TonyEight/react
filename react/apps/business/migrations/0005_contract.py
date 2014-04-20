# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0004_auto_20140420_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length='750', verbose_name=u'name')),
                ('contact', models.ForeignKey(to='business.Contact', to_field=u'id', verbose_name=u'contact')),
                ('start', models.DateField(verbose_name=u'start')),
                ('end', models.DateField(verbose_name=u'end')),
                ('days', models.DecimalField(verbose_name=u'number of days', max_digits=6, decimal_places=2)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id', verbose_name=u'actor')),
            ],
            options={
                u'verbose_name': u'Contract',
                u'verbose_name_plural': u'Contracts',
            },
            bases=(models.Model,),
        ),
    ]
