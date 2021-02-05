# Generated by Django 3.1.6 on 2021-02-05 04:49

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('pages', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PoliticalOrganization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.PositiveSmallIntegerField()),
                ('text', models.TextField(blank=True, null=True)),
                ('tokens', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='web.document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='political_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='web.politicalorganization'),
        ),
    ]
