"""
Invoice Generator Module
Generates PDF invoices for healthcare appointments
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import io
import os


def generate_invoice(appointment_data, patient_data, doctor_data):
    """
    Generate a professional PDF invoice for healthcare appointment
    
    Args:
        appointment_data: dict with appointment details
        patient_data: dict with patient information
        doctor_data: dict with doctor and hospital information
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Header - Company Info
    header_data = [
        [Paragraph("<b>AI HEALTHCARE SERVICES</b>", styles['Center'])],
        [Paragraph("Advanced Medical Care with AI Assistance", styles['Center'])],
        [Paragraph("contact@aihealthcare.com | +1 (555) 123-4567", styles['Center'])],
    ]
    
    header_table = Table(header_data, colWidths=[6*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white)
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice Title
    elements.append(Paragraph("<b>MEDICAL INVOICE</b>", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice Details
    invoice_number = f"INV-{appointment_data.get('id', '0000'):05d}"
    invoice_date = datetime.now().strftime("%B %d, %Y")
    
    invoice_info = [
        [Paragraph("<b>Invoice Number:</b>", styles['Normal']), invoice_number],
        [Paragraph("<b>Invoice Date:</b>", styles['Normal']), invoice_date],
        [Paragraph("<b>Appointment Date:</b>", styles['Normal']), 
         appointment_data.get('appointment_date', 'N/A')],
    ]
    
    invoice_table = Table(invoice_info, colWidths=[2*inch, 4*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(invoice_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Information Section
    patient_header = Paragraph("<b>PATIENT INFORMATION</b>", styles['Heading2'])
    elements.append(patient_header)
    elements.append(Spacer(1, 0.1*inch))
    
    patient_info = [
        [Paragraph("<b>Name:</b>", styles['Normal']), patient_data.get('name', 'N/A')],
        [Paragraph("<b>Medical Record #:</b>", styles['Normal']), 
         patient_data.get('medical_record_number', 'N/A')],
        [Paragraph("<b>Contact:</b>", styles['Normal']), 
         patient_data.get('contact_number', 'N/A')],
        [Paragraph("<b>Blood Group:</b>", styles['Normal']), 
         patient_data.get('blood_group', 'N/A')],
    ]
    
    patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Doctor/Service Information
    service_header = Paragraph("<b>SERVICE DETAILS</b>", styles['Heading2'])
    elements.append(service_header)
    elements.append(Spacer(1, 0.1*inch))
    
    service_info = [
        [Paragraph("<b>Doctor:</b>", styles['Normal']), 
         doctor_data.get('doctor_name', 'N/A')],
        [Paragraph("<b>Specialization:</b>", styles['Normal']), 
         doctor_data.get('specialization', 'N/A')],
        [Paragraph("<b>Hospital:</b>", styles['Normal']), 
         doctor_data.get('hospital_name', 'N/A')],
        [Paragraph("<b>Appointment Time:</b>", styles['Normal']), 
         appointment_data.get('appointment_time', 'N/A')],
        [Paragraph("<b>Reason for Visit:</b>", styles['Normal']), 
         appointment_data.get('reason', 'General Consultation')],
    ]
    
    service_table = Table(service_info, colWidths=[2*inch, 4*inch])
    service_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(service_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Billing Details
    billing_header = Paragraph("<b>BILLING DETAILS</b>", styles['Heading2'])
    elements.append(billing_header)
    elements.append(Spacer(1, 0.1*inch))
    
    consultation_fee = doctor_data.get('fees', 500)
    service_charge = 50
    subtotal = consultation_fee + service_charge
    tax = subtotal * 0.18  # 18% GST
    total = subtotal + tax
    
    billing_data = [
        [Paragraph("<b>Description</b>", styles['Normal']), 
         Paragraph("<b>Amount (₹)</b>", styles['Right'])],
        ['Consultation Fee', f"₹{consultation_fee:,.2f}"],
        ['Service Charge', f"₹{service_charge:,.2f}"],
        ['Subtotal', f"₹{subtotal:,.2f}"],
        ['GST (18%)', f"₹{tax:,.2f}"],
        [Paragraph("<b>Total Amount</b>", styles['Normal']), 
         Paragraph(f"<b>₹{total:,.2f}</b>", styles['Right'])],
    ]
    
    billing_table = Table(billing_data, colWidths=[4*inch, 2*inch])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1e40af')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(billing_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Payment Information
    payment_info = Paragraph(
        "<b>Payment Status:</b> Paid via Razorpay<br/>"
        "<b>Transaction ID:</b> " + appointment_data.get('transaction_id', 'RAZORPAY_' + str(appointment_data.get('id', '0000'))),
        styles['Normal']
    )
    elements.append(payment_info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    footer_text = [
        "Thank you for choosing AI Healthcare Services!",
        "For any queries, please contact us at support@aihealthcare.com",
        "This is a computer-generated invoice and does not require a signature."
    ]
    
    for text in footer_text:
        elements.append(Paragraph(text, footer_style))
        elements.append(Spacer(1, 0.05*inch))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_invoice_filename(appointment_id, patient_name):
    """Generate a standardized filename for the invoice"""
    date_str = datetime.now().strftime("%Y%m%d")
    safe_name = "".join(c for c in patient_name if c.isalnum() or c.isspace()).replace(" ", "_")
    return f"Invoice_{safe_name}_{appointment_id}_{date_str}.pdf"
