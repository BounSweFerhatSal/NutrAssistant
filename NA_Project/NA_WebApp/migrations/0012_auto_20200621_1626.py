# Generated by Django 3.0.5 on 2020-06-21 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NA_WebApp', '0011_auto_20200619_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gramWeight', models.DecimalField(decimal_places=4, default=0, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='ingredient_composition',
            name='unitname',
            field=models.CharField(default='?', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Ingredient_Portions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NA_WebApp.Ingredient')),
                ('portion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NA_WebApp.Portion')),
            ],
        ),
    ]
