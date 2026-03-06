# Migration pour supprimer les tables de paiements

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_canal_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='annee_academique',
        ),
        migrations.RemoveField(
            model_name='paiement',
            name='enregistre_par',
        ),
        migrations.RemoveField(
            model_name='paiement',
            name='etudiant',
        ),
        migrations.DeleteModel(
            name='Paiement',
        ),
        migrations.RemoveField(
            model_name='rappelpaiement',
            name='envoye_par',
        ),
        migrations.RemoveField(
            model_name='rappelpaiement',
            name='etudiant',
        ),
        migrations.DeleteModel(
            name='RappelPaiement',
        ),
        migrations.RemoveField(
            model_name='lettrerappel',
            name='etudiant',
        ),
        migrations.RemoveField(
            model_name='lettrerappel',
            name='generee_par',
        ),
        migrations.DeleteModel(
            name='LettreRappel',
        ),
    ]
