// =====================================================
//  ERP UNIVERSITAIRE - UTILITAIRES PARTAGÉS
// =====================================================

// === TOAST NOTIFICATIONS ===
function showToast(msg, type = 'info', duration = 3500) {
  const icons = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' };
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.style.cssText = `background:#fff;border-radius:12px;padding:14px 18px;box-shadow:0 8px 32px rgba(0,0,0,0.15);
    display:flex;align-items:center;gap:12px;min-width:280px;max-width:360px;
    border-left:4px solid ${type === 'success' ? '#059669' : type === 'danger' ? '#dc2626' : type === 'warning' ? '#d97706' : '#2563a8'};
    animation:slideIn .3s ease;font-family:'Inter',sans-serif;`;
  toast.innerHTML = `<span style="font-size:20px">${icons[type] || 'ℹ️'}</span>
    <span style="font-size:14px;font-weight:500;flex:1;color:#0f2338">${msg}</span>
    <span onclick="this.parentElement.remove()" style="cursor:pointer;font-size:16px;color:#94a3b8">✕</span>`;
  container.appendChild(toast);
  setTimeout(() => { if (toast.parentElement) toast.remove(); }, duration);
}

// === MODAL HELPERS ===
function openModal(id) {
  const m = document.getElementById(id);
  if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) { m.classList.remove('open'); document.body.style.overflow = ''; }
}

// Close modal on overlay click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
    document.body.style.overflow = '';
  }
});

// === TABS ===
function switchTab(tabGroup, tabId) {
  document.querySelectorAll(`[data-tab-group="${tabGroup}"]`).forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll(`[data-tab-content="${tabGroup}"]`).forEach(pane => pane.classList.remove('active'));
  const btn = document.querySelector(`[data-tab-group="${tabGroup}"][data-tab="${tabId}"]`);
  const pane = document.querySelector(`[data-tab-content="${tabGroup}"][data-tab="${tabId}"]`);
  if (btn) btn.classList.add('active');
  if (pane) pane.classList.add('active');
}

// === DATE HELPERS ===
function formatDate(d) {
  if (!d) return '—';
  const dt = new Date(d);
  return dt.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}
function formatDateTime(d) {
  if (!d) return '—';
  const dt = new Date(d);
  return dt.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}
function currentYear() { return new Date().getFullYear(); }

// === GRADE BADGE ===
function noteBadge(note) {
  const n = parseFloat(note);
  if (isNaN(n)) return `<span class="badge badge-muted">—</span>`;
  if (n >= 16) return `<span class="note-chip excellent">${n.toFixed(2)}</span>`;
  if (n >= 12) return `<span class="note-chip bien">${n.toFixed(2)}</span>`;
  if (n >= 10) return `<span class="note-chip passable">${n.toFixed(2)}</span>`;
  return `<span class="note-chip echec">${n.toFixed(2)}</span>`;
}

// === SEARCH TABLE ===
function filterTable(inputId, tableId) {
  const q = document.getElementById(inputId).value.toLowerCase();
  document.querySelectorAll(`#${tableId} tbody tr`).forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}

// === EXPORT CSV ===
function exportTableCSV(tableId, filename = 'export.csv') {
  const table = document.getElementById(tableId);
  if (!table) { showToast('Tableau introuvable', 'danger'); return; }
  let csv = [];
  table.querySelectorAll('tr').forEach(row => {
    const cells = [...row.querySelectorAll('th, td')].map(c => `"${c.textContent.trim().replace(/"/g, '""')}"`);
    csv.push(cells.join(','));
  });
  const blob = new Blob(['\uFEFF' + csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  showToast(`Export ${filename} réussi !`, 'success');
}

// === PRINT ===
function printSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (!section) return;
  const w = window.open('', '_blank');
  w.document.write(`<!DOCTYPE html><html><head><meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>body{font-family:'Inter',sans-serif;padding:20px;color:#0f2338;}table{width:100%;border-collapse:collapse;}
    th,td{border:1px solid #e2e8f0;padding:8px 12px;font-size:13px;}th{background:#f0f4f8;font-weight:600;}
    h1,h2{font-family:'Outfit',sans-serif;}</style></head><body>${section.innerHTML}</body></html>`);
  w.document.close();
  w.print();
}

// === CONFIRM DIALOG ===
function confirmAction(msg, callback) {
  if (window.confirm(msg)) callback();
}

// === CURRENCY FORMAT ===
function formatCFA(amount) {
  return new Intl.NumberFormat('fr-FR').format(amount) + ' FCFA';
}

// === NAVIGATION ACTIVE ===
function setActiveNav(page) {
  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.dataset.page === page) item.classList.add('active');
    else item.classList.remove('active');
  });
}

// === SIDEBAR TOGGLE ===
function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// === LOGOUT ===
function logout() {
  if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
    if (typeof API !== 'undefined' && API.logout) {
      API.logout();
    } else {
      localStorage.removeItem('erp_access_token');
      localStorage.removeItem('erp_refresh_token');
      localStorage.removeItem('erp_user');
      window.location.href = 'index.html';
    }
  }
}

// === PAGE SHOW/HIDE ===
function showPage(pageId) {
  document.querySelectorAll('.erp-page').forEach(p => p.style.display = 'none');
  const page = document.getElementById(pageId);
  if (page) { page.style.display = 'block'; page.style.animation = 'fadeIn .25s ease'; }
}

// Keyframe injection
const styleKF = document.createElement('style');
styleKF.textContent = `
  @keyframes slideIn { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
  @keyframes fadeIn { from{opacity:0} to{opacity:1} }
`;
document.head.appendChild(styleKF);
