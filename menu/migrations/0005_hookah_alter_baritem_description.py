# Generated by Django 5.0.1 on 2024-02-01 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_barcategory_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hookah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='baritem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
