import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Success.css";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export default function Success() {
  const [data, setData] = useState({
    patientName: "",
    doctor: "",
    hospital: "",
    bookingId: "",
    date: "",
    time: "",
  });
  const [actualUserName, setActualUserName] = useState("");
  const [showConfetti, setShowConfetti] = useState(false);
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  // Function to format the date and time for display
  const formatAppointmentDateTime = (dateString, timeString) => {
    if (!dateString || !timeString) return "Not available";
    
    try {
      const appointmentDate = new Date(dateString);
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      // Format the date
      let dateLabel;
      if (appointmentDate.toDateString() === today.toDateString()) {
        dateLabel = "Today";
      } else if (appointmentDate.toDateString() === tomorrow.toDateString()) {
        dateLabel = "Tomorrow";
      } else {
        dateLabel = appointmentDate.toLocaleDateString('en-US', { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        });
      }
      
      // Format the time (assuming timeString is in HH:MM:SS format)
      const [hours, minutes] = timeString.split(':');
      const hour = parseInt(hours);
      const ampm = hour >= 12 ? 'PM' : 'AM';
      const displayHour = hour % 12 || 12;
      const formattedTime = `${displayHour}:${minutes} ${ampm}`;
      
      return `${dateLabel}, ${formattedTime}`;
    } catch (error) {
      console.error("Error formatting date/time:", error);
      return "Not available";
    }
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const queryData = JSON.parse(params.get("data"));
    setData(queryData);
    
    // Trigger confetti animation
    setShowConfetti(true);
    setTimeout(() => setShowConfetti(false), 3000);
  }, []);

  // Fetch actual logged-in user's name
  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    
    if (userId) {
      fetch(`${BACKEND_URL}/patient-details/${userId}`)
        .then((res) => {
          if (!res.ok) throw new Error("Failed to fetch patient details");
          return res.json();
        })
        .then((patientData) => {
          // Set the actual user's name
          if (patientData && patientData.name) {
            setActualUserName(patientData.name);
          }
        })
        .catch((err) => {
          console.error("Error fetching patient details:", err);
          // Fall back to URL data if fetch fails
        });
    }
  }, []);

  return (
    <div className="success-container">
      {showConfetti && <div className="confetti-overlay"></div>}
      
      {/* Theme Toggle Button */}
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
      
      {/* Success Header */}
      <div className="success-header">
        <div className="success-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.2"/>
            <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <h1 className="success-title">Appointment Confirmed!</h1>
        <p className="success-subtitle">
          Your healthcare appointment has been successfully scheduled. We've sent a confirmation to your registered email.
        </p>
      </div>

      {/* Appointment Details Card */}
      <div className="appointment-details-card">
        <div className="card-header">
          <div className="card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
              <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" strokeWidth="2"/>
              <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" strokeWidth="2"/>
              <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </div>
          <h2>Appointment Details</h2>
        </div>

        <div className="details-grid">
          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Patient Name</span>
              <span className="detail-value">{actualUserName || data.patientName || "John Doe"}</span>
            </div>
          </div>

          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2"/>
                <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2"/>
                <polyline points="10,9 9,9 8,9" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Doctor</span>
              <span className="detail-value">{data.doctor || "Dr. Sarah Johnson"}</span>
            </div>
          </div>

          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke="currentColor" strokeWidth="2"/>
                <circle cx="12" cy="10" r="3" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Hospital/Clinic</span>
              <span className="detail-value">{data.hospital || "City General Hospital"}</span>
            </div>
          </div>

          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 11H5a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h4m6-6h4a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-4" stroke="currentColor" strokeWidth="2"/>
                <path d="M8 21V9a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v12" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Booking ID</span>
              <span className="detail-value">{data.bookingId || "APT-2024-001"}</span>
            </div>
          </div>

          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <polyline points="12,6 12,12 16,14" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Appointment Time</span>
              <span className="detail-value">{formatAppointmentDateTime(data.date, data.time)}</span>
            </div>
          </div>

          <div className="detail-item">
            <div className="detail-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="detail-content">
              <span className="detail-label">Required Documents</span>
              <span className="detail-value">Valid ID Proof, Insurance Card</span>
            </div>
          </div>
        </div>
      </div>

      {/* Important Notes */}
      <div className="important-notes">
        <div className="notes-header">
          <div className="notes-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
              <line x1="12" y1="8" x2="12" y2="16" stroke="currentColor" strokeWidth="2"/>
              <line x1="12" y1="6" x2="12.01" y2="6" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </div>
          <h3>Important Information</h3>
        </div>
        <ul className="notes-list">
          <li>Please arrive 15 minutes before your scheduled appointment</li>
          <li>Bring all required documents and your insurance card</li>
          <li>If you need to cancel or reschedule, please contact us at least 24 hours in advance</li>
          <li>For emergency contact: <strong>1800-123-456</strong></li>
        </ul>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="primary-btn download-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2"/>
            <polyline points="7,10 12,15 17,10" stroke="currentColor" strokeWidth="2"/>
            <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Download Appointment Slip
        </button>

        <button className="secondary-btn calendar-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
            <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" strokeWidth="2"/>
            <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" strokeWidth="2"/>
            <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Add to Calendar
        </button>

        <button className="secondary-btn reschedule-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polyline points="23,4 23,10 17,10" stroke="currentColor" strokeWidth="2"/>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Reschedule Appointment
        </button>

        <button className="primary-btn dashboard-btn" onClick={() => navigate('/dashboard')}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="7" height="7" stroke="currentColor" strokeWidth="2"/>
            <rect x="14" y="3" width="7" height="7" stroke="currentColor" strokeWidth="2"/>
            <rect x="14" y="14" width="7" height="7" stroke="currentColor" strokeWidth="2"/>
            <rect x="3" y="14" width="7" height="7" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Return to Dashboard
        </button>
      </div>
    </div>
  );
}
