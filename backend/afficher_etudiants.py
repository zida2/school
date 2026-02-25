"""
Script pour afficher tous les étudiants
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from api.models import Etudiant
    
    print("\n" + "="*80)
    print("📚 LISTE COMPLÈTE DES ÉTUDIANTS DANS LA BASE DE DONNÉES")
    print("="*80 + "\n")
    
    etudiants = Etudiant.objects.all().order_by('matricule')
    
    if not etudiants:
        print("❌ Aucun étudiant dans la base de données")
        return
    
    for i, e in enumerate(etudiants, 1):
        print(f"{'='*80}")
        print(f"ÉTUDIANT #{i}")
        print(f"{'='*80}")
        print(f"📋 Matricule       : {e.matricule}")
        print(f"👤 Nom complet     : {e.prenom} {e.nom}")
        print(f"📧 Email           : {e.email}")
        print(f"📱 Téléphone       : {e.telephone}")
        print(f"🎓 Filière         : {e.filiere.nom} ({e.filiere.code})")
        print(f"📊 Niveau          : {e.niveau}")
        print(f"✅ Statut          : {e.statut}")
        print(f"💰 Frais filière   : {e.filiere.frais_inscription:,} FCFA".replace(',', ' '))
        print(f"💳 Solde dû        : {e.solde_du:,} FCFA".replace(',', ' '))
        print(f"📅 Date naissance  : {e.date_naissance.strftime('%d/%m/%Y') if e.date_naissance else 'Non renseignée'}")
        print(f"📆 Date inscription: {e.date_inscription.strftime('%d/%m/%Y à %H:%M')}")
        print(f"🏛️  Université      : {e.universite.nom}")
        print(f"📚 Année académique: {e.annee_academique.libelle}")
        
        # Compte utilisateur
        if e.utilisateur:
            print(f"🔐 Compte actif    : {'Oui' if e.utilisateur.is_active else 'Non'}")
            print(f"🔑 Mot de passe    : etudiant123 (par défaut)")
        
        print()
    
    print("="*80)
    print(f"📊 TOTAL : {etudiants.count()} étudiant(s) dans la base de données")
    print("="*80)
    
    # Statistiques par filière
    print("\n" + "="*80)
    print("📈 RÉPARTITION PAR FILIÈRE")
    print("="*80)
    
    from django.db.models import Count
    stats = Etudiant.objects.values('filiere__nom', 'filiere__code').annotate(total=Count('id')).order_by('-total')
    
    for stat in stats:
        print(f"  • {stat['filiere__nom']} ({stat['filiere__code']}) : {stat['total']} étudiant(s)")
    
    # Statistiques par niveau
    print("\n" + "="*80)
    print("📈 RÉPARTITION PAR NIVEAU")
    print("="*80)
    
    stats_niveau = Etudiant.objects.values('niveau').annotate(total=Count('id')).order_by('niveau')
    
    for stat in stats_niveau:
        print(f"  • {stat['niveau']} : {stat['total']} étudiant(s)")
    
    print("\n")

if __name__ == '__main__':
    main()
