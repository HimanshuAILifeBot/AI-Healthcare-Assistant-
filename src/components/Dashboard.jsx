import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Dashboard.css";
import logo from "../assets/logo-01.jpg";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const PatientDashboard = () => {
  const [patient, setPatient] = useState(null);
  const [history, setHistory] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [error, setError] = useState(null);
  const [openDropdown, setOpenDropdown] = useState(null);
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    if (!userId) {
      navigate("/");
      return;
    }

    fetch(`${BACKEND_URL}/patient-details/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch patient details");
        return res.json();
      })
      .then((data) => setPatient(data))
      .catch((err) => setError(err.message));

    fetch(`${BACKEND_URL}/medical-history/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch medical history");
        return res.json();
      })
      .then((data) => setHistory(data))
      .catch((err) => setError(err.message));

    fetch(`${BACKEND_URL}/appointments/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch appointments");
        return res.json();
      })
      .then((data) => {
        // Sort appointments by id in descending order (last booked first)
        const sortedAppointments = (data.appointments || []).sort((a, b) => {
          return b.id - a.id;
        });
        setAppointments(sortedAppointments);
      })
      .catch((err) => console.log("No appointments found:", err.message));
  }, [navigate, userId]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (openDropdown && !event.target.closest('.appointment-actions')) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [openDropdown]);

  // Toggle dropdown menu
  const toggleDropdown = (appointmentId) => {
    setOpenDropdown(openDropdown === appointmentId ? null : appointmentId);
  };

  // Delete appointment
  const handleDeleteAppointment = async (appointmentId) => {
    if (!window.confirm("Are you sure you want to delete this appointment?")) {
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/appointments/${appointmentId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete appointment");
      }

      // Remove the appointment from state
      setAppointments(appointments.filter(apt => apt.id !== appointmentId));
      setOpenDropdown(null);
      alert("Appointment deleted successfully!");
    } catch (err) {
      console.error("Error deleting appointment:", err);
      alert("Failed to delete appointment. Please try again.");
    }
  };

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="error-container">
          <div className="error-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
          </div>
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <button 
            className="retry-button"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!patient || !history) {
    return (
      <div className="dashboard-page">
        <div className="loading-container">
          <div className="loading-spinner">
            <div className="spinner"></div>
          </div>
          <h2>Loading your health data...</h2>
          <p>Please wait while we fetch your information</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
        <div className="gradient-orb orb-4"></div>
        <div className="floating-particles">
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
        </div>
      </div>
      
      {/* Navigation Bar */}
      <nav className="dashboard-nav">
        <div className="nav-container">
          <div className="nav-logo">
            <div className="logo-icon">
              <img src={logo} alt="AI LifeBot" style={{ width: '120px', height: 'auto' }} />
            </div>
          </div>
          <div className="nav-actions">
            <button 
              className="theme-toggle-button"
              onClick={toggleTheme}
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="5"/>
                  <line x1="12" y1="1" x2="12" y2="3"/>
                  <line x1="12" y1="21" x2="12" y2="23"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                  <line x1="1" y1="12" x2="3" y2="12"/>
                  <line x1="21" y1="12" x2="23" y2="12"/>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
              )}
            </button>
            <button 
              className="logout-button"
              onClick={() => {
                localStorage.removeItem("user_id");
                navigate("/");
              }}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16,17 21,12 16,7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              Sign Out
            </button>
          </div>
        </div>
      </nav>
      
      <header className="dashboard-header">
        <div className="header-content">
          <div className="welcome-section">
            <div className="user-avatar">
              {patient.name.charAt(0).toUpperCase()}
            </div>
            <div className="welcome-text">
              <h1>Welcome back, <span className="gradient-text">{patient.name}</span></h1>
              <p>Here's your comprehensive health overview</p>
            </div>
          </div>
          <div className="header-actions">
            <button
              className="assistant-button"
              onClick={() => navigate("/assistant")}
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="m12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
              Talk to AI Assistant
            </button>
          </div>
        </div>
      </header>

      {/* Quick Actions Section */}
      <div className="quick-actions-section">
        <div className="quick-actions-container">
          <h3 className="quick-actions-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12,6 12,12 16,14"/>
            </svg>
            Quick Actions
          </h3>
          <div className="quick-actions-grid">
            <button className="action-card insurance-card" onClick={() => navigate("/insurance")}>
              <div className="action-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  <path d="M9 12l2 2 4-4"/>
                </svg>
              </div>
              <div className="action-content">
                <h4>Health Insurance</h4>
                <p>View plans & coverage options</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12,5 19,12 12,19"/>
                </svg>
              </div>
            </button>

            <button className="action-card appointments-action-card" onClick={() => navigate("/assistant")}>
              <div className="action-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <div className="action-content">
                <h4>Book Appointment</h4>
                <p>Schedule with AI assistance</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12,5 19,12 12,19"/>
                </svg>
              </div>
            </button>

            <button className="action-card records-card" onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}>
              <div className="action-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <div className="action-content">
                <h4>Medical Records</h4>
                <p>View your health history</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12,5 19,12 12,19"/>
                </svg>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-grid">
        <div className="dashboard-card patient-info-card">
          <div className="card-header">
            <div className="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <h2>Patient Information</h2>
          </div>
          <div className="info-grid">
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                Date of Birth
              </div>
              <span className="info-value">{patient.date_of_birth}</span>
            </div>
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
                </svg>
                Gender
              </div>
              <span className="info-value">{patient.gender}</span>
            </div>
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                </svg>
                Contact
              </div>
              <span className="info-value">{patient.contact_number}</span>
            </div>
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
                Medical Record #
              </div>
              <span className="info-value">{patient.medical_record_number}</span>
            </div>
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2z"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                Blood Group
              </div>
              <span className="info-value blood-group">{patient.blood_group}</span>
            </div>
            <div className="info-item">
              <div className="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
                Marital Status
              </div>
              <span className="info-value">{patient.marital_status}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card medical-history-card">
          <div className="card-header">
            <div className="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7z"/>
              </svg>
            </div>
            <h2>Medical History</h2>
          </div>
          <div className="medical-history-grid">
            <div className="history-item diagnosis">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
                Past Diagnoses
              </div>
              <div className="history-value">{history.past_diagnoses || 'No diagnoses recorded'}</div>
            </div>
            
            <div className="history-item surgery">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4.037 4.688a.495.495 0 01.651-.651l6.015 2.48c.237.1.237.4 0 .5l-6.015 2.48a.495.495 0 01-.651-.651L5.5 6.8z"/>
                  <path d="M16 12l3-3 3 3-3 3z"/>
                </svg>
                Surgeries
              </div>
              <div className="history-value">{history.surgeries || 'No surgeries recorded'}</div>
            </div>
            
            <div className="history-item admission">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2z"/>
                  <path d="M8 21v-4a2 2 0 012-2h4a2 2 0 012 2v4"/>
                </svg>
                Hospital Admissions
              </div>
              <div className="history-value">{history.hospital_admissions || 'No admissions recorded'}</div>
            </div>
            
            <div className="history-item immunization">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
                Immunizations
              </div>
              <div className="history-value">{history.immunization_records || 'No immunizations recorded'}</div>
            </div>
            
            <div className="history-item family">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/>
                </svg>
                Family History
              </div>
              <div className="history-value">{history.family_medical_history || 'No family history recorded'}</div>
            </div>
            
            <div className="history-item lifestyle">
              <div className="history-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
                Lifestyle Factors
              </div>
              <div className="history-value">{history.lifestyle_factors || 'No lifestyle factors recorded'}</div>
            </div>
          </div>
        </div>

        {/* Appointments Section */}
        <div className="dashboard-card appointments-card">
          <div className="card-header">
            <div className="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </div>
            <h2>My Appointments</h2>
          </div>
          
          {appointments.length > 0 ? (
            <div className="appointments-grid">
              {appointments.map((appointment) => (
                <div key={appointment.id} className="appointment-item">
                  <div className="appointment-header">
                    <div className="appointment-date">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                      </svg>
                      <span>{new Date(appointment.appointment_date).toLocaleDateString()}</span>
                    </div>
                    <div className="appointment-time">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12,6 12,12 16,14"/>
                      </svg>
                      <span>{appointment.appointment_time}</span>
                    </div>
                    <div className="appointment-actions">
                      <button 
                        className="dropdown-toggle"
                        onClick={() => toggleDropdown(appointment.id)}
                        aria-label="More options"
                      >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <circle cx="12" cy="12" r="1"/>
                          <circle cx="12" cy="5" r="1"/>
                          <circle cx="12" cy="19" r="1"/>
                        </svg>
                      </button>
                      {openDropdown === appointment.id && (
                        <div className="dropdown-menu">
                          <button 
                            className="dropdown-item delete-item"
                            onClick={() => handleDeleteAppointment(appointment.id)}
                          >
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <polyline points="3,6 5,6 21,6"/>
                              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                              <line x1="10" y1="11" x2="10" y2="17"/>
                              <line x1="14" y1="11" x2="14" y2="17"/>
                            </svg>
                            Delete Appointment
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="appointment-details">
                    <div className="doctor-info">
                      <h4>Dr. {appointment.doctor_name}</h4>
                      <p className="specialization">{appointment.doctor_specialization}</p>
                    </div>
                    
                    <div className="appointment-meta">
                      <div className="hospital-info">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2z"/>
                          <path d="M8 21v-4a2 2 0 012-2h4a2 2 0 012 2v4"/>
                        </svg>
                        <span>{appointment.hospital_name}</span>
                      </div>
                      
                      {appointment.reason && (
                        <div className="appointment-reason">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14,2 14,8 20,8"/>
                            <line x1="16" y1="13" x2="8" y2="13"/>
                            <line x1="16" y1="17" x2="8" y2="17"/>
                            <polyline points="10,9 9,9 8,9"/>
                          </svg>
                          <span>{appointment.reason}</span>
                        </div>
                      )}
                      
                      <div className="appointment-status">
                        <span className={`status-badge ${appointment.status.toLowerCase()}`}>
                          {appointment.status}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-appointments">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <h3>No Appointments</h3>
              <p>You don't have any scheduled appointments yet.</p>
              <button 
                className="book-appointment-btn"
                onClick={() => navigate("/assistant")}
              >
                Book an Appointment
              </button>
            </div>
          )}
        </div>
      </div>
      </div>
    </div>
  );
};

export default PatientDashboard;

