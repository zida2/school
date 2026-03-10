"""
Générateur de PDF pour les reçus de paiement et autres documents
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime


def generer_recu_paiement(paiement):
    """
    Génère un PDF de reçu de paiement
    
    Args:
        paiement: Instance du modèle Paiement
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les informations
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
    )
    
    # En-tête avec logo et infos université
    universite = paiement.etudiant.universite
    elements.append(Paragraph(universite.nom, title_style))
    elements.append(Paragraph(f"{universite.ville} - {universite.telephone}", 
                             ParagraphStyle('SubTitle', parent=styles['Normal'], 
                                          fontSize=10, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(Spacer(1, 1*cm))
    
    # Titre du document
    elements.append(Paragraph("REÇU DE PAIEMENT", 
                             ParagraphStyle('DocTitle', parent=styles['Heading1'],
                                          fontSize=18, alignment=TA_CENTER,
                                          textColor=colors.HexColor('#059669'),
                                          spaceAfter=20)))
    
    # Numéro de reçu
    elements.append(Paragraph(f"<b>N° {paiement.numero_recu}</b>", 
                             ParagraphStyle('ReceiptNo', parent=styles['Normal'],
                                          fontSize=12, alignment=TA_CENTER,
                                          spaceAfter=30)))
    
    # Informations étudiant
    etudiant_data = [
        ['INFORMATIONS ÉTUDIANT', ''],
        ['Matricule:', paiement.etudiant.matricule],
        ['Nom complet:', paiement.etudiant.get_full_name()],
        ['Filière:', paiement.etudiant.filiere.nom],
        ['Niveau:', paiement.etudiant.niveau],
        ['Année académique:', paiement.annee_academique.libelle],
    ]
    
    etudiant_table = Table(etudiant_data, colWidths=[5*cm, 10*cm])
    etudiant_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (-1, 0)),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(etudiant_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Détails du paiement
    paiement_data = [
        ['DÉTAILS DU PAIEMENT', ''],
        ['Montant payé:', f"{int(paiement.montant):,} FCFA".replace(',', ' ')],
        ['Mode de paiement:', paiement.get_mode_paiement_display()],
        ['Date de paiement:', paiement.date_paiement.strftime('%d/%m/%Y')],
        ['Statut:', paiement.get_statut_display()],
    ]
    
    if paiement.observation:
        paiement_data.append(['Observation:', paiement.observation])
    
    paiement_table = Table(paiement_data, colWidths=[5*cm, 10*cm])
    paiement_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dcfce7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (-1, 0)),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(paiement_table)
    elements.append(Spacer(1, 1*cm))
    
    # Solde restant
    frais_total = paiement.etudiant.filiere.frais_inscription
    montant_paye_total = paiement.etudiant.paiements.filter(statut='valide').aggregate(
        total=__import__('django.db.models', fromlist=['Sum']).Sum('montant')
    )['total'] or 0
    solde_restant = max(0, int(frais_total) - int(montant_paye_total))
    
    solde_data = [
        ['Frais de scolarité total:', f"{int(frais_total):,} FCFA".replace(',', ' ')],
        ['Total payé à ce jour:', f"{int(montant_paye_total):,} FCFA".replace(',', ' ')],
        ['Solde restant:', f"{solde_restant:,} FCFA".replace(',', ' ')],
    ]
    
    solde_table = Table(solde_data, colWidths=[8*cm, 7*cm])
    solde_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#dc2626') if solde_restant > 0 else colors.HexColor('#059669')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(solde_table)
    elements.append(Spacer(1, 1.5*cm))
    
    # Signature et cachet
    signature_data = [
        ['Enregistré par:', paiement.enregistre_par.get_full_name() if paiement.enregistre_par else 'Système'],
        ['Date d\'émission:', datetime.now().strftime('%d/%m/%Y à %H:%M')],
    ]
    
    signature_table = Table(signature_data, colWidths=[5*cm, 10*cm])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(signature_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Note de bas de page
    elements.append(Paragraph(
        "<i>Ce reçu est généré automatiquement et fait foi de paiement. "
        "Conservez-le précieusement pour toute réclamation.</i>",
        ParagraphStyle('Footer', parent=styles['Normal'],
                      fontSize=8, textColor=colors.grey,
                      alignment=TA_CENTER)
    ))
    
    # Construire le PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
