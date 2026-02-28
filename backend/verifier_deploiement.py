#!/usr/bin/env python
"""
Script de vérification post-déploiement
À exécuter sur PythonAnywhere après le git pull
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Note, Utilisateur, Enseignant, Etudiant

print("=" * 70)
print("🔍 VÉRIFICATION POST-DÉPLOIEMENT")
print("=" * 70)

# Test 1: Vérifier que la propriété mention fonctionne
print("\n✅ Test 1: Propriété mention du modèle Note")
try:
    note = Note.objects.first()
    if note:
        mention = note.mention  # Ceci devrait fonctionner maintenant
        print(f"   ✅ Propriété mention fonctionne: {mention}")
        print(f"   Note testée: {note.etudiant.prenom} {note.etudiant.nom} - {note.matiere.nom}")
        print(f"   Moyenne: {note.moyenne}, Mention: {mention}")
    else:
        print("   ⚠️ Aucune note dans la base de données")
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print("   Le déploiement a peut-être échoué!")

# Test 2: Vérifier les comptes de test
print("\n✅ Test 2: Comptes de test Ouedraogo et Diallo")
try:
    prof = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
    etudiant = Utilisateur.objects.get(email='m.diallo@etu.bf')
    print(f"   ✅ Prof: {prof.prenom} {prof.nom} ({prof.role})")
    print(f"   ✅ Étudiant: {etudiant.prenom} {etudiant.nom} ({etudiant.role})")
except Exception as e:
    print(f"   ❌ ERREUR: {e}")

# Test 3: Vérifier les notes de Diallo
print("\n✅ Test 3: Notes de Moussa Diallo")
try:
    etudiant = Etudiant.objects.get(utilisateur__email='m.diallo@etu.bf')
    notes = Note.objects.filter(etudiant=etudiant)
    print(f"   Total notes: {notes.count()}")
    print(f"   Notes publiées: {notes.filter(publie=True).count()}")
    print(f"   Notes en brouillon: {notes.filter(publie=False).count()}")
    
    # Afficher quelques notes
    for note in notes[:3]:
        try:
            print(f"   - {note.matiere.nom}: Moyenne={note.moyenne}, Mention={note.mention}")
        except Exception as e:
            print(f"   - {note.matiere.nom}: ERREUR={e}")
except Exception as e:
    print(f"   ❌ ERREUR: {e}")

# Test 4: Vérifier les matières de Ouedraogo
print("\n✅ Test 4: Matières enseignées par Ouedraogo")
try:
    enseignant = Enseignant.objects.get(utilisateur__email='j.ouedraogo@uan.bf')
    matieres = enseignant.matieres.all()
    print(f"   Total matières: {matieres.count()}")
    for matiere in matieres[:5]:
        print(f"   - {matiere.nom} ({matiere.code})")
    if matieres.count() > 5:
        print(f"   ... et {matieres.count() - 5} autres")
except Exception as e:
    print(f"   ❌ ERREUR: {e}")

# Résumé
print("\n" + "=" * 70)
print("📋 RÉSUMÉ")
print("=" * 70)
print("Si tous les tests sont ✅, le déploiement est réussi!")
print("Vous pouvez maintenant tester l'application web.")
print("\nTest à faire:")
print("1. Ouvrir: https://school-wheat-six.vercel.app")
print("2. Se connecter: j.ouedraogo@uan.bf / enseignant123")
print("3. Aller dans 'Saisie des notes'")
print("4. Sélectionner une matière")
print("5. Vérifier que la liste des étudiants apparaît")
print("=" * 70)
