#!/usr/bin/env python
"""
Script pour nettoyer toutes les références aux paiements
"""
import re

files_to_clean = {
    'backend/api/serializers.py': [
        (r'# ===== PAIEMENT =====.*?(?=# =====|\Z)', ''),
        (r'# ===== GESTION FINANCIÈRE =====.*?(?=# =====|\Z)', ''),
        (r'Paiement, |, Paiement|RappelPaiement, |, RappelPaiement|LettreRappel, |, LettreRappel', ''),
    ],
    'backend/api/views.py': [
        (r'class PaiementViewSet.*?(?=class |\Z)', ''),
        (r'from \.views_finances import.*?\n', ''),
        (r'Paiement, |, Paiement|RappelPaiement, |, RappelPaiement|LettreRappel, |, LettreRappel', ''),
    ],
    'backend/api/urls.py': [
        (r"router\.register\(r'paiements'.*?\n", ''),
        (r"router\.register\(r'finances'.*?\n", ''),
        (r"router\.register\(r'rappels-paiement'.*?\n", ''),
        (r"router\.register\(r'lettres-rappel'.*?\n", ''),
        (r'from \.views_finances import.*?\n', ''),
        (r'GestionFinanciereViewSet, |, GestionFinanciereViewSet|RappelPaiementViewSet, |, RappelPaiementViewSet|LettreRappelViewSet, |, LettreRappelViewSet', ''),
    ],
    'backend/api/admin.py': [
        (r'@admin\.register\(Paiement\).*?(?=@admin\.register|\Z)', ''),
        (r'@admin\.register\(RappelPaiement\).*?(?=@admin\.register|\Z)', ''),
        (r'@admin\.register\(LettreRappel\).*?(?=@admin\.register|\Z)', ''),
        (r'Paiement, |, Paiement|RappelPaiement, |, RappelPaiement|LettreRappel, |, LettreRappel', ''),
    ],
}

print("🧹 Nettoyage des références aux paiements...")
print("=" * 60)

for filepath, patterns in files_to_clean.items():
    print(f"\n📄 {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_length = len(content)
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Nettoyer les lignes vides multiples
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        removed = original_length - len(content)
        print(f"  ✅ {removed} caractères supprimés")
        
    except FileNotFoundError:
        print(f"  ⚠️  Fichier non trouvé")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

print("\n" + "=" * 60)
print("✅ Nettoyage terminé!")
