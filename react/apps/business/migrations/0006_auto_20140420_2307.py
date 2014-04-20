# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_contract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='contact',
            new_name='client',
        ),
    ]
