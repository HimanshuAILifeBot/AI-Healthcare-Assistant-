# Architecture Diagram for New Features

## Feature 1: Voice Biometrics Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    User Starts Voice Chat                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend: fetchUserName()                                   │
│  GET /patient/{user_id}                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend: Query Database                                     │
│  SELECT name FROM patients WHERE user_id = ?                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Return: {"name": "John Doe"}                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Greeting: "Hello John! I'm your AI Health Assistant"   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  User Speaks: "I have a headache"                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Language Detection                                          │
│  Detect if Hindi (Unicode) or English                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Generate Acknowledgment                                     │
│  English: "I understand" / Hindi: "समझ गया"                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Speak Acknowledgment → Continue Conversation               │
└─────────────────────────────────────────────────────────────┘
```

---

## Feature 2: Invoice Generation & Email Flow

```
┌─────────────────────────────────────────────────────────────┐
│              User Books Appointment                          │
│              POST /appointments                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Create Appointment in Database                             │
│  INSERT INTO appointments (...)                             │
│  RETURNS appointment_id                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Async: generate_and_send_invoice()                        │
│  (Runs in background, doesn't block response)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌──────────────────┐      ┌─────────────────────┐
│ Fetch Patient    │      │ Fetch Doctor        │
│ Details          │      │ Details             │
│ - Name           │      │ - Name              │
│ - Email          │      │ - Specialization    │
│ - MRN            │      │ - Hospital          │
│ - Blood Group    │      │ - Fees              │
└────────┬─────────┘      └──────────┬──────────┘
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  invoice_generator.py                                        │
│  generate_invoice()                                          │
│  ├─ Create PDF document                                     │
│  ├─ Add header with branding                                │
│  ├─ Add patient information table                           │
│  ├─ Add doctor/service details                              │
│  ├─ Add billing breakdown                                   │
│  └─ Add footer with legal text                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  PDF Generated (BytesIO buffer)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Check Email Configuration                                   │
│  If SENDER_EMAIL exists → Send Email                        │
│  Else → Save Locally                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌──────────────────┐      ┌─────────────────────┐
│ email_service.py │      │ Save to             │
│ send_invoice()   │      │ backend/invoices/   │
│ ├─ HTML email    │      │ Invoice_Name_ID.pdf │
│ ├─ Attach PDF    │      └─────────────────────┘
│ └─ SMTP send     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Email Delivered          │
│ ✅ Patient receives:     │
│    - Appointment details │
│    - Payment info        │
│    - PDF invoice         │
└──────────────────────────┘
```

---

## Feature 3: Insurance Portal Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User in Dashboard                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Click "View Insurance" Button                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  React Router: navigate("/insurance")                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Insurance.jsx Component Loads                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Render Insurance Page                                       │
│  ├─ Navigation Bar                                          │
│  ├─ Hero Section (stats, intro)                            │
│  ├─ Insurance Plans Grid                                   │
│  │   ├─ Basic Health Shield                                │
│  │   ├─ Premium Health Plus (Popular)                      │
│  │   └─ Elite Care Supreme                                 │
│  ├─ Benefits Section                                        │
│  └─ Footer                                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  User Interaction                                            │
│  onClick: setSelectedPlan(planId)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌──────────────────┐      ┌─────────────────────┐
│ Plan Selected    │      │ View Terms Clicked  │
│ - Card highlights│      │ - Modal opens       │
│ - Button changes │      │ - Show T&C          │
│ - Actions appear │      │ - User can accept   │
└──────────────────┘      └─────────────────────┘
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Future: Proceed to Purchase                                │
│  (Can integrate real insurance API here)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     USER ACTIONS                              │
└───────────┬──────────────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌─────────┐    ┌──────────┐
│ Voice   │    │Insurance │
│Assistant│    │Portal    │
└────┬────┘    └────┬─────┘
     │              │
     ▼              │
┌─────────────┐    │
│Fetch Patient│    │
│Name & Greet │    │
└─────────────┘    │
                   │
     ▼              ▼
┌─────────────────────┐
│  Book Appointment   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Generate Invoice    │
│ (Async/Background)  │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐  ┌──────────┐
│Generate │  │  Send    │
│  PDF    │  │  Email   │
└─────────┘  └──────────┘
     │           │
     └─────┬─────┘
           │
           ▼
┌─────────────────────┐
│  Patient Receives   │
│  Invoice            │
└─────────────────────┘
```

---

## System Component Integration

```
┌────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  Assistant   │  │  Dashboard   │  │   Insurance     │ │
│  │  Component   │  │  Component   │  │   Component     │ │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘ │
│         │                  │                    │          │
└─────────┼──────────────────┼────────────────────┼──────────┘
          │                  │                    │
          ▼                  ▼                    ▼
┌────────────────────────────────────────────────────────────┐
│                   API LAYER (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │GET /patient/ │  │POST /appoint │  │  (Future: GET   │ │
│  │   {user_id}  │  │    ments     │  │  /insurance)    │ │
│  └──────┬───────┘  └──────┬───────┘  └─────────────────┘ │
└─────────┼──────────────────┼────────────────────────────────┘
          │                  │
          ▼                  ▼
┌────────────────────────────────────────────────────────────┐
│               BUSINESS LOGIC LAYER                          │
│  ┌──────────────┐  ┌─────────────────────────────────┐   │
│  │Query Patient │  │  generate_and_send_invoice()     │   │
│  │  Database    │  │  ├─ invoice_generator.py         │   │
│  └──────────────┘  │  └─ email_service.py             │   │
│                     └─────────────────────────────────┘   │
└───────────┬────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────────┐
│                 DATA LAYER                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  PostgreSQL  │  │  File System │  │  SMTP Server    │ │
│  │  (Patients,  │  │  (PDF        │  │  (Gmail)        │ │
│  │   Doctors)   │  │   Invoices)  │  │                 │ │
│  └──────────────┘  └──────────────┘  └─────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Integration

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND STACK                           │
│  React 19.0 + React Router + Context API                   │
│  ├─ UserContext (Voice + State Management)                 │
│  ├─ Insurance Component (New)                               │
│  └─ Dashboard Integration                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND STACK                            │
│  FastAPI + Python 3.12                                      │
│  ├─ Async/Await for invoice generation                     │
│  ├─ ReportLab for PDF creation                              │
│  ├─ SMTP for email sending                                  │
│  └─ PostgreSQL for data                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│  ├─ Gmail SMTP (Email Delivery)                            │
│  ├─ Azure TTS (Voice Synthesis)                             │
│  ├─ Gemini AI (Symptom Analysis)                            │
│  └─ (Future: Insurance API)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Recommended)

```
┌────────────────────────────────────────────────────────────┐
│                         USERS                               │
└───────────┬────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER                            │
│                    (nginx/CloudFlare)                       │
└───────────┬────────────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌─────────┐    ┌──────────┐
│Frontend │    │ Backend  │
│(Vercel/ │    │(AWS/     │
│ Netlify)│    │ Railway) │
└─────────┘    └────┬─────┘
                    │
            ┌───────┴────────┐
            │                │
            ▼                ▼
    ┌──────────┐      ┌──────────┐
    │PostgreSQL│      │  Email   │
    │(Supabase)│      │  Service │
    └──────────┘      │ (Gmail)  │
                       └──────────┘
                            │
                            ▼
                      ┌──────────┐
                      │Patient's │
                      │  Inbox   │
                      └──────────┘
```

---

This architecture demonstrates:
- ✅ Clear separation of concerns
- ✅ Async/background processing
- ✅ Scalable design
- ✅ Modern tech stack
- ✅ Professional implementation
