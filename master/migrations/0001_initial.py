# Generated by Django 5.0.7 on 2025-01-03 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'db_table': 'Brand',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
                'db_table': 'Store',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.brand')),
            ],
            options={
                'verbose_name': 'Smartphone',
                'verbose_name_plural': 'Smartphones',
                'db_table': 'Smartphone',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('link', models.URLField(null=True)),
                ('refurbished', models.BooleanField(default=False)),
                ('smartphone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.smartphone')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.store')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'Product',
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('smartphone', 'store'), name='unique_smartphone_store'),
        ),
    ]
