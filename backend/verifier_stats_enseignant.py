#!/usr/bin/env python
"""
Script pour vérifier la cohérence des statistiques de l'enseignant
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.db import models
from api.models import Enseignant, Etudiant, Matiere, Note, EmploiDuTemps

print("=" * 70)
print("VÉRIFICATION DES STATISTIQUES ENSEIGNANT")
print("=" * 70)

# Enseignant J. Ouedraogo
try:
    enseignant = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
    print(f"\n✅ Enseignant: {enseignant.prenom} {enseignant.nom}")
    print("=" * 70)
    
    # 1. Matières enseignées
    matieres = enseignant.matieres.all()
    nb_matieres = matieres.count()
    print(f"\n📚 MATIÈRES ENSEIGNÉES: {nb_matieres}")
    print("-" * 70)
    for m in matieres:
        print(f"   - {m.nom} ({m.code}) - Coef: {m.coefficient}, Semestre: {m.semestre}")
        print(f"     Filière: {m.filiere.nom}")
    
    # 2. Étudiants (via les filières des matières)
    filieres_ids = set(matieres.values_list('filiere', flat=True))
    etudiants = Etudiant.objects.filter(filiere__in=filieres_ids).distinct()
    nb_etudiants = etudiants.count()
    print(f"\n🎓 ÉTUDIANTS: {nb_etudiants}")
    print("-" * 70)
    print(f"   Filières concernées: {len(filieres_ids)}")
    for filiere_id in filieres_ids:
        filiere_etudiants = etudiants.filter(filiere_id=filiere_id)
        filiere_nom = filiere_etudiants.first().filiere.nom if filiere_etudiants.exists() else "N/A"
        print(f"   - {filiere_nom}: {filiere_etudiants.count()} étudiant(s)")
    
    print(f"\n   Liste des étudiants:")
    for e in etudiants[:10]:
        print(f"   - {e.matricule}: {e.prenom} {e.nom} ({e.niveau})")
    if nb_etudiants > 10:
        print(f"   ... et {nb_etudiants - 10} autre(s)")
    
    # 3. Notes saisies
    notes_total = Note.objects.filter(matiere__in=matieres)
    notes_saisies = notes_total.filter(
        models.Q(note_cc__isnull=False) | models.Q(note_examen__isnull=False)
    )
    nb_notes_saisies = notes_saisies.count()
    print(f"\n📝 NOTES SAISIES: {nb_notes_saisies}")
    print("-" * 70)
    print(f"   Total notes (toutes matières): {notes_total.count()}")
    print(f"   Notes avec CC ou Examen: {nb_notes_saisies}")
    
    # Détail par matière
    print(f"\n   Détail par matière:")
    for m in matieres:
        notes_matiere = Note.objects.filter(matiere=m)
        notes_saisies_matiere = notes_matiere.filter(
            models.Q(note_cc__isnull=False) | models.Q(note_examen__isnull=False)
        )
        print(f"   - {m.nom}: {notes_saisies_matiere.count()}/{notes_matiere.count()} notes saisies")
    
    # 4. Cours cette semaine (emploi du temps)
    emplois = EmploiDuTemps.objects.filter(matiere__in=matieres)
    nb_cours = emplois.count()
    print(f"\n📅 COURS (EMPLOI DU TEMPS): {nb_cours}")
    print("-" * 70)
    
    # Grouper par jour
    jours = {}
    for emploi in emplois:
        if emploi.jour not in jours:
            jours[emploi.jour] = []
        jours[emploi.jour].append(emploi)
    
    for jour in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']:
        if jour in jours:
            print(f"\n   {jour}:")
            for e in jours[jour]:
                print(f"   - {e.heure_debut}-{e.heure_fin}: {e.matiere.nom} (Salle {e.salle})")
    
    # RÉSUMÉ FINAL
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES STATISTIQUES")
    print("=" * 70)
    print(f"Matières enseignées:  {nb_matieres}")
    print(f"Étudiants:            {nb_etudiants}")
    print(f"Notes saisies:        {nb_notes_saisies}")
    print(f"Cours (emploi):       {nb_cours}")
    print("=" * 70)
    
    # Vérification de cohérence
    print("\n✅ VÉRIFICATION DE COHÉRENCE:")
    print("-" * 70)
    
    # Vérifier que chaque matière a des étudiants potentiels
    for m in matieres:
        etudiants_matiere = Etudiant.objects.filter(filiere=m.filiere)
        if etudiants_matiere.count() == 0:
            print(f"⚠️  {m.nom}: Aucun étudiant dans la filière {m.filiere.nom}")
        else:
            print(f"✅ {m.nom}: {etudiants_matiere.count()} étudiant(s) potentiel(s)")
    
    print("\n" + "=" * 70)
    print("VÉRIFICATION TERMINÉE")
    print("=" * 70)
    
except Enseignant.DoesNotExist:
    print("❌ Enseignant J. Ouedraogo non trouvé")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

