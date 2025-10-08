import React, { createContext, useRef, useState } from "react";
import run from "../gemini";
import { useNavigate } from "react-router-dom";

export const datacontext = createContext();

function UserContext({ children }) {
    const isListening = useRef(false);
    const isSpeaking = useRef(false);
    const recognitionRef = useRef(null);
    const [messages, setMessages] = useState([]);
    const [status, setStatus] = useState("Idle");
    const navigate = useNavigate();
    const audioRef = useRef(new Audio());
    const [userName, setUserName] = useState(null);
    const [hasGreeted, setHasGreeted] = useState(false);
    const symptomCount = useRef(0);

    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    async function speak(text) {
        isSpeaking.current = true;
        
        // CRITICAL: Stop recognition BEFORE speaking to prevent feedback loop
        if (recognitionRef.current && isListening.current) {
            try {
                recognitionRef.current.stop();
                console.log("Speech recognition stopped before speaking");
            } catch (e) {
                console.log("Recognition already stopped");
            }
        }
        
        setStatus("Speaking");

        try {
            // Call Azure TTS backend endpoint with auto language detection
            const response = await fetch(`${BACKEND_URL}/tts`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    text: text,
                    language: null,  // Auto-detect language from text
                    voice_name: null // Auto-select best voice for detected language
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to generate speech");
            }

            const data = await response.json();
            
            if (data.success && data.audio_data) {
                // Convert base64 to audio blob
                const audioBlob = base64ToBlob(data.audio_data, 'audio/mpeg');
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // Play the audio
                audioRef.current.src = audioUrl;
                audioRef.current.onended = () => {
                    URL.revokeObjectURL(audioUrl); // Clean up
                    console.log("Audio playback finished");
                    
                    // Add delay before restarting recognition to prevent picking up echo
                    setTimeout(() => {
                        isSpeaking.current = false;
                        if (isListening.current && recognitionRef.current) {
                            try {
                                recognitionRef.current.start();
                                setStatus("Listening");
                                console.log("Speech recognition restarted after delay");
                            } catch (e) {
                                console.log("Recognition already running or error:", e);
                            }
                        } else {
                            setStatus("Idle");
                        }
                    }, 500); // 500ms delay to let audio hardware settle
                };
                
                audioRef.current.onerror = (e) => {
                    console.error("Audio playback error:", e);
                    isSpeaking.current = false;
                    if (isListening.current && recognitionRef.current) {
                        setTimeout(() => {
                            try {
                                recognitionRef.current.start();
                                setStatus("Listening");
                            } catch (err) {
                                console.log("Error restarting recognition:", err);
                            }
                        }, 500);
                    }
                };
                
                await audioRef.current.play();
            }
        } catch (error) {
            console.error("Error with Azure TTS:", error);
            isSpeaking.current = false;
            // Fallback to browser TTS if Azure fails
            fallbackSpeak(text);
        }
    }

    function base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }

    function fallbackSpeak(text) {
        // Fallback to browser's Web Speech API if Azure TTS fails
        const text_speak = new SpeechSynthesisUtterance(text);
        text_speak.volume = 1;
        text_speak.rate = 1;
        text_speak.pitch = 1;
        text_speak.lang = "en-GB";

        text_speak.onend = () => {
            console.log("Fallback speech finished");
            // Add delay before restarting recognition
            setTimeout(() => {
                isSpeaking.current = false;
                if (isListening.current && recognitionRef.current) {
                    try {
                        recognitionRef.current.start();
                        setStatus("Listening");
                        console.log("Recognition restarted after fallback speech");
                    } catch (e) {
                        console.log("Error restarting recognition:", e);
                    }
                } else {
                    setStatus("Idle");
                }
            }, 500); // 500ms delay
        };

        text_speak.onerror = (e) => {
            console.error("Speech synthesis error:", e);
            isSpeaking.current = false;
            if (isListening.current && recognitionRef.current) {
                setTimeout(() => {
                    try {
                        recognitionRef.current.start();
                        setStatus("Listening");
                    } catch (err) {
                        console.log("Error restarting recognition:", err);
                    }
                }, 500);
            }
        };

        window.speechSynthesis.speak(text_speak);
    }

    // Function to detect language and generate appropriate acknowledgment
    function getAcknowledgment(text) {
        // Detect if text contains Hindi words (basic detection)
        const hindiPattern = /[\u0900-\u097F]/;
        const isHindi = hindiPattern.test(text);
        
        const acknowledgments = {
            hindi: [
                "समझ गया",
                "ठीक है, बताइए",
                "जी हाँ, सुन रहा हूँ",
                "अच्छा, आगे बताइए",
                "समझ गया, और क्या?"
            ],
            english: [
                "I understand",
                "Got it",
                "I see",
                "Okay, continue",
                "Understood, what else?"
            ]
        };
        
        const ackList = isHindi ? acknowledgments.hindi : acknowledgments.english;
        return ackList[Math.floor(Math.random() * ackList.length)];
    }

    async function aiResponse(prompt) {
        setMessages(prev => [...prev, { sender: "Patient", text: prompt }]);

        // First time greeting with user name
        if (!hasGreeted && userName) {
            const hindiPattern = /[\u0900-\u097F]/;
            const isHindi = hindiPattern.test(prompt);
            
            const greeting = isHindi 
                ? `नमस्ते ${userName}! मैं आपका AI हेल्थ असिस्टेंट हूँ। आप अपनी समस्या बताइए।`
                : `Hello ${userName}! I'm your AI Health Assistant. Please tell me about your symptoms.`;
            
            setMessages(prev => [...prev, { sender: "Assistant", text: greeting }]);
            speak(greeting);
            setHasGreeted(true);
            return;
        }

        // Add natural acknowledgment for symptom descriptions
        const acknowledgment = getAcknowledgment(prompt);
        symptomCount.current++;
        
        // Speak acknowledgment immediately for better UX
        if (symptomCount.current > 1) {
            speak(acknowledgment);
            await new Promise(resolve => setTimeout(resolve, 1500)); // Brief pause
        }

        const text = await run(prompt);
        let cleanedText = text.replace(/^Agent:\s*/i, "").trim();

        setMessages(prev => [...prev, { sender: "Assistant", text: cleanedText }]);
        speak(cleanedText);
    }

    if (!recognitionRef.current) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "en-IN";  // Indian English - recognizes both English and Hindi accurately

        recognition.onstart = () => {
            setStatus("Listening");
            console.log("Recognition started");
        };

        recognition.onresult = (e) => {
            // Ignore results if the assistant is currently speaking
            if (isSpeaking.current) {
                console.log("Ignoring recognition result - assistant is speaking");
                return;
            }
            
            const currentIndex = e.resultIndex;
            const transcript = e.results[currentIndex][0].transcript.trim();
            
            // Ignore very short or empty transcripts (likely noise or echo)
            if (transcript.length < 2) {
                console.log("Ignoring short transcript:", transcript);
                return;
            }
            
            console.log("Patient said:", transcript);
            
            // Stop recognition immediately to prevent double-triggering
            recognition.stop();
            
            // Process the response
            aiResponse(transcript);
        };

        recognition.onend = () => {
            console.log("Recognition ended");
            // Only restart if we're supposed to be listening AND not speaking
            if (isListening.current && !isSpeaking.current) {
                try {
                    recognition.start();
                    console.log("Recognition restarted");
                } catch (e) {
                    console.log("Recognition restart failed (might already be running):", e.message);
                }
            } else {
                setStatus("Idle");
            }
        };

        recognition.onerror = (e) => {
            console.error("Recognition error:", e.error);
            setStatus("Idle");
        };

        recognitionRef.current = recognition;
    }

    async function fetchUserName() {
        try {
            const userId = localStorage.getItem("user_id");
            if (!userId) return;

            const response = await fetch(`${BACKEND_URL}/patient/${userId}`);
            if (response.ok) {
                const data = await response.json();
                setUserName(data.name);
            }
        } catch (error) {
            console.error("Error fetching user name:", error);
        }
    }

    function connect() {
        isListening.current = true;
        recognitionRef.current.start();
        symptomCount.current = 0;
        setHasGreeted(false);
        
        // Fetch user name for personalized greeting
        if (!userName) {
            fetchUserName();
        }
        
        console.log("Mic started");
    }

    async function disconnect() {
        console.log("Disconnecting...");
        
        // Set flags first to prevent any restarts
        isListening.current = false;
        isSpeaking.current = false;
        
        // Stop speech recognition
        try {
            if (recognitionRef.current) {
                recognitionRef.current.stop();
                console.log("Speech recognition stopped");
            }
        } catch (e) {
            console.log("Recognition stop error:", e);
        }
        
        // Cancel any ongoing speech synthesis
        try {
            window.speechSynthesis.cancel();
            console.log("Speech synthesis cancelled");
        } catch (e) {
            console.log("Speech synthesis cancel error:", e);
        }
        
        // Stop Azure TTS audio if playing
        try {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.currentTime = 0;
                audioRef.current.src = "";
                console.log("Audio playback stopped");
            }
        } catch (e) {
            console.log("Audio stop error:", e);
        }
        
        setStatus("Idle");
        console.log("Mic stopped");

        console.log("Full Conversation:");
        messages.forEach((msg, index) => {
            console.log(`${index + 1}. ${msg.sender}: ${msg.text}`);
        });

        const patientMessages = messages
            .filter(msg => msg.sender === "Patient")
            .map(msg => msg.text)
            .join(" ");

        const symptomPhrases = patientMessages
            .split(/[.?!]/)
            .map(s => s.trim())
            .filter(Boolean);

        console.log("Extracted Phrases:", symptomPhrases);

        try {
            console.log("Sending phrases to LangGraph:", symptomPhrases);
            const response = await fetch(`${BACKEND_URL}/run_langgraph`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phrases: symptomPhrases }),
            });

            const data = await response.json();
            console.log("Received LangGraph response:", data);
            navigate("/recommendation", { state: data });

        } catch (error) {
            console.error("Error during LangGraph execution:", error);
        }
    }

    const value = {
        connect,
        disconnect,
        messages,
        status,
        userName,
    };

    return (
        <datacontext.Provider value={value}>
            {children}
        </datacontext.Provider>
    );
}

export default UserContext;
