import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import React from "react";
import { useTheme } from "../context/ThemeContext";
import "./Recommendation.css";
import logo from "../assets/logo-01.jpg";

// Backend URL from environment variable
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export default function Recommendation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const {
    recommended_specialists = [],
    doctors = [],
  } = location.state || {};

  const [showPayment, setShowPayment] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const DOCTORS_PER_PAGE = 9; // Show 9 doctors per page
  
  // Date filter state
  const [selectedDate, setSelectedDate] = useState('');
  const [filteredDoctors, setFilteredDoctors] = useState(doctors);
  
  // Update filtered doctors whenever doctors or selectedDate changes
  React.useEffect(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set to start of today
    
    // First filter: Only show doctors with future or today's availability
    const futureDoctors = doctors.filter(doctor => {
      if (doctor.next_available_date && doctor.next_available_date !== "Not available") {
        const doctorDate = new Date(doctor.next_available_date);
        doctorDate.setHours(0, 0, 0, 0);
        return doctorDate >= today; // Only include today and future dates
      }
      return false;
    });
    
    if (!selectedDate) {
      setFilteredDoctors(futureDoctors);
      return;
    }
    
    // Second filter: Apply date selection on already filtered future doctors
    const filtered = futureDoctors.filter(doctor => {
      const doctorDateStr = new Date(doctor.next_available_date).toISOString().split('T')[0];
      const selectedDateStr = new Date(selectedDate).toISOString().split('T')[0];
      return doctorDateStr === selectedDateStr;
    });
    
    console.log(`Filtering by exact date: ${selectedDate}, found ${filtered.length} doctors`);
    setFilteredDoctors(filtered);
    setCurrentPage(1); // Reset to first page when filtering
  }, [doctors, selectedDate]);
  
  const totalPages = Math.ceil(filteredDoctors.length / DOCTORS_PER_PAGE);
  
  // Calculate which doctors to show based on current page
  const startIndex = (currentPage - 1) * DOCTORS_PER_PAGE;
  const endIndex = startIndex + DOCTORS_PER_PAGE;
  const currentDoctors = filteredDoctors.slice(startIndex, endIndex);
  
  // Function to handle page change with smooth scroll
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    // Scroll to doctors section smoothly
    const doctorsSection = document.querySelector('.doctors-section');
    if (doctorsSection) {
      doctorsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  // Function to handle date filtering
  const handleDateFilter = (newDate) => {
    setSelectedDate(newDate);
  };

  const handleBookAppointment = (doctor) => {
    setSelectedDoctor(doctor);
    setShowPayment(true);
  };

  const handleDummyPayment = async () => {
    setIsProcessing(true);
    try {
      const userId = localStorage.getItem("user_id");

      const response = await fetch(`${BACKEND_URL}/appointments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_id: parseInt(userId),
          doctor_id: selectedDoctor.doctor_id,
          slot_id: selectedDoctor.slot_id,
          reason: "Booked via AI Assistant"
        }),
      });

      const data = await response.json();

      const patientDetails = await fetch(`${BACKEND_URL}/patient-details/${userId}`);
      const patientData = await patientDetails.json();

      const payload = {
        patientName: patientData.name,
        doctor: selectedDoctor.name,
        hospital: selectedDoctor.hospital,
        bookingId: `BOOK-${data.appointment_id}`,
        date: selectedDoctor.next_available_date,
        time: selectedDoctor.start_time
      };
      const encoded = encodeURIComponent(JSON.stringify(payload));
      navigate(`/success?data=${encoded}`);
    } catch (err) {
      console.error("Appointment creation failed:", err);
    } finally {
      setIsProcessing(false);
      setShowPayment(false);
    }
  };

  function formatDateTime(dateString, timeString) {
    if (!dateString || !timeString) return "Not available";

    const date = new Date(`${dateString}T${timeString}`);
    const dayOfWeek = date.toLocaleDateString("en-GB", { weekday: "short" });
    const dateFormatted = date.toLocaleDateString("en-GB");
    const timeFormatted = date.toLocaleTimeString("en-GB", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });

    return `${dayOfWeek} ${dateFormatted} at ${timeFormatted}`;
  }

  return (
    <div className="recommendation-container">
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
              className="dashboard-button"
              onClick={() => navigate("/dashboard")}
            >
              Return to Dashboard
            </button>
            <button 
              className="logout-button"
              onClick={() => {
                localStorage.removeItem("user_id");
                navigate("/");
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Header Section */}
      <div className="recommendation-header">
        <div className="header-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19.5 7A9 9 0 0 0 12 3a9 9 0 0 0-7.5 4"/>
            <path d="M11.76 21.48A9 9 0 0 0 15.5 9.4"/>
            <path d="M8.5 14.5L12 11l7 7"/>
            <circle cx="12" cy="12" r="2"/>
          </svg>
        </div>
        <h1 className="recommendation-title">AI Health Recommendations</h1>
        <p className="recommendation-subtitle">Personalized healthcare guidance based on your symptoms</p>
      </div>

      {/* Specialists Section */}
      {recommended_specialists.length > 0 ? (
        <div className="specialists-section">
          <div className="section-header">
            <h2>Recommended Specialists</h2>
            <p>Based on your symptoms analysis, we suggest consulting these medical specialists:</p>
          </div>
          <div className="specialists-grid">
            {recommended_specialists.map((spec, idx) => (
              <div key={idx} className="specialist-badge">
                <div className="specialist-icon">🩺</div>
                <span className="specialist-name">{spec}</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="warning-section">
          <div className="warning-icon">⚠️</div>
          <p className="warning-text">No specialist recommendations available at this time.</p>
        </div>
      )}

      {/* Available Doctors Section */}
      {doctors.length > 0 ? (
        <div className="doctors-section">
          <div className="section-header">
            <h2>Available Doctors</h2>
            <p>Choose from our verified healthcare professionals</p>
            
            {/* Date Filter */}
            <div className="date-filter-section">
              <div className="date-filter-container">
                <label htmlFor="appointment-date" className="date-filter-label">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  Filter by Date:
                </label>
                <input
                  type="date"
                  id="appointment-date"
                  className="date-filter-input"
                  value={selectedDate}
                  onChange={(e) => handleDateFilter(e.target.value)}
                  min={new Date().toISOString().split('T')[0]}
                />
                {selectedDate && (
                  <button 
                    className="clear-date-btn"
                    onClick={() => handleDateFilter('')}
                    title="Clear date filter"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18"/>
                      <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                  </button>
                )}
              </div>
            </div>
            
            {filteredDoctors.length > DOCTORS_PER_PAGE && (
              <div className="pagination-info">
                <span className="showing-count">
                  Showing {startIndex + 1}-{Math.min(endIndex, filteredDoctors.length)} of {filteredDoctors.length} doctors
                  {selectedDate && ` available on ${new Date(selectedDate).toLocaleDateString()}`}
                </span>
              </div>
            )}
          </div>
          {filteredDoctors.length === 0 && selectedDate ? (
            <div className="no-doctors-date-section">
              <div className="no-doctors-icon">📅</div>
              <p className="no-doctors-text">
                No doctors available on {new Date(selectedDate).toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
              <p className="suggestion-text">Try selecting a different date or clear the date filter to see all available doctors.</p>
              <button 
                className="clear-filter-btn" 
                onClick={() => handleDateFilter('')}
              >
                Clear Date Filter
              </button>
            </div>
          ) : (
            <div className="doctors-grid">
              {currentDoctors.map((doc, index) => (
              <div className="doctor-card" key={index}>
                <div className="doctor-card-header">
                  <div className="doctor-avatar">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div className="doctor-basic-info">
                    <h3 className="doctor-name">{doc.name}</h3>
                    <p className="doctor-specialization">{doc.specialization}</p>
                    <div className="doctor-rating">
                      <div className="rating-stars">
                        {[...Array(5)].map((_, i) => (
                          <span key={i} className={`star ${i < Math.floor(doc.rating) ? 'filled' : ''}`}>★</span>
                        ))}
                      </div>
                      <span className="rating-value">{doc.rating}/5</span>
                    </div>
                  </div>
                </div>
                
                <div className="doctor-details">
                  <div className="detail-item">
                    <div className="detail-icon">🏥</div>
                    <div className="detail-content">
                      <span className="detail-label">Hospital</span>
                      <span className="detail-value">{doc.hospital}</span>
                    </div>
                  </div>
                  
                  <div className="detail-item">
                    <div className="detail-icon">💰</div>
                    <div className="detail-content">
                      <span className="detail-label">Consultation Fee</span>
                      <span className="detail-value">₹{doc.fees}</span>
                    </div>
                  </div>
                  
                  <div className="detail-item">
                    <div className="detail-icon">📅</div>
                    <div className="detail-content">
                      <span className="detail-label">Next Available</span>
                      <span className="detail-value">{formatDateTime(doc.next_available_date, doc.start_time)}</span>
                    </div>
                  </div>
                </div>
                
                <div className="doctor-actions">
                  <button className="book-appointment-btn" onClick={() => handleBookAppointment(doc)}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M8 2v4"/>
                      <path d="M16 2v4"/>
                      <rect x="3" y="4" width="18" height="18" rx="2"/>
                      <path d="M3 10h18"/>
                    </svg>
                    Book Appointment
                  </button>
                </div>
              </div>
              ))}
            </div>
          )}
          
          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination-slider-container">
              <div className="pagination-slider">
                <button 
                  className="pagination-nav-btn"
                  onClick={() => handlePageChange(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M15 18l-6-6 6-6"/>
                  </svg>
                  Previous
                </button>
                
                <div className="page-numbers">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
                    <button
                      key={pageNum}
                      className={`page-number-btn ${currentPage === pageNum ? 'active' : ''}`}
                      onClick={() => handlePageChange(pageNum)}
                    >
                      {pageNum}
                    </button>
                  ))}
                </div>
                
                <button 
                  className="pagination-nav-btn"
                  onClick={() => handlePageChange(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 18l6-6-6-6"/>
                  </svg>
                </button>
              </div>
              
              <div className="pagination-info-bottom">
                <span>Page {currentPage} of {totalPages}</span>
                <span className="total-results">{filteredDoctors.length} doctors found</span>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="no-doctors-section">
          <div className="no-doctors-icon">👨‍⚕️</div>
          <p className="no-doctors-text">No doctors available for the selected specialists at the moment.</p>
          <button className="retry-btn" onClick={() => window.location.reload()}>
            Try Again
          </button>
        </div>
      )}

      {/* Enhanced Payment Modal */}
      {showPayment && (
        <div className="payment-modal">
          <div className="payment-overlay"></div>
          <div className="payment-content">
            <div className="payment-header">
              <div className="payment-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"/>
                  <line x1="1" y1="10" x2="23" y2="10"/>
                </svg>
              </div>
              <h3>Secure Payment</h3>
              <button className="close-btn" onClick={() => setShowPayment(false)}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            
            <div className="appointment-summary">
              <div className="summary-item">
                <span className="summary-label">Doctor</span>
                <span className="summary-value">Dr. {selectedDoctor?.name}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Specialization</span>
                <span className="summary-value">{selectedDoctor?.specialization}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Hospital</span>
                <span className="summary-value">{selectedDoctor?.hospital}</span>
              </div>
              <div className="summary-item total">
                <span className="summary-label">Total Amount</span>
                <span className="summary-value">₹{selectedDoctor?.fees}</span>
              </div>
            </div>
            
            <form className="payment-form" onSubmit={(e) => { e.preventDefault(); handleDummyPayment(); }}>
              <div className="form-group">
                <label htmlFor="cardNumber">Card Number</label>
                <div className="input-with-icon">
                  <input 
                    type="text" 
                    id="cardNumber"
                    placeholder="1234 5678 9012 3456" 
                    maxLength="19"
                    required 
                  />
                  <div className="card-icon">💳</div>
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="expiryDate">Expiry Date</label>
                  <input 
                    type="text" 
                    id="expiryDate"
                    placeholder="MM/YY" 
                    maxLength="5"
                    required 
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="cvv">CVV</label>
                  <input 
                    type="text" 
                    id="cvv"
                    placeholder="123" 
                    maxLength="3"
                    required 
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="cardHolder">Cardholder Name</label>
                <input 
                  type="text" 
                  id="cardHolder"
                  placeholder="John Doe" 
                  required 
                />
              </div>
              
              <div className="payment-actions">
                <button 
                  type="submit" 
                  className="pay-now-btn"
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <div className="spinner"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M9 12l2 2 4-4"/>
                        <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9"/>
                      </svg>
                      Pay ₹{selectedDoctor?.fees}
                    </>
                  )}
                </button>
                <button 
                  type="button" 
                  className="cancel-payment-btn" 
                  onClick={() => setShowPayment(false)}
                  disabled={isProcessing}
                >
                  Cancel
                </button>
              </div>
            </form>
            
            <div className="payment-security">
              <div className="security-badge">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <span>256-bit SSL encrypted</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
