# Generated by Django 3.0.5 on 2020-05-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NA_WebApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthYear',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Others')], null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hasKids',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lat',
            field=models.DecimalField(decimal_places=8, default=41.086203, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lng',
            field=models.DecimalField(decimal_places=8, default=29.044378, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='married',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
