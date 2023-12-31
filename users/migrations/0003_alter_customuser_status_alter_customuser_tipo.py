# Generated by Django 4.2 on 2023-06-03 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_almoco_alter_customuser_entrada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='tipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.tipo'),
            preserve_default=False,
        ),
    ]
