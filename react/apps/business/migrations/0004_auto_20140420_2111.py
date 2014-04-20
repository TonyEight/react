# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20140420_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name=u'email'),
        ),
    ]
