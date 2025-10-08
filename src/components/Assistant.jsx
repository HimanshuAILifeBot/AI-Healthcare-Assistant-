import { useState, useRef, useContext } from "react";
import { useTheme } from "../context/ThemeContext";
import "./Assistant.css";
import RecordRTC from "recordrtc";
import va from "../assets/assistant.jpg";
import logo from "../assets/logo-01.jpg";
import { datacontext } from "../context/UserContext";

export default function Assistant() {
  const {connect, disconnect, messages}=useContext(datacontext)
  const { theme, toggleTheme } = useTheme();
  const [isListening, setIsListening] = useState(false);
  const [botStatus, setBotStatus] = useState('Ready to help');

  const handleConnect = () => {
    setIsListening(true);
    setBotStatus('Listening...');
    connect();
  };

  const handleDisconnect = () => {
    setIsListening(false);
    setBotStatus('Ready to help');
    disconnect();
  };

  return (
    <div className="assistant-page">
      {/* Navigation */}
      <nav className="assistant-nav">
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
              className="back-button"
              onClick={() => window.history.back()}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 12H5"/>
                <path d="M12 19l-7-7 7-7"/>
              </svg>
              Back to Dashboard
            </button>
          </div>
        </div>
      </nav>

      <div className="assistant-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
        <div className="floating-particles">
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
        </div>
      </div>
      
      <div className="assistant-container">
        {/* Avatar Section */}
        <div className="avatar-section">
          <div className="avatar-container">
            <div className="avatar-frame">
              <div className="avatar-glow"></div>
              <img
                src={va}
                alt="AI LifeBot Avatar"
                className={`avatar-image ${isListening ? 'listening' : ''}`}
              />
              <div className="pulse-rings">
                <div className={`pulse-ring ${isListening ? 'active' : ''}`}></div>
                <div className={`pulse-ring pulse-ring-2 ${isListening ? 'active' : ''}`}></div>
                <div className={`pulse-ring pulse-ring-3 ${isListening ? 'active' : ''}`}></div>
              </div>
              <div className="voice-waves">
                <div className={`wave ${isListening ? 'animate' : ''}`}></div>
                <div className={`wave ${isListening ? 'animate' : ''}`}></div>
                <div className={`wave ${isListening ? 'animate' : ''}`}></div>
                <div className={`wave ${isListening ? 'animate' : ''}`}></div>
              </div>
            </div>
            
            <div className="avatar-info">
              <h2 className="avatar-name">Dr. LifeBot</h2>
              <p className="avatar-title">Your AI Medical Assistant</p>
              <div className="status-badge">
                <div className={`status-dot ${isListening ? 'listening' : 'ready'}`}></div>
                <span>{botStatus}</span>
              </div>
            </div>
          </div>

          {/* Voice Controls */}
          <div className="voice-controls">
            <button
              className={`voice-button ${isListening ? 'listening' : ''}`}
              onClick={isListening ? handleDisconnect : handleConnect}
            >
              <div className="button-glow"></div>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                {isListening ? (
                  <>
                    <rect x="6" y="4" width="4" height="16" rx="2"/>
                    <rect x="14" y="4" width="4" height="16" rx="2"/>
                  </>
                ) : (
                  <>
                    <path d="M12 2a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3Z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                    <line x1="12" x2="12" y1="19" y2="22"/>
                  </>
                )}
              </svg>
              <span>{isListening ? 'Stop Listening' : 'Start Voice Chat'}</span>
            </button>
            
            <div className="voice-tips">
              <p>💡 Try saying: "How can you help me?" or "I have a headache"</p>
            </div>
          </div>
        </div>

        {/* Chat Section */}
        <div className="chat-section">
          <div className="chat-header">
            <div className="chat-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <span>Conversation History</span>
            </div>
            <div className="chat-status">
              <div className={`status-indicator ${messages.length > 0 ? 'active' : ''}`}></div>
              <span>{messages.length} messages</span>
            </div>
          </div>
          
          <div className="chat-messages">
            {messages.length > 0 ? (
              messages.map((message, index) => (
                <div key={index} className={`message ${message.sender.toLowerCase()}`}>
                  <div className="message-avatar">
                    {message.sender === 'Patient' ? (
                      <div className="user-avatar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                          <circle cx="12" cy="7" r="4"/>
                        </svg>
                      </div>
                    ) : (
                      <div className="bot-avatar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M12 2a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3Z"/>
                          <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                          <line x1="12" x2="12" y1="19" y2="22"/>
                        </svg>
                      </div>
                    )}
                  </div>
                  <div className="message-content">
                    <div className="message-sender-label">
                      {message.sender === 'Patient' ? (
                        <>
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                          </svg>
                          You
                        </>
                      ) : (
                        <>
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                          </svg>
                          Dr. LifeBot
                        </>
                      )}
                    </div>
                    <div className="message-bubble">
                      <div className="message-text">{message.text}</div>
                      <div className="message-time">{new Date().toLocaleTimeString()}</div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-chat">
                <div className="empty-icon">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    <path d="M12 8v4"/>
                    <path d="M12 16h.01"/>
                  </svg>
                </div>
                <h3>Ready to Start Your Health Journey</h3>
                <p>Click "Start Voice Chat" to begin talking with Dr. LifeBot</p>
                <div className="quick-actions">
                  <div className="quick-action">
                    <span>💊</span>
                    <p>Ask about medications</p>
                  </div>
                  <div className="quick-action">
                    <span>🩺</span>
                    <p>Describe symptoms</p>
                  </div>
                  <div className="quick-action">
                    <span>📋</span>
                    <p>Get health advice</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}