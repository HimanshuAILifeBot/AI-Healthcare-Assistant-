import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  apiKey: import.meta.env.VITE_GEMINI_API_KEY,
});


// Initialize a conversation history
let conversationHistory = [];

async function run(prompt) {
  // Enhanced language detection - detects Hindi in both Devanagari and Roman script
  const hasDevanagari = /[\u0900-\u097F]/.test(prompt); // Check for Devanagari script
  
  // Common Hindi words/patterns in Roman script (Hinglish)
  const hindiPatterns = [
    /\b(mujhe|mujh|mai|main|mere|mera|meri|hai|hain|ho|tha|thi|the|ka|ki|ke|ko|se|ne|par|aur)\b/i,
    /\b(kya|kaise|kaisa|kaisi|kab|kaha|kahan|kyun|kyunki|lekin|acha|thik)\b/i,
    /\b(nahi|nahin|haan|ji|sir|madam|sahab|dard|bukhar|sir|pet|sar)\b/i,
    /\b(din|raat|subah|sham|kal|aaj|abhi|pehle|baad|bohot|bahut)\b/i
  ];
  
  // Check if prompt contains common Hindi words in Roman script
  const hasHindiWords = hindiPatterns.some(pattern => pattern.test(prompt.toLowerCase()));
  
  let languageInstruction = "";
  if (hasDevanagari) {
    // Devanagari script detected - definitely Hindi
    languageInstruction = "RESPOND IN HINDI ONLY (हिंदी में जवाब दें)";
  } else if (hasHindiWords) {
    // Hindi words in Roman script detected - Hinglish
    languageInstruction = "RESPOND IN HINDI ONLY (हिंदी में जवाब दें)";
  } else {
    // English
    languageInstruction = "RESPOND IN ENGLISH ONLY";
  }
  
  // Add the current user message with explicit language marker
  conversationHistory.push(`User [${languageInstruction}]: ${prompt}`);
  
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: conversationHistory.join('\n'), // Include the full conversation history
    config: {
      systemInstruction: "You are a helpful AI Medical Assistant.\n\n" +
"🔴 ABSOLUTE LANGUAGE RULE - FOLLOW STRICTLY:\n" +
"1. Check the LAST user message for [RESPOND IN ENGLISH ONLY] or [RESPOND IN HINDI ONLY]\n" +
"2. If it says ENGLISH ONLY → Respond ENTIRELY in English\n" +
"3. If it says HINDI ONLY → Respond ENTIRELY in Hindi (Devanagari: हिंदी)\n" +
"4. IGNORE all previous conversation languages\n" +
"5. The language can SWITCH at any time - always follow the LATEST instruction\n" +
"6. NEVER mix languages\n\n" +
`⚡ CURRENT INSTRUCTION: ${languageInstruction}\n\n` +
"Your job is to ask follow-up questions one at a time to gather the patient's symptoms.\n" +
"Wait for the patient's response before asking the next question. Do not ask multiple questions together.\n" +
"Do not decide or mention any medical specialist. Do not include any tags or hidden signals.\n" +
"Once you are confident you have collected all symptoms, say:\n" +
"- In English: 'I have thoroughly examined your symptoms. Now you can click on disconnect.'\n" +
"- In Hindi: 'मैंने आपके लक्षणों की अच्छी तरह से जांच कर ली है। अब आप डिस्कनेक्ट पर क्लिक कर सकते हैं।'",
    },
  });
  
  // Log the response for debugging
  console.log(response);

  // Extract the generated text from the response
  const generatedText = response?.candidates?.[0]?.content?.parts?.[0]?.text || "No response available";
  
  // Add the agent's response to the conversation history
  conversationHistory.push(`Agent: ${generatedText}`);
  
  return generatedText;
}

export default run;
