"""
Text preprocessing utilities for the healthcare voice assistant.
"""
import re
import string

def preprocess_text(text):
    """
    Preprocess text for better analysis.
    
    Args:
        text (str): Input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\?\!]', '', text)
    
    return text