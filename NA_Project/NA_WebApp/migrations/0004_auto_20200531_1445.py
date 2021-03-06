# Generated by Django 3.0.5 on 2020-05-31 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NA_WebApp', '0003_auto_20200530_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hasKids',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lat',
            field=models.DecimalField(decimal_places=18, default=41.086203, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lng',
            field=models.DecimalField(decimal_places=18, default=29.044378, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='married',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], null=True),
        ),
    ]
