# Testing Guide for New Features

## Quick Start Testing

### Prerequisites
1. Backend server running: `uvicorn main:app --reload`
2. Frontend server running: `npm run dev`
3. User logged in with valid credentials
4. Database populated with sample data

---

## Feature 1: Voice Biometrics & Natural Acknowledgments

### Test Steps:
1. **Login** to the application
2. Navigate to **Dashboard**
3. Click **"Talk to AI Assistant"** button
4. Click **"Start Voice Chat"**
5. **Wait 2-3 seconds** for the system to fetch your name
6. Observe the greeting (should include your name)

### Expected Results:
- ✅ Greeting includes your name
- ✅ Format: "Hello [YourName]!" or "नमस्ते [YourName]!"
- ✅ Language matches your first input

### Test Natural Acknowledgments:
1. Speak: **"I have a headache"** (English)
2. Wait for response
3. Speak: **"I also have fever"**
4. Listen for acknowledgment: "I understand" / "Got it" / etc.

5. For Hindi test:
   - Speak: **"मुझे सिर दर्द है"**
   - Wait for response
   - Speak: **"और बुखार भी है"**
   - Listen for acknowledgment: "समझ गया" / "ठीक है" / etc.

### Troubleshooting:
- If no greeting: Check browser console for errors
- If no name: Verify `/patient/{user_id}` endpoint works
- If no acknowledgments: Check symptom count > 1

---

## Feature 2: Invoice Generation & Email Delivery

### Setup Email (Optional):
```bash
# Edit .env file in backend folder
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=AI Healthcare Services
```

### Test Invoice Generation:
1. **Complete symptom analysis** in Assistant
2. Select a **recommended doctor**
3. Click **"Book Appointment"**
4. Confirm booking

### Expected Results:
✅ **If Email Configured:**
- Appointment created successfully
- Email sent to your registered email
- Check inbox for "Healthcare Invoice" email
- Email contains:
  - Appointment details
  - Payment information
  - PDF invoice attachment
  
✅ **If Email Not Configured:**
- Appointment created successfully
- Invoice saved locally
- Check `backend/invoices/` folder
- File format: `Invoice_[Name]_[ID]_[Date].pdf`

### Verify Invoice Contents:
Open the PDF and check:
- [ ] Patient name and details
- [ ] Medical record number
- [ ] Doctor name and specialization
- [ ] Hospital name
- [ ] Appointment date and time
- [ ] Billing breakdown (consultation fee, service charge, GST, total)
- [ ] Transaction ID
- [ ] Professional branding and footer

### Test Email Template:
1. Open the email
2. Verify HTML rendering
3. Check all appointment details visible
4. Verify PDF attachment is present
5. Download and open PDF

### Troubleshooting:
- **Email not received:**
  - Check spam folder
  - Verify `.env` credentials
  - Check backend logs for errors
  - Verify `SENDER_EMAIL` matches Gmail account
  
- **PDF not generated:**
  - Check `backend/invoices/` folder exists
  - Verify reportlab is installed: `pip list | grep reportlab`
  - Check backend logs for errors

- **Invoice missing data:**
  - Verify database has complete patient/doctor data
  - Check appointment creation was successful

---

## Feature 3: Insurance Integration

### Test Insurance Portal:
1. Navigate to **Dashboard**
2. Click **"View Insurance"** button (green shield icon)
3. Should redirect to `/insurance` route

### Verify Insurance Page Elements:
- [ ] Header with logo and navigation
- [ ] Hero section with statistics
- [ ] Three insurance plans displayed
- [ ] Plan details visible (price, coverage, features)
- [ ] "Most Popular" badge on Premium plan
- [ ] Interactive plan selection

### Test Plan Selection:
1. Click **"Select Plan"** on any plan card
2. Card should highlight with green border
3. Button text changes to **"Selected ✓"**
4. Action buttons appear below:
   - "View Terms & Conditions"
   - "Proceed to Purchase"

### Test Terms & Conditions:
1. Click **"View Terms & Conditions"**
2. Modal should open with full overlay
3. Verify modal contents:
   - [ ] Coverage details
   - [ ] Waiting periods
   - [ ] Exclusions list
   - [ ] Claim process
   - [ ] Renewal terms
   - [ ] Cancellation policy
   - [ ] Data privacy
   - [ ] Customer responsibilities
4. Click **"I Accept"** button
5. Modal should close

### Test Responsiveness:
1. Resize browser window
2. Test on mobile viewport (DevTools)
3. Verify:
   - [ ] Plans stack vertically on mobile
   - [ ] Navigation adapts
   - [ ] Modal fits screen
   - [ ] All buttons accessible

### Test Benefits Section:
Scroll down to verify:
- [ ] "Why Choose SecureHealth?" section
- [ ] Four benefit cards displayed
- [ ] Icons and descriptions visible
- [ ] Hover effects work

### Test Footer:
Verify footer contains:
- [ ] About Us section
- [ ] Quick Links
- [ ] Contact information
- [ ] Regulatory information
- [ ] Copyright notice
- [ ] Disclaimer text

### Troubleshooting:
- **Insurance page not loading:**
  - Check route added in `Root.jsx`
  - Verify `Insurance.jsx` imported correctly
  - Check browser console for errors
  
- **Styles not applying:**
  - Verify `Insurance.css` imported in component
  - Clear browser cache
  - Check for CSS syntax errors
  
- **Button not visible on Dashboard:**
  - Check Dashboard.jsx changes saved
  - Verify inline styles applied
  - Restart dev server

---

## Complete User Journey Test

### Full Flow Test (30 minutes):
1. **Login** → Dashboard
2. **View Insurance** → Browse plans → Select plan → View terms → Back to Dashboard
3. **Talk to AI Assistant** → Start voice chat → Get personalized greeting
4. **Describe symptoms** → Hear natural acknowledgments → Complete triage
5. **View recommendations** → Select doctor → Book appointment
6. **Check email** → Receive invoice → Download PDF
7. **Verify invoice** → All details correct

### Expected Success Indicators:
- ✅ Personalized voice greeting with name
- ✅ Natural acknowledgments during conversation
- ✅ Smooth insurance portal experience
- ✅ Appointment booking successful
- ✅ Invoice received via email (if configured)
- ✅ Invoice PDF generated and complete
- ✅ All navigation works smoothly

---

## API Testing (Optional)

### Test Backend Endpoints:

**1. Get Patient Name:**
```bash
curl http://localhost:8000/patient/1
# Expected: {"name": "Patient Name"}
```

**2. Create Appointment (triggers invoice):**
```bash
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "slot_id": 1,
    "reason": "Regular checkup"
  }'
# Expected: {"message": "Appointment created and invoice sent", "appointment_id": X}
```

**3. Check Invoice Generation:**
```bash
# Check if invoice file was created
ls -la backend/invoices/
# Should show PDF files with recent timestamps
```

---

## Performance Testing

### Load Test Invoice Generation:
```python
# Create test_invoice.py
from invoice_generator import generate_invoice
import time

appointment_data = {
    'id': 1,
    'appointment_date': '2025-10-10',
    'appointment_time': '10:00 AM',
    'reason': 'General Consultation',
    'transaction_id': 'TEST123'
}

patient_data = {
    'name': 'Test Patient',
    'contact_number': '1234567890',
    'medical_record_number': 'MRN001',
    'blood_group': 'O+',
    'email': 'test@example.com'
}

doctor_data = {
    'doctor_name': 'Dr. Smith',
    'specialization': 'General Medicine',
    'hospital_name': 'City Hospital',
    'fees': 500
}

start = time.time()
pdf = generate_invoice(appointment_data, patient_data, doctor_data)
end = time.time()

print(f"Invoice generated in {end-start:.2f} seconds")
print(f"PDF size: {len(pdf.getvalue())} bytes")
```

Run: `python test_invoice.py`

---

## Browser Compatibility Testing

Test on multiple browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (if on Windows)

Features to verify:
- [ ] Voice recognition works
- [ ] Audio playback works
- [ ] CSS animations smooth
- [ ] Modals display correctly
- [ ] PDF downloads work
- [ ] Email links work

---

## Accessibility Testing

1. **Keyboard Navigation:**
   - Tab through all interactive elements
   - Enter/Space should activate buttons
   - Escape should close modals

2. **Screen Reader:**
   - Test with browser screen reader
   - Verify all content is readable
   - Check button labels are clear

3. **Color Contrast:**
   - Verify text is readable
   - Check buttons have sufficient contrast
   - Test in high contrast mode

---

## Security Testing

1. **Email Credentials:**
   - Verify `.env` not committed to git
   - Check credentials not exposed in logs
   - Test with invalid credentials (should fail gracefully)

2. **SQL Injection:**
   - Try entering special characters in symptoms
   - Verify parameterized queries used

3. **XSS Prevention:**
   - Try entering `<script>alert('XSS')</script>` in voice input
   - Verify proper sanitization

---

## Demo Preparation

### Before Showcasing:
1. ✅ Populate database with sample data
2. ✅ Create test user account
3. ✅ Configure email (optional but impressive)
4. ✅ Clear browser cache
5. ✅ Close unnecessary browser tabs
6. ✅ Prepare backup slides/screenshots
7. ✅ Test microphone permissions
8. ✅ Have sample symptoms ready
9. ✅ Know which doctor to book
10. ✅ Have email open to show invoice

### Demo Script:
1. **Start (2 min):** "Today I'll show you three major enhancements..."
2. **Voice Feature (5 min):** Login → Assistant → Show greeting → Acknowledgments
3. **Invoice (5 min):** Book appointment → Show email → Open PDF
4. **Insurance (3 min):** Navigate portal → Select plan → Show terms
5. **Q&A (5 min):** Answer questions

---

## Troubleshooting Common Issues

### Issue: "Voice greeting not working"
**Solution:**
- Check browser console for errors
- Verify `/patient/{user_id}` endpoint returns data
- Clear localStorage and re-login
- Check network tab for failed requests

### Issue: "Invoice not generated"
**Solution:**
- Verify reportlab installed: `pip list | grep reportlab`
- Check backend logs for Python errors
- Ensure `invoices/` directory exists
- Test with simple data first

### Issue: "Email not sending"
**Solution:**
- Verify Gmail app password (not regular password)
- Check 2-factor auth enabled
- Test SMTP connection separately
- Check firewall/antivirus blocking port 587

### Issue: "Insurance page blank"
**Solution:**
- Check browser console
- Verify CSS file imported
- Clear cache and hard reload (Cmd+Shift+R)
- Check React DevTools for errors

---

## Success Criteria

### ✅ Feature is Working If:

**Voice Biometrics:**
- [ ] User name appears in greeting
- [ ] Language detection works
- [ ] Acknowledgments play after each symptom
- [ ] Voice feels natural and conversational

**Invoice System:**
- [ ] PDF generates without errors
- [ ] Email delivers to inbox (if configured)
- [ ] All patient/doctor data correct
- [ ] Billing calculations accurate
- [ ] Professional appearance

**Insurance Portal:**
- [ ] All three plans visible
- [ ] Selection interaction works
- [ ] Terms modal opens/closes
- [ ] Responsive on mobile
- [ ] Navigation works
- [ ] No console errors

---

## Next Steps After Testing

1. ✅ Document any bugs found
2. ✅ Create GitHub issues for improvements
3. ✅ Update README with new features
4. ✅ Add screenshots to documentation
5. ✅ Record demo video
6. ✅ Prepare presentation slides
7. ✅ Get feedback from users
8. ✅ Plan next enhancements

---

**Happy Testing! 🎉**

For issues or questions, check:
- `NEW_FEATURES_GUIDE.md` for detailed documentation
- Backend logs: `backend/uvicorn.log`
- Browser console for frontend errors
- Network tab for API call failures
