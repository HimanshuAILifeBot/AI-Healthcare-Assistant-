import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './Insurance.css';

export default function Insurance() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [showTerms, setShowTerms] = useState(false);

  const insurancePlans = [
    {
      id: 1,
      name: "Basic Health Shield",
      price: "₹5,000",
      pricePerMonth: "₹417/month",
      coverage: "₹5,00,000",
      features: [
        "Hospitalization cover",
        "Pre & post hospitalization",
        "Ambulance charges",
        "Day care procedures",
        "24/7 Customer support"
      ],
      popular: false
    },
    {
      id: 2,
      name: "Premium Health Plus",
      price: "₹10,000",
      pricePerMonth: "₹833/month",
      coverage: "₹10,00,000",
      features: [
        "All Basic features",
        "Critical illness cover",
        "Maternity benefits",
        "Annual health checkup",
        "No claim bonus 50%",
        "Worldwide emergency care"
      ],
      popular: true
    },
    {
      id: 3,
      name: "Elite Care Supreme",
      price: "₹20,000",
      pricePerMonth: "₹1,667/month",
      coverage: "₹25,00,000",
      features: [
        "All Premium features",
        "Organ transplant cover",
        "Cancer care treatment",
        "Home healthcare",
        "Alternative treatments (Ayurveda)",
        "International treatment",
        "Personal health manager"
      ],
      popular: false
    }
  ];

  return (
    <div className="insurance-page">
      {/* Header */}
      <nav className="insurance-nav">
        <div className="nav-container">
          <div className="nav-logo">
            <div className="insurance-logo">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <path d="M9 12l2 2 4-4"/>
              </svg>
              <span>SecureHealth Insurance</span>
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
            <button className="back-button" onClick={() => navigate('/dashboard')}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 12H5"/>
                <path d="M12 19l-7-7 7-7"/>
              </svg>
              Back to Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="insurance-hero">
        <div className="hero-content">
          <h1 className="hero-title">Protect Your Health, Secure Your Future</h1>
          <p className="hero-subtitle">
            Comprehensive health insurance plans designed for you and your family
          </p>
          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">10,000+</div>
              <div className="stat-label">Network Hospitals</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Claim Support</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">98%</div>
              <div className="stat-label">Claim Settlement</div>
            </div>
          </div>
        </div>
      </div>

      {/* Plans Section */}
      <div className="plans-section">
        <div className="section-header">
          <h2>Choose Your Perfect Plan</h2>
          <p>Select a plan that matches your healthcare needs</p>
        </div>

        <div className="plans-grid">
          {insurancePlans.map((plan) => (
            <div 
              key={plan.id} 
              className={`plan-card ${plan.popular ? 'popular' : ''} ${selectedPlan === plan.id ? 'selected' : ''}`}
            >
              {plan.popular && <div className="popular-badge">Most Popular</div>}
              
              <div className="plan-header">
                <h3>{plan.name}</h3>
                <div className="plan-price">
                  <span className="price-amount">{plan.price}</span>
                  <span className="price-period">/year</span>
                </div>
                <div className="price-monthly">{plan.pricePerMonth}</div>
              </div>

              <div className="plan-coverage">
                <div className="coverage-label">Coverage Amount</div>
                <div className="coverage-amount">{plan.coverage}</div>
              </div>

              <div className="plan-features">
                <h4>Key Features:</h4>
                <ul>
                  {plan.features.map((feature, index) => (
                    <li key={index}>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <button 
                className={`select-plan-btn ${selectedPlan === plan.id ? 'selected' : ''}`}
                onClick={() => setSelectedPlan(plan.id)}
              >
                {selectedPlan === plan.id ? 'Selected ✓' : 'Select Plan'}
              </button>
            </div>
          ))}
        </div>

        {selectedPlan && (
          <div className="action-buttons">
            <button 
              className="view-terms-btn"
              onClick={() => setShowTerms(true)}
            >
              View Terms & Conditions
            </button>
            <button className="proceed-btn">
              Proceed to Purchase
            </button>
          </div>
        )}
      </div>

      {/* Benefits Section */}
      <div className="benefits-section">
        <h2>Why Choose SecureHealth?</h2>
        <div className="benefits-grid">
          <div className="benefit-card">
            <div className="benefit-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
            </div>
            <h3>Instant Claim Settlement</h3>
            <p>Get your claims processed within 24-48 hours with our streamlined digital process</p>
          </div>

          <div className="benefit-card">
            <div className="benefit-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <h3>Cashless Hospitalization</h3>
            <p>Access cashless treatment at 10,000+ network hospitals across India</p>
          </div>

          <div className="benefit-card">
            <div className="benefit-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <h3>24/7 Support</h3>
            <p>Round-the-clock customer support and medical assistance whenever you need</p>
          </div>

          <div className="benefit-card">
            <div className="benefit-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <h3>No Pre-Policy Checkup</h3>
            <p>Get instant coverage without the hassle of medical tests for eligible plans</p>
          </div>
        </div>
      </div>

      {/* Terms Modal */}
      {showTerms && (
        <div className="modal-overlay" onClick={() => setShowTerms(false)}>
          <div className="terms-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Terms & Conditions</h2>
              <button className="close-modal" onClick={() => setShowTerms(false)}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            
            <div className="modal-content">
              <section>
                <h3>1. Coverage Details</h3>
                <p>This health insurance policy provides comprehensive coverage for hospitalization, pre and post-hospitalization expenses, day care procedures, and emergency ambulance services. The coverage amount varies based on the selected plan.</p>
              </section>

              <section>
                <h3>2. Waiting Period</h3>
                <p>
                  <strong>Initial Waiting Period:</strong> 30 days from policy inception (except accident-related claims)
                  <br/>
                  <strong>Pre-existing Diseases:</strong> 24-48 months waiting period
                  <br/>
                  <strong>Specific Diseases:</strong> 2-4 years for specified illnesses
                </p>
              </section>

              <section>
                <h3>3. Exclusions</h3>
                <ul>
                  <li>Cosmetic or aesthetic treatments</li>
                  <li>Self-inflicted injuries</li>
                  <li>Treatment arising from alcohol or drug abuse</li>
                  <li>War, nuclear contamination related injuries</li>
                  <li>Experimental or unproven treatments</li>
                </ul>
              </section>

              <section>
                <h3>4. Claim Process</h3>
                <p>Claims must be intimated within 24 hours of hospitalization. Required documents include hospital bills, discharge summary, diagnostic reports, and claim form. Cashless facility is available at network hospitals with pre-authorization.</p>
              </section>

              <section>
                <h3>5. Renewal Terms</h3>
                <p>The policy is renewable for lifetime. Premium rates may be revised at renewal based on age and claim history. Grace period of 30 days provided for premium payment.</p>
              </section>

              <section>
                <h3>6. Cancellation Policy</h3>
                <p>Free-look period of 15 days available. If cancelled within this period, premium will be refunded after deducting proportionate risk premium and expenses. After free-look period, cancellation terms as per policy conditions apply.</p>
              </section>

              <section>
                <h3>7. Data Privacy</h3>
                <p>Your personal and medical information will be kept confidential and used only for policy administration, claims processing, and regulatory compliance. We comply with all data protection regulations.</p>
              </section>

              <section>
                <h3>8. Customer Responsibilities</h3>
                <ul>
                  <li>Provide accurate information during application</li>
                  <li>Disclose pre-existing medical conditions</li>
                  <li>Pay premiums on time to avoid policy lapse</li>
                  <li>Inform us of any changes in contact details</li>
                  <li>Submit genuine claims with proper documentation</li>
                </ul>
              </section>

              <div className="terms-footer">
                <p><strong>For detailed terms and conditions, please refer to the policy document.</strong></p>
                <p>For queries, contact: support@securehealthinsurance.com | 1800-XXX-XXXX</p>
              </div>
            </div>

            <div className="modal-footer">
              <button className="accept-btn" onClick={() => setShowTerms(false)}>
                I Accept the Terms & Conditions
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="insurance-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>About Us</h4>
            <p>SecureHealth Insurance is a leading health insurance provider committed to protecting your health and financial well-being.</p>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#plans">Our Plans</a></li>
              <li><a href="#claims">File a Claim</a></li>
              <li><a href="#network">Network Hospitals</a></li>
              <li><a href="#contact">Contact Us</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <p>Email: support@securehealthinsurance.com</p>
            <p>Phone: 1800-XXX-XXXX</p>
            <p>Available 24/7</p>
          </div>
          <div className="footer-section">
            <h4>Regulatory</h4>
            <p>IRDAI Registration No: XXX/2024</p>
            <p>License Valid Till: 31/12/2030</p>
            <p>CIN: UXXXXXXXXXX</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 SecureHealth Insurance. All rights reserved.</p>
          <p>Insurance is the subject matter of solicitation | This is a demo insurance page for educational purposes</p>
        </div>
      </footer>
    </div>
  );
}
