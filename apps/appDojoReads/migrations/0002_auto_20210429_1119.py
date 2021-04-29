# Generated by Django 2.2.4 on 2021-04-29 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appDojoReads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libros',
            name='comentario',
        ),
        migrations.AddField(
            model_name='resena',
            name='comentario',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comentario', to='appDojoReads.Libros'),
        ),
    ]