#!/usr/bin/env python3
"""
Script pour remplacer toutes les occurrences de role == 'professeur' 
par role in ['professeur', 'enseignant'] dans les fichiers backend
"""

import re
import os

def fix_role_checks(filepath):
    """Remplacer les vérifications de rôle professeur"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remplacer role == 'professeur' par role in ['professeur', 'enseignant']
    content = re.sub(
        r"role\s*==\s*['\"]professeur['\"]",
        "role in ['professeur', 'enseignant']",
        content
    )
    
    # Remplacer user.role == 'professeur' par user.role in ['professeur', 'enseignant']
    content = re.sub(
        r"user\.role\s*==\s*['\"]professeur['\"]",
        "user.role in ['professeur', 'enseignant']",
        content
    )
    
    # Remplacer request.user.role == 'professeur' par request.user.role in ['professeur', 'enseignant']
    content = re.sub(
        r"request\.user\.role\s*==\s*['\"]professeur['\"]",
        "request.user.role in ['professeur', 'enseignant']",
        content
    )
    
    # Remplacer self.request.user.role == 'professeur' par self.request.user.role in ['professeur', 'enseignant']
    content = re.sub(
        r"self\.request\.user\.role\s*==\s*['\"]professeur['\"]",
        "self.request.user.role in ['professeur', 'enseignant']",
        content
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Modifié: {filepath}")
        return True
    else:
        print(f"⏭️  Aucun changement: {filepath}")
        return False

if __name__ == '__main__':
    files_to_fix = [
        'api/views.py',
        'api/views_extensions.py',
        'api/permissions.py'
    ]
    
    modified_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_role_checks(filepath):
                modified_count += 1
        else:
            print(f"❌ Fichier non trouvé: {filepath}")
    
    print(f"\n✅ {modified_count} fichier(s) modifié(s)")
