# Generated by Django 3.2 on 2024-05-23 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.titles', verbose_name='ID_произведения'),
        ),
    ]
