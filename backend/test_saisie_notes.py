#!/usr/bin/env python
"""
Script de test pour la saisie des notes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Enseignant, Etudiant, Matiere, Note, AnneeAcademique
from decimal import Decimal

print("=" * 60)
print("TEST DE LA SAISIE DES NOTES")
print("=" * 60)

# Test 1: Vérifier l'enseignant J. Ouedraogo
print("\n1. ENSEIGNANT J. OUEDRAOGO:")
print("-" * 60)
try:
    enseignant = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
    print(f"✅ Enseignant trouvé: {enseignant.prenom} {enseignant.nom}")
    print(f"   Matières enseignées: {enseignant.matieres.count()}")
    
    # Afficher les matières
    for matiere in enseignant.matieres.all()[:5]:
        print(f"   - {matiere.nom} (Coef: {matiere.coefficient}, Semestre: {matiere.semestre})")
        
except Enseignant.DoesNotExist:
    print("❌ Enseignant non trouvé")
    exit(1)

# Test 2: Vérifier les étudiants de la filière
print("\n2. ÉTUDIANTS DE LA FILIÈRE:")
print("-" * 60)
matiere = enseignant.matieres.first()
if matiere:
    print(f"Matière sélectionnée: {matiere.nom}")
    print(f"Filière: {matiere.filiere.nom}")
    
    etudiants = Etudiant.objects.filter(filiere=matiere.filiere)
    print(f"\n✅ {etudiants.count()} étudiant(s) dans la filière\n")
    
    for e in etudiants[:10]:
        print(f"   - {e.matricule}: {e.prenom} {e.nom} ({e.niveau})")
else:
    print("❌ Aucune matière trouvée")
    exit(1)

# Test 3: Créer des notes de test
print("\n3. CRÉATION DE NOTES DE TEST:")
print("-" * 60)

annee = AnneeAcademique.objects.filter(active=True).first()
if not annee:
    annee = AnneeAcademique.objects.first()

if not annee:
    print("❌ Aucune année académique trouvée")
    exit(1)

print(f"Année académique: {annee.libelle}")

# Créer des notes pour quelques étudiants
notes_creees = 0
for i, etudiant in enumerate(etudiants[:5], 1):
    # Vérifier si la note existe déjà
    note, created = Note.objects.get_or_create(
        etudiant=etudiant,
        matiere=matiere,
        annee_academique=annee,
        defaults={
            'note_cc': Decimal('12.00') + i,
            'note_examen': Decimal('13.00') + i,
            'publie': False
        }
    )
    
    if created:
        notes_creees += 1
        moyenne = float(note.note_cc) * 0.4 + float(note.note_examen) * 0.6
        print(f"\n✅ Note créée:")
        print(f"   Étudiant: {etudiant.prenom} {etudiant.nom}")
        print(f"   CC: {note.note_cc}/20")
        print(f"   Examen: {note.note_examen}/20")
        print(f"   Moyenne: {moyenne:.2f}/20")
        print(f"   Statut: {'Validé' if moyenne >= 10 else 'Ajourné'}")
    else:
        print(f"\n⚠️  Note existante pour {etudiant.prenom} {etudiant.nom}")

print(f"\n{notes_creees} note(s) créée(s)")

# Test 4: Statistiques des notes
print("\n4. STATISTIQUES DES NOTES:")
print("-" * 60)

notes_matiere = Note.objects.filter(matiere=matiere, annee_academique=annee)
total_notes = notes_matiere.count()
notes_publiees = notes_matiere.filter(publie=True).count()
notes_non_publiees = notes_matiere.filter(publie=False).count()

print(f"Total notes: {total_notes}")
print(f"Notes publiées: {notes_publiees}")
print(f"Notes non publiées: {notes_non_publiees}")

# Calculer les moyennes
moyennes = []
for note in notes_matiere:
    if note.note_cc is not None and note.note_examen is not None:
        moyenne = float(note.note_cc) * 0.4 + float(note.note_examen) * 0.6
        moyennes.append(moyenne)

if moyennes:
    moyenne_classe = sum(moyennes) / len(moyennes)
    taux_reussite = len([m for m in moyennes if m >= 10]) / len(moyennes) * 100
    
    print(f"\nMoyenne de la classe: {moyenne_classe:.2f}/20")
    print(f"Taux de réussite: {taux_reussite:.1f}%")
    print(f"Note min: {min(moyennes):.2f}/20")
    print(f"Note max: {max(moyennes):.2f}/20")

# Test 5: Vérifier les notes par étudiant
print("\n5. DÉTAIL DES NOTES:")
print("-" * 60)

for note in notes_matiere[:5]:
    moyenne = float(note.note_cc) * 0.4 + float(note.note_examen) * 0.6 if note.note_cc and note.note_examen else 0
    print(f"\n{note.etudiant.matricule} - {note.etudiant.prenom} {note.etudiant.nom}")
    print(f"  CC: {note.note_cc or '-'}/20")
    print(f"  Examen: {note.note_examen or '-'}/20")
    print(f"  Moyenne: {moyenne:.2f}/20" if moyenne > 0 else "  Moyenne: -")
    print(f"  Statut: {'✅ Validé' if moyenne >= 10 else '❌ Ajourné' if moyenne > 0 else '⏳ En attente'}")
    print(f"  Publié: {'Oui' if note.publie else 'Non'}")

print("\n" + "=" * 60)
print("TEST TERMINÉ")
print("=" * 60)

print("\n📝 RÉSUMÉ:")
print(f"- Enseignant: {enseignant.prenom} {enseignant.nom}")
print(f"- Matières: {enseignant.matieres.count()}")
print(f"- Étudiants dans la filière: {etudiants.count()}")
print(f"- Notes créées: {notes_creees}")
print(f"- Total notes: {total_notes}")
print(f"- Moyenne classe: {moyenne_classe:.2f}/20" if moyennes else "- Moyenne classe: N/A")
print(f"- Taux de réussite: {taux_reussite:.1f}%" if moyennes else "- Taux de réussite: N/A")
