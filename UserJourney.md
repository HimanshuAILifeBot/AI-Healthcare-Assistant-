# Healthcare Voice Agent: User Journey Documentation

## Overview
This document describes the user journey for the Healthcare Voice Agent application, detailing each step a user takes from initial interaction to completion of core tasks. The application is designed to streamline healthcare interactions using a voice-enabled AI agent, integrating a modern web frontend, FastAPI backend, PostgreSQL database, and advanced LLMs (Gemini 2.0 Flash).

---

## 1. Entry Point: Landing & Login
- **Landing Page:**
  - Users arrive at a visually appealing login page with branding, avatar, and social login options (Google, Apple).
  - The page provides a clear call-to-action to log in or sign up.
- **Authentication:**
  - Users can log in using email/password or via social login.
  - Credentials are sent to the backend `/login` endpoint.
  - Backend validates credentials using the `sp_login_user` stored procedure in PostgreSQL.
  - On success, user context is established in the frontend; on failure, an error message is shown.

---

## 2. Dashboard & Navigation
- **Dashboard:**
  - After login, users are redirected to the dashboard.
  - The dashboard displays personalized information (e.g., name, upcoming appointments, health summary).
  - Navigation options allow users to access medical history, book appointments, interact with the AI assistant, and view recommendations.

---

## 3. Core Interactions
### a. Medical History
- **Accessing Medical History:**
  - Users select the medical history option.
  - Frontend sends a request to `/medical-history` with the user ID.
  - Backend retrieves data using `sp_get_medical_history` stored procedure.
  - Medical history is displayed in a user-friendly format.

### b. Appointment Booking
- **Booking an Appointment:**
  - Users choose to book an appointment.
  - The system guides them through selecting a specialist, date, and time.
  - Available doctors are fetched via `/get-doctors-by-specialists` (using `sp_get_doctors_by_specialists`).
  - Appointment details are submitted to `/appointments`, which invokes `sp_create_appointment`.
  - Confirmation is shown, and the appointment appears in the dashboard.

### c. AI Assistant Interaction
- **Voice/Text Assistant:**
  - Users interact with the AI assistant via voice or text input.
  - Queries are sent to `/run_langgraph`, which orchestrates LLM calls (Gemini 2.0 Flash) for natural language understanding and response.
  - The assistant can answer health questions, provide recommendations, and help with navigation.

---

## 4. Data Normalization & Recommendations
- **Normalization:**
  - Users can submit health data for normalization via `/normalize`.
  - The backend processes and standardizes the data for further analysis.
- **Recommendations:**
  - Personalized health recommendations are displayed based on user data and AI analysis.

---

## 5. Logout & Session Management
- **Logout:**
  - Users can log out at any time, ending their session and clearing sensitive data from the frontend context.

---

## 6. Error Handling & Feedback
- **Error States:**
  - Invalid login, failed API calls, or database errors are handled gracefully with clear feedback.
- **User Feedback:**
  - Users can provide feedback on their experience, which is sent to the backend for analysis.

---

## 7. Security & Privacy
- **Data Protection:**
  - All sensitive data is transmitted securely.
  - User sessions are managed with proper authentication and authorization.
  - Health data is stored and accessed in compliance with privacy standards.

---

## 8. End-to-End Flow Example
1. User lands on login page and authenticates.
2. Redirected to dashboard; sees health summary and options.
3. Books an appointment with a specialist.
4. Interacts with AI assistant for health advice.
5. Views medical history and recommendations.
6. Logs out securely.

---

## 9. Technical Touchpoints
- **Frontend:** React (App.jsx, Dashboard.jsx, Assistant.jsx, etc.)
- **Backend:** FastAPI (main.py, langgraph_llm_agents.py)
- **Database:** PostgreSQL (schema.sql, stored procedures)
- **AI:** Gemini 2.0 Flash via LangGraph workflow

---

## 10. Future Enhancements
- Voice biometrics for authentication
- Real-time notifications
- Integration with external health APIs

---

## Conclusion
This user journey ensures a seamless, secure, and intelligent healthcare experience, leveraging modern web technologies and AI to empower users in managing their health.
