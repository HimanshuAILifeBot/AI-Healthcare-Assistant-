"""
Email Service Module
Handles sending emails with invoice attachments
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        """Initialize email service with configuration from environment"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.sender_name = os.getenv("SENDER_NAME", "AI Healthcare Services")
        
    def send_invoice_email(self, recipient_email, patient_name, invoice_pdf, 
                          appointment_data, doctor_data):
        """
        Send invoice email with PDF attachment
        
        Args:
            recipient_email: Patient's email address
            patient_name: Patient's name
            invoice_pdf: BytesIO object containing PDF
            appointment_data: Dict with appointment details
            doctor_data: Dict with doctor details
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Healthcare Invoice - Appointment with Dr. {doctor_data.get('doctor_name', 'Doctor')}"
            
            # Email body (HTML)
            html_body = self._generate_email_body(
                patient_name, 
                appointment_data, 
                doctor_data
            )
            
            # Attach HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Attach PDF invoice
            pdf_attachment = MIMEBase('application', 'pdf')
            pdf_attachment.set_payload(invoice_pdf.read())
            encoders.encode_base64(pdf_attachment)
            
            filename = f"Invoice_Appointment_{appointment_data.get('id', '0000')}.pdf"
            pdf_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename={filename}'
            )
            msg.attach(pdf_attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Invoice email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send invoice email: {e}")
            return False
    
    def _generate_email_body(self, patient_name, appointment_data, doctor_data):
        """Generate HTML email body"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    background: #f9fafb;
                    padding: 30px;
                    border: 1px solid #e5e7eb;
                }}
                .info-box {{
                    background: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-left: 4px solid #1e40af;
                    border-radius: 5px;
                }}
                .info-box h3 {{
                    margin-top: 0;
                    color: #1e40af;
                }}
                .detail-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                .detail-label {{
                    font-weight: bold;
                    color: #6b7280;
                }}
                .footer {{
                    background: #1f2937;
                    color: #9ca3af;
                    padding: 20px;
                    text-align: center;
                    border-radius: 0 0 10px 10px;
                    font-size: 12px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: #1e40af;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🩺 AI Healthcare Services</h1>
                    <p>Your Health, Our Priority</p>
                </div>
                
                <div class="content">
                    <h2>Dear {patient_name},</h2>
                    <p>Thank you for choosing AI Healthcare Services. Your appointment has been confirmed and your invoice is attached to this email.</p>
                    
                    <div class="info-box">
                        <h3>📅 Appointment Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Doctor:</span>
                            <span>Dr. {doctor_data.get('doctor_name', 'N/A')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Specialization:</span>
                            <span>{doctor_data.get('specialization', 'N/A')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Hospital:</span>
                            <span>{doctor_data.get('hospital_name', 'N/A')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Date:</span>
                            <span>{appointment_data.get('appointment_date', 'N/A')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Time:</span>
                            <span>{appointment_data.get('appointment_time', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <div class="info-box">
                        <h3>💳 Payment Information</h3>
                        <p>Your payment has been successfully processed.</p>
                        <div class="detail-row">
                            <span class="detail-label">Consultation Fee:</span>
                            <span>₹{doctor_data.get('fees', 500)}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span style="color: #059669; font-weight: bold;">✓ Paid</span>
                        </div>
                    </div>
                    
                    <p><strong>📎 Your detailed invoice is attached to this email as a PDF.</strong></p>
                    
                    <div style="text-align: center;">
                        <p>Need to reschedule or have questions?</p>
                        <p style="margin: 10px 0;">📧 support@aihealthcare.com</p>
                        <p style="margin: 10px 0;">📞 +1 (555) 123-4567</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>AI Healthcare Services</strong></p>
                    <p>Advanced Medical Care with AI Assistance</p>
                    <p style="margin-top: 15px;">
                        This is an automated email. Please do not reply directly to this message.
                    </p>
                    <p style="margin-top: 10px; font-size: 10px;">
                        © {datetime.now().year} AI Healthcare Services. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """


# Fallback function for testing without SMTP
def save_invoice_locally(invoice_pdf, filename):
    """Save invoice PDF locally for testing"""
    try:
        invoices_dir = "invoices"
        os.makedirs(invoices_dir, exist_ok=True)
        
        filepath = os.path.join(invoices_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(invoice_pdf.getvalue())
        
        logger.info(f"Invoice saved locally: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save invoice locally: {e}")
        return None
