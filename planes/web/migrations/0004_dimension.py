# Generated by Django 3.1.6 on 2021-02-06 05:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20210205_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id_plan', models.IntegerField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('problem', models.TextField(blank=True, null=True)),
                ('target', models.TextField(blank=True, null=True)),
                ('goal', models.TextField(blank=True, null=True)),
                ('trace', models.TextField(blank=True, null=True)),
                ('dimension', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Dimensión Social'), (2, 'Dimensión Económica'), (3, 'Dimensión Ambiental'), (4, 'Dimensión Institucional')], null=True)),
                ('political_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dimensions', to='web.politicalorganization')),
            ],
        ),
    ]