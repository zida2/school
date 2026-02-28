# Script pour standardiser tous les dashboards avec le design moderne

$dashboards = @(
    "dashboard-etudiant.html",
    "dashboard-prof.html",
    "dashboard-bureau.html",
    "dashboard-superadmin.html"
)

foreach ($dashboard in $dashboards) {
    if (Test-Path $dashboard) {
        Write-Host "Traitement de $dashboard..." -ForegroundColor Cyan
        
        $content = Get-Content $dashboard -Raw -Encoding UTF8
        
        # Remplacer les classes
        $content = $content -replace 'app-container', 'app-wrapper'
        $content = $content -replace 'sidebar-premium', 'sidebar-ultra'
        $content = $content -replace 'sidebar-logo', 'logo-icon-ultra'
        $content = $content -replace 'sidebar-brand-name', 'logo-name-ultra'
        $content = $content -replace 'sidebar-brand-tagline', 'logo-tag-ultra'
        $content = $content -replace 'sidebar-brand', 'logo-text-ultra'
        $content = $content -replace 'sidebar-nav', 'sidebar-nav-ultra'
        $content = $content -replace 'nav-section-label', 'nav-label-ultra'
        $content = $content -replace 'nav-section', 'nav-section-ultra'
        $content = $content -replace 'nav-item-premium', 'nav-item-ultra'
        $content = $content -replace 'nav-icon', 'nav-icon-ultra'
        $content = $content -replace 'nav-text', 'nav-text-ultra'
        $content = $content -replace 'main-wrapper', 'main-ultra'
        $content = $content -replace 'topbar-premium', 'topbar-ultra'
        $content = $content -replace 'topbar-left', 'topbar-left-ultra'
        $content = $content -replace 'topbar-right', 'topbar-right-ultra'
        $content = $content -replace 'btn-menu-toggle', 'btn-menu-ultra'
        $content = $content -replace 'search-bar', 'search-ultra'
        $content = $content -replace 'search-icon', 'search-icon-ultra'
        $content = $content -replace 'search-input', 'search-input-ultra'
        $content = $content -replace 'topbar-action', 'topbar-btn-ultra'
        $content = $content -replace 'user-menu', 'user-menu-ultra'
        $content = $content -replace 'user-avatar', 'user-avatar-ultra'
        $content = $content -replace 'user-info', 'user-info-ultra'
        $content = $content -replace 'user-name', 'user-name-ultra'
        $content = $content -replace 'user-role', 'user-role-ultra'
        $content = $content -replace 'content-area', 'content-ultra'
        $content = $content -replace 'page-header', 'page-header-ultra'
        $content = $content -replace 'page-title-row', 'page-title-row-ultra'
        $content = $content -replace 'page-title', 'page-title-ultra'
        $content = $content -replace 'page-subtitle', 'page-subtitle-ultra'
        $content = $content -replace 'page-actions', 'page-actions-ultra'
        $content = $content -replace 'stats-grid', 'stats-grid-ultra'
        $content = $content -replace 'stat-card-premium', 'stat-card-ultra'
        $content = $content -replace 'stat-icon-wrapper', 'stat-icon-ultra'
        $content = $content -replace 'stat-value', 'stat-value-ultra'
        $content = $content -replace 'stat-label', 'stat-label-ultra'
        $content = $content -replace 'card-premium', 'card-ultra'
        $content = $content -replace 'card-header-premium', 'card-header-ultra'
        $content = $content -replace 'card-title-premium', 'card-title-ultra'
        $content = $content -replace 'card-body-premium', 'card-body-ultra'
        $content = $content -replace 'table-premium', 'table-ultra'
        $content = $content -replace 'btn-premium', 'btn-ultra'
        $content = $content -replace 'btn-primary', 'btn-primary-ultra'
        $content = $content -replace 'btn-outline', 'btn-secondary-ultra'
        
        # Remplacer les fonctions JavaScript
        $content = $content -replace 'navToPremium', 'navToUltra'
        
        # Remplacer les polices
        $content = $content -replace 'Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800', 'Poppins:wght@300;400;500;600;700;800;900'
        $content = $content -replace 'Inter', 'Poppins'
        $content = $content -replace 'Outfit', 'Poppins'
        
        # Mettre à jour la version du theme-toggle.js
        $content = $content -replace 'theme-toggle\.js\?v=2\.0', 'theme-toggle.js?v=3.0'
        
        # Mettre à jour le titre
        $content = $content -replace 'ERP Universitaire', 'UniERP BF Premium'
        
        # Ajouter la structure logo si nécessaire
        if ($content -notmatch 'logo-ultra') {
            $content = $content -replace '<div class="sidebar-header">.*?</div>', @'
<div class="sidebar-header">
                <div class="logo-ultra">
                    <div class="logo-icon-ultra">🎓</div>
                    <div class="logo-text-ultra">
                        <div class="logo-name-ultra">UniERP BF</div>
                        <div class="logo-tag-ultra">Premium Edition</div>
                    </div>
                </div>
            </div>
'@
        }
        
        # Sauvegarder
        $content | Set-Content $dashboard -Encoding UTF8 -NoNewline
        
        Write-Host "✅ $dashboard mis à jour" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $dashboard introuvable" -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Standardisation terminée!" -ForegroundColor Green
Write-Host "Les dashboards utilisent maintenant le design moderne unifié." -ForegroundColor Cyan
