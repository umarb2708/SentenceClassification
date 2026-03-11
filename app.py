from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import re
from textblob import TextBlob
import nltk
from gtts import gTTS
import base64
from io import BytesIO
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure AI (Gemini)
api_key = os.getenv('GEMINI_API_KEY')
gemini_model = os.getenv('GEMINI_MODEL', 'gemini-pro')

if not api_key:
    print("Warning: GEMINI_API_KEY not set in .env file")
else:
    genai.configure(api_key=api_key)
    
# Initialize model with error handling
try:
    model = genai.GenerativeModel(gemini_model)
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None

def calculate_flesch_reading_ease(text):
    """Calculate Flesch Reading Ease score"""
    sentences = len(re.findall(r'\w+[.!?]', text))
    words = len(text.split())
    syllables = sum([count_syllables(word) for word in text.split()])
    
    if sentences == 0 or words == 0:
        return 0
    
    flesch_score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return flesch_score

def count_syllables(word):
    """Count syllables in a word"""
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            count += 1
        previous_was_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    
    return count

def classify_difficulty(text):
    """Classify sentence difficulty based on readability metrics"""
    flesch_score = calculate_flesch_reading_ease(text)
    word_count = len(text.split())
    avg_word_length = sum(len(word) for word in text.split()) / word_count if word_count > 0 else 0
    
    # Classification logic
    if flesch_score >= 70 and word_count <= 15 and avg_word_length < 5:
        return "Easy"
    elif flesch_score >= 50 and word_count <= 25:
        return "Medium"
    else:
        return "Hard"

def identify_complex_words_ai(text):
    """Use AI to identify complex words and suggest simpler alternatives"""
    if not model:
        return "Error: AI model not initialized. Check API key configuration."
    
    try:
        prompt = f"""Analyze the following sentence and identify complex words that might be difficult for dyslexic readers.
For each complex word, suggest a simpler alternative that maintains the meaning.

Sentence: {text}

Provide the response in this exact format:
Complex Word 1 -> Simple Alternative 1
Complex Word 2 -> Simple Alternative 2
(continue for all complex words found)

If no complex words are found, respond with: "No complex words found"
"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

def simplify_sentence_ai(text, complexity_analysis):
    """Use AI to create a simplified version of the sentence"""
    if not model:
        return "Error: AI model not initialized. Check API key configuration."
    
    try:
        prompt = f"""Simplify the following sentence for dyslexic readers by:
1. Breaking long sentences into shorter ones
2. Using simpler vocabulary
3. Maintaining the original meaning
4. Making it easier to read

Original sentence: {text}

Complex words identified: {complexity_analysis}

Provide ONLY the simplified sentence(s) as your response, without any explanations or additional text."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error simplifying text: {str(e)}"

def text_to_speech(text):
    """Convert text to speech and return as base64 encoded audio"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_base64 = base64.b64encode(audio_fp.read()).decode('utf-8')
        return audio_base64
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '').strip()
    
    if not text:
        return render_template('index.html', error="Please enter some text to analyze.")
    
    # Classify difficulty
    difficulty = classify_difficulty(text)
    flesch_score = calculate_flesch_reading_ease(text)
    
    # Identify complex words using AI
    complex_words_analysis = identify_complex_words_ai(text)
    
    # Simplify sentence using AI
    simplified_text = simplify_sentence_ai(text, complex_words_analysis)
    
    # Generate audio for original text
    audio_original = text_to_speech(text)
    
    # Generate audio for simplified text
    audio_simplified = text_to_speech(simplified_text)

    # Generate audio for complex words
    audio_complex_words = text_to_speech(complex_words_analysis)
    
    # Prepare results
    results = {
        'original_text': text,
        'difficulty': difficulty,
        'flesch_score': round(flesch_score, 2),
        'complex_words': complex_words_analysis,
        'simplified_text': simplified_text,
        'audio_original': audio_original,
        'audio_simplified': audio_simplified,
        'audio_complex_words': audio_complex_words,
        'word_count': len(text.split())
    }
    
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
