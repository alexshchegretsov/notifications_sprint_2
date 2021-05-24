# Generated by Django 3.2.3 on 2021-05-23 12:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event', models.CharField(max_length=50)),
                ('text', models.TextField()),
            ],
            options={
                'db_table': '"public"."content"',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('recipient', models.CharField(max_length=255)),
                ('status', models.CharField(default='pending', max_length=255)),
                ('content_id', models.ForeignKey(db_column='content_id', on_delete=django.db.models.deletion.CASCADE, to='admin_panel.content')),
            ],
            options={
                'db_table': '"public"."notification"',
            },
        ),
        migrations.CreateModel(
            name='Compaigne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_id', models.ForeignKey(db_column='content_id', on_delete=django.db.models.deletion.DO_NOTHING, to='admin_panel.content')),
            ],
            options={
                'db_table': '"public"."compaigne"',
            },
        ),
    ]
