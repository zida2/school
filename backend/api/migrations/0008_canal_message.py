# Generated migration for Canal and Message models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_merge_20260228_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Canal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('type_canal', models.CharField(choices=[('officiel', 'Canal Officiel'), ('etudiant', 'Canal Étudiants')], max_length=20)),
                ('actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Canal',
                'verbose_name_plural': 'Canaux',
                'ordering': ['type_canal', 'nom'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('modifie', models.BooleanField(default=False)),
                ('date_modification', models.DateTimeField(blank=True, null=True)),
                ('canal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.canal')),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_envoyes_canal', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['date_envoi'],
            },
        ),
        migrations.CreateModel(
            name='LectureMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_lecture', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='api.message')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_lus', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lecture Message',
                'verbose_name_plural': 'Lectures Messages',
                'unique_together': {('message', 'utilisateur')},
            },
        ),
    ]
