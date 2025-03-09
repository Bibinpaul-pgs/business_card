# Generated by Django 5.1.2 on 2025-03-09 09:13

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('profile_image', models.FileField(blank=True, null=True, upload_to='cards/profile_image')),
                ('full_name', models.CharField(blank=True, max_length=300, null=True)),
                ('designation', models.CharField(blank=True, max_length=300, null=True)),
                ('company_name', models.CharField(blank=True, help_text='Company/Organisation name', max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('location_details', models.TextField(blank=True, null=True)),
                ('card_type', models.IntegerField(choices=[(1, 'Public'), (2, 'Private')], default=2)),
                ('social_media_links', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CardFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('file', models.FileField(upload_to='cards/file')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CardRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
            ],
        ),
    ]
