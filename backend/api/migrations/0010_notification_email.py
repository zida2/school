# Migration pour ajouter les notifications email

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_suppression_paiements'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_notification', models.CharField(choices=[('nouvelle_note', 'Nouvelle note publiée'), ('modification_note', 'Note modifiée'), ('nouvelle_evaluation', 'Nouvelle évaluation programmée'), ('absence_signale', 'Absence signalée'), ('support_cours', 'Nouveau support de cours'), ('emploi_modifie', 'Emploi du temps modifié'), ('demande_traitee', 'Demande administrative traitée'), ('message_canal', 'Nouveau message dans un canal'), ('annonce_officielle', 'Annonce officielle')], max_length=30)),
                ('sujet', models.CharField(max_length=200)),
                ('contenu', models.TextField()),
                ('lien', models.CharField(blank=True, max_length=500)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('envoye', models.BooleanField(default=False)),
                ('date_envoi', models.DateTimeField(blank=True, null=True)),
                ('erreur', models.TextField(blank=True)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_email', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification Email',
                'verbose_name_plural': 'Notifications Email',
                'ordering': ['-date_creation'],
                'indexes': [
                    models.Index(fields=['destinataire', '-date_creation'], name='api_notific_destina_idx'),
                    models.Index(fields=['envoye', 'date_creation'], name='api_notific_envoye_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='PreferenceNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activer_emails', models.BooleanField(default=True)),
                ('nouvelle_note', models.BooleanField(default=True)),
                ('modification_note', models.BooleanField(default=True)),
                ('nouvelle_evaluation', models.BooleanField(default=True)),
                ('absence_signale', models.BooleanField(default=True)),
                ('support_cours', models.BooleanField(default=True)),
                ('emploi_modifie', models.BooleanField(default=True)),
                ('demande_traitee', models.BooleanField(default=True)),
                ('message_canal', models.BooleanField(default=True)),
                ('annonce_officielle', models.BooleanField(default=True)),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences_notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Préférence de Notification',
                'verbose_name_plural': 'Préférences de Notification',
            },
        ),
    ]
