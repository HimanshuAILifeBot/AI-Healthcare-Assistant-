import React, { useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import AuthModal from './AuthModal';
import './HeroPage.css';
import logo from '../assets/logo-01.jpg';

const HeroPage = () => {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'
  const { theme, toggleTheme } = useTheme();

  const openAuthModal = (mode) => {
    setAuthMode(mode);
    setIsAuthModalOpen(true);
  };

  const features = [
    {
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3Z"/>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
          <line x1="12" x2="12" y1="19" y2="22"/>
        </svg>
      ),
      title: "Voice-Activated Care",
      description: "Natural conversation with AI that understands medical terminology and provides accurate health insights."
    },
    {
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
      ),
      title: "Smart Health Monitoring",
      description: "Continuous tracking of your health metrics with AI-powered analysis and personalized recommendations."
    },
    {
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 9V5a3 3 0 0 0-6 0v4"/>
          <rect x="2" y="11" width="20" height="11" rx="2" ry="2"/>
        </svg>
      ),
      title: "HIPAA Compliant",
      description: "Your health data is protected with enterprise-grade security and full HIPAA compliance."
    },
    {
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12,6 12,12 16,14"/>
        </svg>
      ),
      title: "24/7 Availability",
      description: "Your AI health companion is always available, providing instant support whenever you need it."
    }
  ];

  const benefits = [
    {
      metric: "98%",
      label: "Accuracy Rate",
      description: "Clinical-grade accuracy in health assessments and recommendations"
    },
    {
      metric: "24/7",
      label: "Availability",
      description: "Always-on health support without waiting for appointments"
    },
    {
      metric: "5min",
      label: "Average Response",
      description: "Quick, comprehensive health insights in minutes, not hours"
    },
    {
      metric: "100K+",
      label: "Users Served",
      description: "Trusted by healthcare professionals and patients worldwide"
    }
  ];

  return (
    <div className="hero-page">
      {/* Navigation Header */}
      <nav className="hero-nav">
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
              className="nav-btn login-btn"
              onClick={() => openAuthModal('login')}
            >
              Sign In
            </button>
            <button 
              className="nav-btn cta-btn"
              onClick={() => openAuthModal('signup')}
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
        </div>
        
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <span>🏥 #1 AI Health Assistant</span>
            </div>
            <h1 className="hero-title">
              Your Personal
              <span className="gradient-text"> AI Health Companion</span>
              <br />for Better Living
            </h1>
            <p className="hero-subtitle">
              Experience the future of healthcare with our advanced AI voice agent. 
              Get instant health insights, personalized recommendations, and 24/7 medical support 
              through natural conversation.
            </p>
            <div className="hero-actions">
              <button 
                className="hero-cta primary"
                onClick={() => openAuthModal('signup')}
              >
                Start Your Health Journey
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12,5 19,12 12,19"/>
                </svg>
              </button>
              <button className="hero-cta secondary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polygon points="5,3 19,12 5,21"/>
                </svg>
                Watch Demo
              </button>
            </div>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">98%</span>
                <span className="stat-label">Accuracy</span>
              </div>
              <div className="stat">
                <span className="stat-number">24/7</span>
                <span className="stat-label">Available</span>
              </div>
              <div className="stat">
                <span className="stat-number">100K+</span>
                <span className="stat-label">Users</span>
              </div>
            </div>
          </div>
          <div className="hero-visual">
            <div className="ai-avatar-container">
              <div className="avatar-glow"></div>
              <div className="ai-avatar">
                <img src="/src/assets/assistant.jpg" alt="AI Health Assistant" />
              </div>
              <div className="pulse-rings">
                <div className="pulse-ring ring-1"></div>
                <div className="pulse-ring ring-2"></div>
                <div className="pulse-ring ring-3"></div>
              </div>
            </div>
            <div className="floating-cards">
              <div className="health-card card-1">
                <div className="card-icon">💓</div>
                <div className="card-content">
                  <span className="card-label">Heart Rate</span>
                  <span className="card-value">72 BPM</span>
                </div>
              </div>
              <div className="health-card card-2">
                <div className="card-icon">🩺</div>
                <div className="card-content">
                  <span className="card-label">Health Score</span>
                  <span className="card-value">95/100</span>
                </div>
              </div>
              <div className="health-card card-3">
                <div className="card-icon">💊</div>
                <div className="card-content">
                  <span className="card-label">Medication</span>
                  <span className="card-value">On Track</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-container">
          <div className="section-header">
            <h2>Powered by Advanced AI Technology</h2>
            <p>Experience healthcare like never before with our cutting-edge AI voice agent</p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="use-cases-section">
        <div className="use-cases-container">
          <div className="use-cases-header">
            <h2>
              <span className="highlight-text">Battle-Tested</span> Healthcare AI Voice Agents
            </h2>
            <p>Our specialized AI agents handle various healthcare scenarios with precision and care</p>
          </div>
          <div className="use-cases-grid">
            <div className="use-case-card">
              <div className="use-case-content">
                <h3>Appointment Scheduling</h3>
                <p>Books and reschedules appointments seamlessly</p>
              </div>
              <div className="agent-photo">
                <img src="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&h=300&q=80" alt="Anna - Appointment Specialist" />
                <div className="agent-name">Anna</div>
              </div>
            </div>
            
            <div className="use-case-card">
              <div className="use-case-content">
                <h3>Medical Billing Questions</h3>
                <p>Answers patients' billing questions accurately</p>
              </div>
              <div className="agent-photo">
                <img src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80" alt="Emma - Billing Specialist" />
                <div className="agent-name">Emma</div>
              </div>
            </div>
            
            <div className="use-case-card">
              <div className="use-case-content">
                <h3>Patient Balance Reminder</h3>
                <p>Reminds patients of balances and collects payment on the call</p>
              </div>
              <div className="agent-photo">
                <img src="https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&h=300&q=80" alt="Ben - Payment Specialist" />
                <div className="agent-name">Ben</div>
              </div>
            </div>
            
            <div className="use-case-card">
              <div className="use-case-content">
                <h3>Re-Engagement Campaign</h3>
                <p>Schedules annual check-ups and follow-up appointments</p>
              </div>
              <div className="agent-photo">
                <img src="https://images.unsplash.com/photo-1551836022-deb4988cc6c0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&h=300&q=80" alt="Sara - Engagement Specialist" />
                <div className="agent-name">Sara</div>
              </div>
            </div>
          </div>
          
          <div className="additional-use-cases">
            <div className="additional-case">
              <div className="additional-content">
                <h3>Appointment Reminder</h3>
                <p>Sends timely reminders to reduce no-shows</p>
              </div>
            </div>
            
            <div className="additional-case">
              <div className="additional-content">
                <h3>Symptom Assessment</h3>
                <p>Conducts initial symptom evaluation</p>
              </div>
            </div>
            
            <div className="additional-case">
              <div className="additional-content">
                <h3>Medication Reminder</h3>
                <p>Helps patients stay on track with medications</p>
              </div>
            </div>
            
            <div className="additional-case">
              <div className="additional-content">
                <h3>Prior Authorization</h3>
                <p>Initiation and Follow-up for insurance approvals</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="benefits-section">
        <div className="benefits-container">
          <div className="benefits-header">
            <h2>Why Choose AI LifeBot Health Agent?</h2>
            <p>Experience the future of healthcare with our advanced AI technology</p>
          </div>
          <div className="benefits-content">
            <div className="benefits-metrics">
              <div className="metric-card">
                <div className="metric-icon">🎯</div>
                <div className="metric-content">
                  <span className="metric-number">98%</span>
                  <span className="metric-label">Accuracy Rate</span>
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">⚡</div>
                <div className="metric-content">
                  <span className="metric-number">24/7</span>
                  <span className="metric-label">Availability</span>
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">🔒</div>
                <div className="metric-content">
                  <span className="metric-number">100%</span>
                  <span className="metric-label">HIPAA Compliant</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="workflow-section">
        <div className="section-container">
          <div className="section-header">
            <h2>How It Works</h2>
            <p>Get started with your AI health companion in three simple steps</p>
          </div>
          <div className="workflow-steps">
            <div className="workflow-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Sign Up & Setup</h3>
                <p>Create your account and complete your health profile for personalized care</p>
              </div>
            </div>
            <div className="workflow-arrow">
              <svg width="40" height="20" viewBox="0 0 40 20" fill="none">
                <path d="M0 10h35m-5-5l5 5-5 5" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="workflow-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Start Conversation</h3>
                <p>Simply speak to your AI health assistant about any health concerns or questions</p>
              </div>
            </div>
            <div className="workflow-arrow">
              <svg width="40" height="20" viewBox="0 0 40 20" fill="none">
                <path d="M0 10h35m-5-5l5 5-5 5" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="workflow-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Get Insights</h3>
                <p>Receive personalized health insights, recommendations, and next steps</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-content">
            <h2>Ready to Transform Your Health Journey?</h2>
            <p>Join thousands of users who trust AI LifeBot Health Agent for their healthcare needs</p>
            <div className="cta-actions">
              <button 
                className="cta-button primary"
                onClick={() => openAuthModal('signup')}
              >
                Get Started Today
              </button>
              <button 
                className="cta-button secondary"
                onClick={() => openAuthModal('login')}
              >
                Sign In
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="hero-footer">
        <div className="footer-content">
          <div className="footer-logo">
            <div className="logo-icon">
              <img src={logo} alt="AI LifeBot" style={{ width: '100px', height: 'auto' }} />
            </div>
          </div>
          <div className="footer-links">
            <a href="#privacy">Privacy Policy</a>
            <a href="#terms">Terms of Service</a>
            <a href="#contact">Contact</a>
          </div>
          <div className="footer-copyright">
            <p>&copy; 2025 AI LifeBot Health Agent. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      {isAuthModalOpen && (
        <AuthModal 
          mode={authMode} 
          onClose={() => setIsAuthModalOpen(false)}
        />
      )}
    </div>
  );
};

export default HeroPage;