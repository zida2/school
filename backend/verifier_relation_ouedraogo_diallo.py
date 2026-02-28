#!/usr/bin/env python
"""
Script pour vérifier la relation entre Ouedraogo (enseignant) et Diallo (étudiant)
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Etudiant, Enseignant, Matiere, Note

print("=" * 70)
print("VÉRIFICATION RELATION OUEDRAOGO (PROF) ↔ DIALLO (ÉTUDIANT)")
print("=" * 70)

# Récupérer l'enseignant Ouedraogo
try:
    user_prof = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
    enseignant = user_prof.enseignant
    print(f"\n✅ ENSEIGNANT: {enseignant.prenom} {enseignant.nom}")
    print(f"   Email: {user_prof.email}")
    print(f"   Matricule: {enseignant.matricule}")
except Exception as e:
    print(f"❌ Erreur enseignant: {e}")
    sys.exit(1)

# Récupérer l'étudiant Diallo
try:
    user_etudiant = Utilisateur.objects.get(email='m.diallo@etu.bf')
    etudiant = user_etudiant.etudiant
    print(f"\n✅ ÉTUDIANT: {etudiant.prenom} {etudiant.nom}")
    print(f"   Email: {user_etudiant.email}")
    print(f"   Matricule: {etudiant.matricule}")
    print(f"   Filière: {etudiant.filiere.nom}")
except Exception as e:
    print(f"❌ Erreur étudiant: {e}")
    sys.exit(1)

# Vérifier les matières enseignées par Ouedraogo
print(f"\n📚 MATIÈRES ENSEIGNÉES PAR {enseignant.prenom} {enseignant.nom}:")
matieres = enseignant.matieres.all()
print(f"   Total: {matieres.count()} matières")
for i, matiere in enumerate(matieres, 1):
    print(f"   {i}. {matiere.nom} ({matiere.code}) - Filière: {matiere.filiere.nom}")

# Vérifier si Diallo est dans la même filière
print(f"\n🔍 VÉRIFICATION FILIÈRE:")
matieres_filiere_diallo = matieres.filter(filiere=etudiant.filiere)
if matieres_filiere_diallo.exists():
    print(f"   ✅ Ouedraogo enseigne {matieres_filiere_diallo.count()} matière(s) dans la filière de Diallo")
    for matiere in matieres_filiere_diallo:
        print(f"      - {matiere.nom}")
else:
    print(f"   ❌ Ouedraogo n'enseigne pas dans la filière de Diallo ({etudiant.filiere.nom})")

# Vérifier les notes existantes de Diallo dans les matières de Ouedraogo
print(f"\n📝 NOTES DE DIALLO DANS LES MATIÈRES DE OUEDRAOGO:")
notes = Note.objects.filter(
    etudiant=etudiant,
    matiere__in=matieres
).select_related('matiere')

if notes.exists():
    print(f"   ✅ {notes.count()} note(s) trouvée(s):")
    for note in notes:
        statut = "✅ Publiée" if note.publie else "📝 Brouillon"
        print(f"      - {note.matiere.nom}:")
        print(f"        CC: {note.note_cc or 'Non saisie'}")
        print(f"        Examen: {note.note_examen or 'Non saisie'}")
        print(f"        Moyenne: {note.moyenne or 'N/A'}")
        print(f"        Statut: {statut}")
else:
    print(f"   ⚠️ Aucune note trouvée")
    print(f"   💡 Vous pouvez créer des notes de test pour Diallo")

# Résumé pour le test
print(f"\n" + "=" * 70)
print("📋 RÉSUMÉ POUR LE TEST:")
print("=" * 70)
print(f"1. Connectez-vous en tant que PROF:")
print(f"   Email: j.ouedraogo@uan.bf")
print(f"   Password: enseignant123")
print(f"\n2. Allez dans 'Saisie des notes'")
print(f"   - Sélectionnez la filière: {etudiant.filiere.nom}")
if matieres_filiere_diallo.exists():
    print(f"   - Sélectionnez une matière: {matieres_filiere_diallo.first().nom}")
print(f"   - Vous devriez voir {etudiant.prenom} {etudiant.nom} dans la liste")
print(f"\n3. Saisissez les notes de Diallo et publiez")
print(f"\n4. Déconnectez-vous et connectez-vous en tant qu'ÉTUDIANT:")
print(f"   Email: m.diallo@etu.bf")
print(f"   Password: etudiant123")
print(f"\n5. Vérifiez que les notes apparaissent dans le dashboard étudiant")
print("=" * 70)
