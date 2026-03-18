# Sentence Classification and Simplification System - Project Report

---

## Table of Contents
1. [Introduction](#introduction)
2. [Project Architecture](#project-architecture)
3. [Module-wise Code Explanation](#module-wise-code-explanation)
4. [Working Flow](#working-flow)
5. [Technology Stack](#technology-stack)
6. [Key Features](#key-features)

---

## Introduction

### Project Overview

The **Sentence Classification and Simplification System** is a web-based application designed to improve reading accessibility for dyslexic readers. The application leverages artificial intelligence (Google Gemini AI) to analyze sentence complexity, identify challenging words, and automatically generate simplified versions while maintaining semantic meaning.

### Problem Statement

Dyslexic readers face significant challenges when reading complex sentences with:
- Long, intricate sentence structures
- Advanced vocabulary and complex terminology
- Dense information presentation
- Lack of audio support for pronunciation

### Solution Provided

This system addresses these challenges by:
- **Automated Analysis**: Identifies difficult words using AI
- **Readability Metrics**: Calculates Flesch Reading Ease score for objective difficulty assessment
- **Smart Simplification**: Generates simplified versions maintaining original meaning
- **Accessibility Features**: Provides text-to-speech audio for all content
- **User-Friendly Interface**: Clean, accessible web interface optimized for readability

### Target Users
- Dyslexic readers seeking reading assistance
- Educators teaching students with learning disabilities
- Content creators wanting to make materials more accessible
- General users wanting to understand complex text

---

## Project Architecture

```
SentenceClassification/
│
├── 📄 Configuration & Setup Files
│   ├── app.py                    # Main Flask application (Core logic)
│   ├── start_app.py              # Application starter with validation
│   ├── requirements.txt           # Python dependencies
│   ├── setup.bat                 # Windows setup automation
│   └── start_app.bat             # Windows launcher script
│
├── 📁 templates/                 # HTML Templates (Frontend)
│   ├── index.html                # Input form page
│   └── result.html               # Results display page
│
├── 📁 static/                    # Static Assets (Frontend)
│   └── style.css                 # Application styling
│
└── 📄 Documentation
    ├── README.md                 # User documentation
    ├── QUICKSTART.md            # Quick start guide
    └── REPORT.md                # This file - technical documentation
```

---

## Module-wise Code Explanation

### 1. **app.py** - Core Application Logic

**Purpose**: Main Flask application containing all business logic for text analysis, simplification, and audio generation.

#### Key Components:

##### a) **Imports & Configuration**
```python
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os, re, json
from textblob import TextBlob
import nltk
from gtts import gTTS          # Google Text-to-Speech
import base64
from io import BytesIO
import google.generativeai as genai  # Google Gemini AI
```

**What it does**: 
- Initializes Flask web framework for HTTP routing
- Loads environment variables from .env file for API keys
- Imports NLP libraries for text processing
- Sets up Google Gemini AI for natural language understanding

##### b) **AI Configuration**
```python
api_key = os.getenv('GEMINI_API_KEY')
gemini_model = os.getenv('GEMINI_MODEL', 'gemini-pro')
genai.configure(api_key=api_key)
model = genai.GenerativeModel(gemini_model)
```

**What it does**: 
- Retrieves API key from environment variables
- Initializes the Gemini AI model for text analysis
- Implements error handling for missing API configuration

---

##### c) **Function: `calculate_flesch_reading_ease(text)`**

**Purpose**: Calculates readability score using Flesch Reading Ease formula

**Algorithm**:
```
Flesch Score = 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
```

**What it does**:
- Counts sentences (ending with `.`, `!`, `?`)
- Counts total words in text
- Calculates syllables for each word
- Returns numeric score (0-100): Higher = easier to read

**Score Interpretation**:
- 90-100: Very Easy (5th grade)
- 80-89: Easy (6th grade)
- 70-79: Fairly Easy (7th grade)
- 60-69: Standard (8th-9th grade)
- 50-59: Fairly Difficult (High school)
- 0-49: Difficult (College level and above)

**Code Flow**:
1. Extract sentences using regex pattern `\w+[.!?]`
2. Split text into words
3. For each word, count syllables
4. Apply Flesch formula
5. Return calculated score

---

##### d) **Function: `count_syllables(word)`**

**Purpose**: Counts syllables in a single word

**What it does**:
1. Converts word to lowercase for processing
2. Iterates through each character
3. Counts vowel transitions (ay → 2 syllables)
4. Subtracts 1 if word ends with 'e' (silent e rule)
5. Ensures minimum of 1 syllable

**Example**:
- "example" → e-x-a-m-p-l-e → 3 syllables
- "beautiful" → beau-ti-ful → 3 syllables

**Code Logic**:
```
- Vowels: a, e, i, o, u, y
- Count vowel groups (consecutive vowels = 1 syllable)
- Apply silent 'e' rule
- Minimum return = 1
```

---

##### e) **Function: `classify_difficulty(text)`**

**Purpose**: Classifies sentence difficulty into three categories

**Classification Rules**:
```
EASY:
  - Flesch Score ≥ 70 AND
  - Word Count ≤ 15 AND
  - Average Word Length < 5 characters

MEDIUM:
  - Flesch Score ≥ 50 AND
  - Word Count ≤ 25

HARD:
  - All other cases (low Flesch score or long sentences)
```

**What it does**:
1. Calculates Flesch Reading Ease score
2. Counts total words
3. Calculates average word length
4. Applies classification rules
5. Returns: "Easy", "Medium", or "Hard"

**Example**:
- Input: "The cat sat on the mat" → Easy (simple words, short sentence)
- Input: "The phenomenon occurred" → Hard (longer words, complex)

---

##### f) **Function: `identify_complex_words_ai(text)`**

**Purpose**: Uses Google Gemini AI to identify complex words and suggest simpler alternatives

**What it does**:
1. Constructs AI prompt asking to identify complex words
2. Specifies output format: "Complex Word → Simple Alternative"
3. Sends request to Gemini model
4. Returns AI-generated word simplification pairs
5. Handles errors gracefully

**AI Prompt Strategy**:
- Instructs AI to focus on "dyslexic readers" perspective
- Requests specific format for parsing
- Returns "No complex words found" if text is simple

**Example Output**:
```
phenomenon → event
bioluminescence → light production
ingenuity → cleverness
```

---

##### g) **Function: `simplify_sentence_ai(text, complexity_analysis)`**

**Purpose**: Uses AI to create simplified version of complex sentences

**What it does**:
1. Receives original text and AI's complexity analysis
2. Constructs detailed simplification prompt with tactics:
   - Break long sentences into shorter ones
   - Use simpler vocabulary
   - Maintain original meaning
   - Improve readability
3. Sends to Gemini model
4. Returns simplified text
5. Returns only simplified output without explanations

**Simplification Tactics Applied by AI**:
- Replace advanced words with common alternatives
- Split compound sentences into simple ones
- Remove redundant phrases
- Clarify ambiguous references
- Maintain factual accuracy

**Example**:
- Original: "The phenomenon of bioluminescence in marine organisms is captivating"
- Simplified: "Some sea animals can make their own light. This is really interesting"

---

##### h) **Function: `text_to_speech(text)`**

**Purpose**: Converts text to audio and returns as base64-encoded MP3

**What it does**:
1. Uses Google Text-to-Speech (gTTS) library
2. Generates natural-sounding audio in English
3. Stores audio in memory buffer
4. Encodes audio to base64 for embedding in HTML
5. Returns base64 string (or None on error)

**Audio Features**:
- Language: English
- Speed: Normal (not slow)
- Format: MP3 (playable in browsers)
- Encoding: Base64 (embeddable directly in HTML)

**Why Base64 Encoding**:
- Allows embedding audio directly in HTML responses
- No need for separate file storage
- Reduces server requests
- Improves performance

---

##### i) **Route: `@app.route('/')`**

**Purpose**: Displays the main input form

**What it does**:
1. Responds to GET request for root URL
2. Renders `index.html` template
3. Displays form for text input
4. Shows "How It Works" guide

**URL**: `http://localhost:5000/`

---

##### j) **Route: `@app.route('/analyze', methods=['POST'])`**

**Purpose**: Main analysis endpoint that processes user input

**What it does**:
1. Receives text from form submission
2. Validates text (not empty)
3. Executes analysis pipeline:
   - Classifies difficulty level
   - Calculates Flesch Reading Ease score
   - Identifies complex words using AI
   - Simplifies sentence using AI
   - Generates audio for original text
   - Generates audio for simplified text
   - Generates audio for complex words analysis
4. Packages all results
5. Renders `result.html` with results

**Analysis Pipeline Flow**:
```
User Input
    ↓
Validate Text
    ↓
Calculate Flesch Score
    ↓
Classify Difficulty
    ↓
[AI] Identify Complex Words
    ↓
[AI] Simplify Sentence
    ↓
Generate Audio × 3
    ↓
Package Results
    ↓
Render Result Page
```

**Results Object Structure**:
```python
{
    'original_text': str,           # User input
    'difficulty': str,              # Easy/Medium/Hard
    'flesch_score': float,          # 0-100
    'complex_words': str,           # AI analysis
    'simplified_text': str,         # AI simplified version
    'audio_original': base64,       # MP3 audio
    'audio_simplified': base64,     # MP3 audio
    'audio_complex_words': base64,  # MP3 audio
    'word_count': int               # Total words
}
```

---

### 2. **start_app.py** - Application Starter with Validation

**Purpose**: Pre-flight checks and safe application startup

#### Key Functions:

##### a) **Function: `check_requirements()`**

**What it does**:
1. Verifies `app.py` exists
2. Verifies `.env` file exists
3. Verifies `templates/` directory exists
4. Verifies `static/` directory exists
5. Returns lists of errors and warnings

**Returns**:
- Errors: Critical issues that prevent startup
- Warnings: Recoverable issues (e.g., missing .env)

**Validation Checklist**:
```
✓ app.py exists
✓ .env file present
✓ templates/ directory exists
✓ static/ directory exists
```

---

##### b) **Function: `check_environment()`**

**What it does**:
1. Loads .env file
2. Checks if GEMINI_API_KEY is set
3. Validates it's not the default placeholder
4. Prompts user to configure API key if missing
5. Allows user to continue or exit

**API Key Validation**:
- Checks for empty value
- Checks for default placeholder "your_gemini_api_key_here"
- Provides Google AI Studio link for users

---

##### c) **Function: `main()`**

**What it does**:
1. Displays startup banner
2. Runs `check_requirements()`
3. Reports errors (exits if critical)
4. Reports warnings
5. Runs `check_environment()`
6. Imports and runs Flask app
7. Provides server URL to user

**Startup Output**:
```
==================================================
  Sentence Classification System
  Starting Application...
==================================================

✅ All checks passed!

Starting Flask server...
--------------------------------------------------

🌐 Application will be available at:
   http://localhost:5000
   http://127.0.0.1:5000

Press Ctrl+C to stop the server
==================================================
```

---

### 3. **templates/index.html** - Input Form Page

**Purpose**: First page users see; provides text input interface

#### Page Structure:

##### a) **Header Section**
- Application title: "📚 Sentence Simplification System"
- Subtitle: "Making reading easier for Dyslexic Readers"

##### b) **Main Content Area**

**Form Section**:
- Text input label
- Large textarea (6 rows)
- Placeholder with example complex sentence
- Submit button: "Analyze & Simplify ✨"

**Form Attributes**:
```html
<form method="POST" action="/analyze">
    <textarea 
        id="text" 
        name="text" 
        rows="6" 
        placeholder="Example text..."
        required
    ></textarea>
    <button type="submit">Analyze & Simplify ✨</button>
</form>
```

**Form Flow**:
1. User enters or pastes text
2. Clicks submit button
3. POST request sent to `/analyze` route
4. Server processes text
5. Redirects to result page

---

##### c) **Info Card - "How It Works"**

**Step-by-Step Guide** (4 steps):

| Step | Title | Description |
|------|-------|-------------|
| 1 | Enter Text | User types or pastes sentence |
| 2 | AI Analysis | System identifies complex words and difficulty level |
| 3 | Simplification | System creates easier version |
| 4 | Audio Support | User can listen to pronunciation |

---

##### d) **Error Handling**

**Error Display**:
```html
{% if error %}
<div class="error-message">
    ⚠️ {{ error }}
</div>
{% endif %}
```

**Error Cases**:
- Empty text submission
- AI model not initialized
- API configuration issues

---

### 4. **templates/result.html** - Results Display Page

**Purpose**: Displays analysis results with multiple views and audio support

#### Result Components:

##### a) **Navigation**
- Back link: "← Analyze Another Sentence"
- Returns to index.html for new analysis

##### b) **Difficulty Classification Card**

**Content**:
- Visual badge with emoji
- Color-coded: Green (Easy), Yellow (Medium), Red (Hard)
- Flesch Reading Ease score
- Word count metric

**Badge HTML**:
```html
<div class="classification-badge {{ difficulty.lower() }}">
    {% if difficulty == "Easy" %}
        ✅ Easy
    {% elif difficulty == "Medium" %}
        ⚠️ Medium
    {% else %}
        🔴 Hard
    {% endif %}
</div>
```

---

##### c) **Original Text Card**

**Displays**:
- User's original input text
- Audio playback button: "🔊 Listen to Original"
- Audio embedded as base64 MP3

**Audio Integration**:
```html
<audio id="audio-original" preload="none">
    <source src="data:audio/mp3;base64,{{ audio_original }}" type="audio/mp3">
</audio>
```

---

##### d) **Complex Words Analysis Card**

**Displays**:
- AI-identified complex words
- Suggested simpler alternatives
- Format: "Complex Word → Simple Alternative"
- Audio for complex words analysis

**Content Example**:
```
phenomenon → event
bioluminescence → light production
ingenuity → cleverness
```

---

##### e) **Simplified Version Card** (Highlighted)

**Displays**:
- AI-generated simplified text
- Primary focus of results page
- Audio playback button: "🔊 Listen to Simplified Version"
- Higher visual prominence than other cards

---

##### f) **Side-by-Side Comparison Section**

**Displays**:
- Original text and simplified text in columns
- Easy visual comparison
- Highlights differences

**Purpose**: Users can immediately see improvements in readability

---

##### g) **JavaScript Functionality**

**Audio Playback Function** (`playAudio()`):
```javascript
function playAudio(id) {
    const audio = document.getElementById('audio-' + id);
    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
}
```

**What it does**:
- Plays/pauses audio on button click
- IDs: 'audio-original', 'audio-simplified', 'audio-complex-words'
- Toggles between play and pause states

---

### 5. **static/style.css** - Application Styling

**Purpose**: Makes application visually appealing and accessible for dyslexic readers

#### Design Principles:

##### a) **Typography for Dyslexia**
```css
font-family: 'OpenDyslexic', sans-serif;  /* Dyslexia-friendly font */
```

**Features**:
- OpenDyslexic font reduces visual confusion
- Increased letter spacing
- Heavier baseline for clarity

##### b) **Color Scheme**

**Colors Used**:
- Primary: Blue (Trust, calm)
- Success/Easy: Green (#4CAF50)
- Warning/Medium: Orange (#FF9800)
- Danger/Hard: Red (#F44336)
- Background: Light gray (Low contrast glare)

---

##### c) **Layout Structure**

**Container System**:
- Max-width: 1200px (readable line length)
- Centered with margin: auto
- Padding: 20px (breathing room)

**Cards**:
- White background
- Box shadow for depth
- Rounded corners (12px)
- Padding: 24px (comfortable reading space)
- Margin: 20px bottom (vertical rhythm)

---

##### d) **Responsive Design**

**Breakpoints**:
- Mobile: < 600px
- Tablet: 600px - 1024px
- Desktop: > 1024px

**Mobile Optimizations**:
- Stack columns vertically
- Adjust font sizes
- Reduce padding on small screens
- Full-width textarea

---

##### e) **Accessibility Features**

**Readability Enhancements**:
- Line height: 1.8 (increased spacing)
- Letter spacing: 0.1em (reduced confusion)
- Font weight: 400-700 (clear hierarchy)
- Text alignment: Left (easier for dyslexic readers)

**Visual Hierarchy**:
- Large headings (h1: 2.5rem)
- Medium subheadings (h2: 2rem)
- Body text: 1rem minimum
- Clear contrast ratios (WCAG AA compliant)

---

##### f) **Interactive Elements**

**Buttons**:
- `.btn-primary`: Blue background, white text
- `.btn-audio`: Green background for action-oriented tasks
- Hover effects for user feedback
- Rounded corners for modern look
- Min-height: 44px (thumb-friendly mobile targets)

**Textarea**:
- Large minimum height: 150px
- Padding for comfort: 12px
- Placeholder text: Helpful example
- Focus state: Blue border highlight

---

##### g) **Content Sections**

**Result Cards**:
- `.result-card`: Standard result display
- `.highlight`: Emphasized card for simplified text (yellow background)
- `.comparison-grid`: Side-by-side text comparison

**Text Boxes**:
- `.original-text`: Light gray background
- `.simplified-text`: Light green background
- `.complex-words`: Light blue background
- Border: Left accent color bar (3px)

---

### 6. **requirements.txt** - Python Dependencies

**Purpose**: Lists all Python packages needed to run the application

#### Dependencies Breakdown:

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework for HTTP routing and rendering |
| python-dotenv | 1.0.0 | Load environment variables from .env file |
| google-generativeai | ≥0.3.0 | Google Gemini AI API client |
| gTTS | 2.5.0 | Google Text-to-Speech for audio generation |
| textblob | 0.18.0 | NLP library for text processing (optional) |
| nltk | 3.8.1 | Natural Language Toolkit for tokenization |

**Installation**:
```bash
pip install -r requirements.txt
```

---

### 7. **setup.bat** - Windows Setup Automation

**Purpose**: Automated setup script for Windows users (one-time)

**What it does**:
1. Checks if Python is installed
2. Creates virtual environment (`venv/`)
3. Activates virtual environment
4. Installs all dependencies from requirements.txt
5. Creates `.env` file from template
6. Displays completion message

**Usage**:
```batch
setup.bat
```

**User Steps After Setup**:
1. Open `.env` file
2. Add GEMINI_API_KEY from Google AI Studio
3. Save file
4. Run `start_app.bat`

---

### 8. **start_app.bat** - Windows Launcher

**Purpose**: Quick launch script for Windows users

**What it does**:
1. Activates virtual environment
2. Runs start_app.py with Python
3. Starts Flask server

**Usage**:
```batch
start_app.bat
```

**Result**: Opens application at `http://localhost:5000`

---

## Working Flow

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER WORKFLOW                                 │
└─────────────────────────────────────────────────────────────────┘

1. APPLICATION STARTUP
   ┌─────────────────────┐
   │  Run: start_app.bat │
   │  or: python start_app.py  │
   └─────────────────────┘
           │
           ↓
   ┌──────────────────────────────┐
   │ start_app.py Validation      │
   │ • Check app.py exists        │
   │ • Check .env file exists     │
   │ • Check templates/ exists    │
   │ • Check static/ exists       │
   │ • Verify API key configured  │
   └──────────────────────────────┘
           │
           ↓ (All checks pass)
   ┌──────────────────────────────┐
   │ Flask Server Started         │
   │ ✓ Running on localhost:5000  │
   └──────────────────────────────┘

2. USER ACCESSES APPLICATION
   ┌──────────────────────────────┐
   │ User opens http://localhost:5000 │
   └──────────────────────────────┘
           │
           ↓
   ┌──────────────────────────────┐
   │ GET / Route                  │
   │ Renders: index.html          │
   │ Displays: Input form page    │
   └──────────────────────────────┘

3. USER ENTERS TEXT
   ┌─────────────────────────────────────────┐
   │ User types/pastes sentence in textarea  │
   │ Example: "The phenomenon of              │
   │ bioluminescence is captivating"          │
   └─────────────────────────────────────────┘
           │
           ↓
   ┌──────────────────────────────┐
   │ User clicks submit button    │
   │ "Analyze & Simplify ✨"      │
   └──────────────────────────────┘

4. SERVER-SIDE ANALYSIS (POST /analyze)
   ┌──────────────────────────────────────────────────────────────┐
   │                   ANALYSIS PIPELINE                           │
   └──────────────────────────────────────────────────────────────┘
   
   STEP 1: Text Validation
   ┌─────────────────────────────────────┐
   │ Check: Text not empty               │
   │ If empty: Return error message      │
   └─────────────────────────────────────┘
           │
           ↓ (Valid)
   
   STEP 2: Calculate Flesch Reading Ease Score
   ┌──────────────────────────────────────┐
   │ Function: calculate_flesch_reading_ease(text) │
   │ • Count sentences                    │
   │ • Count words                        │
   │ • Count syllables                    │
   │ • Apply formula: 206.835 - 1.015     │
   │   (words/sentences) - 84.6            │
   │   (syllables/words)                   │
   │ • Return: Score 0-100                │
   │ Example: 45.32 (Fairly Difficult)    │
   └──────────────────────────────────────┘
           │
           ↓
   
   STEP 3: Classify Difficulty Level
   ┌──────────────────────────────────────┐
   │ Function: classify_difficulty(text) │
   │                                       │
   │ Rule 1 - EASY:                        │
   │   • Flesch Score ≥ 70 AND            │
   │   • Word Count ≤ 15 AND              │
   │   • Avg Word Length < 5               │
   │                                       │
   │ Rule 2 - MEDIUM:                      │
   │   • Flesch Score ≥ 50 AND            │
   │   • Word Count ≤ 25                  │
   │                                       │
   │ Rule 3 - HARD:                        │
   │   • All other cases                  │
   │                                       │
   │ Return: "Easy"/"Medium"/"Hard"       │
   │ Example: "Hard"                      │
   └──────────────────────────────────────┘
           │
           ↓
   
   STEP 4: Identify Complex Words (AI)
   ┌────────────────────────────────────────┐
   │ Function: identify_complex_words_ai()  │
   │                                         │
   │ AI Prompt:                              │
   │ "Analyze this sentence. Identify      │
   │  complex words difficult for            │
   │  dyslexic readers. For each complex    │
   │  word, suggest a simpler alternative"  │
   │                                         │
   │ Send to: Google Gemini AI Model        │
   │ Response Format:                        │
   │ Complex Word → Simple Alternative      │
   │ phenomenon → event                      │
   │ bioluminescence → light creation       │
   │ captivating → fascinating               │
   │                                         │
   │ Return: AI Analysis text               │
   └────────────────────────────────────────┘
           │
           ↓
   
   STEP 5: Simplify Sentence (AI)
   ┌────────────────────────────────────────┐
   │ Function: simplify_sentence_ai()       │
   │                                         │
   │ AI Prompt:                              │
   │ "Simplify this sentence:               │
   │  - Break long sentences into short     │
   │  - Use simpler vocabulary              │
   │  - Maintain original meaning           │
   │  - Make it easier to read              │
   │                                         │
   │  Original: {text}                      │
   │  Complex words: {analysis}"            │
   │                                         │
   │ Send to: Google Gemini AI Model        │
   │                                         │
   │ Example Output:                         │
   │ "Some sea animals can make their      │
   │  own light. This is really interesting"│
   │                                         │
   │ Return: Simplified text                │
   └────────────────────────────────────────┘
           │
           ↓
   
   STEP 6: Generate Audio (Text-to-Speech)
   ┌────────────────────────────────────────┐
   │ Function: text_to_speech()             │
   │ Called 3 times:                         │
   │                                         │
   │ 1. For Original Text                   │
   │    • Input: Original sentence          │
   │    • Output: Base64 MP3 audio          │
   │                                         │
   │ 2. For Simplified Text                 │
   │    • Input: Simplified sentence        │
   │    • Output: Base64 MP3 audio          │
   │                                         │
   │ 3. For Complex Words Analysis          │
   │    • Input: Complex words analysis     │
   │    • Output: Base64 MP3 audio          │
   │                                         │
   │ Process:                                │
   │ • Convert text to speech using gTTS    │
   │ • Store in memory buffer               │
   │ • Encode to Base64                     │
   │ • Embed directly in HTML response      │
   └────────────────────────────────────────┘
           │
           ↓
   
   STEP 7: Package Results
   ┌─────────────────────────────────────┐
   │ Create results dictionary:           │
   │ {                                     │
   │   'original_text': str,              │
   │   'difficulty': str,                 │
   │   'flesch_score': float,             │
   │   'complex_words': str,              │
   │   'simplified_text': str,            │
   │   'audio_original': base64,          │
   │   'audio_simplified': base64,        │
   │   'audio_complex_words': base64,     │
   │   'word_count': int                  │
   │ }                                     │
   └─────────────────────────────────────┘

5. RENDER RESULTS PAGE
   ┌─────────────────────────────────────┐
   │ Render: result.html                 │
   │ Pass: results dictionary            │
   │ Display:                             │
   │ • Difficulty badge with color       │
   │ • Flesch score & word count         │
   │ • Original text + audio button      │
   │ • Complex words + audio button      │
   │ • Simplified text + audio button    │
   │ • Side-by-side comparison           │
   │ • "Analyze Another" link            │
   └─────────────────────────────────────┘

6. USER VIEWS AND INTERACTS WITH RESULTS
   ┌─────────────────────────────────────┐
   │ User can:                            │
   │ • Read simplified version           │
   │ • Play audio for pronunciation      │
   │ • Review complex words identified   │
   │ • Compare original vs simplified    │
   │ • Click "Analyze Another Sentence"  │
   │   (Returns to step 3)               │
   └─────────────────────────────────────┘
```

### Data Flow Diagram

```
User Input
    ↓
├─→ Flesch Score Calculation
│   └─→ Sentence/Word/Syllable Count
│
├─→ Difficulty Classification
│   └─→ Easy/Medium/Hard Label
│
├─→ AI: Complex Words Identification
│   ├─→ Gemini API Request
│   └─→ Word → Alternative Mapping
│
├─→ AI: Sentence Simplification
│   ├─→ Gemini API Request (with context)
│   └─→ Simplified Text Generation
│
├─→ Text-to-Speech (3 times)
│   ├─→ Original Text → Audio 1
│   ├─→ Simplified Text → Audio 2
│   └─→ Complex Words → Audio 3
│       Each: Text → gTTS → MP3 → Base64
│
└─→ Results Package
    └─→ Render result.html
        └─→ Display to User
```

---

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0 (Python web framework)
- **Language**: Python 3.8+
- **NLP**: NLTK 3.8.1, TextBlob 0.18.0 (text processing)
- **AI**: Google Generative AI (Gemini Pro model)
- **Audio**: gTTS 2.5.0 (Google Text-to-Speech)
- **Environment**: python-dotenv 1.0.0 (API key management)

### Frontend
- **HTML**: HTML5 (semantic markup)
- **CSS**: CSS3 (responsive styling)
- **JavaScript**: Vanilla JS (audio controls)
- **Fonts**: OpenDyslexic (dyslexia-friendly typography)
- **Icons**: Unicode emojis

### Hosting
- **Server**: Local Flask development server (localhost:5000)
- **Database**: None (stateless processing)
- **Storage**: All data processed stateless (not stored)

### External APIs
- **Google Gemini AI**: Text analysis and simplification
- **Google Text-to-Speech**: Audio generation

---

## Key Features

### 1. AI-Powered Text Analysis
- **Google Gemini Integration**: Advanced NLP for understanding text complexity
- **Context-Aware**: Understands specific needs of dyslexic readers
- **Iterative Improvement**: Prompt engineering for better results

### 2. Readability Metrics
- **Flesch Reading Ease Score**: Standard 0-100 readability metric
- **Difficulty Classification**: Three-tier system (Easy/Medium/Hard)
- **Syllable Counting**: Algorithm implementation for accuracy

### 3. Automatic Simplification
- **Vocabulary Replacement**: Complex words → Simple alternatives
- **Sentence Restructuring**: Long sentences → Shorter, clearer sentences
- **Meaning Preservation**: AI ensures original content isn't altered

### 4. Accessibility Features
- **Text-to-Speech**: Audio for all content (original, simplified, complex words)
- **OpenDyslexic Font**: Specially designed for dyslexic readers
- **High Contrast**: WCAG AA compliant color schemes
- **Responsive Design**: Works on desktop, tablet, mobile

### 5. User Experience
- **Simple Interface**: Single-page form input
- **Immediate Results**: No page reload; quick processing
- **Visual Feedback**: Color-coded difficulty badges
- **Multiple Formats**: Text, metrics, audio options

### 6. Error Handling
- **Validation**: Empty text checking
- **API Fallback**: Graceful error messages if AI unavailable
- **Configuration Checks**: Pre-startup validation in start_app.py

---

## Summary

The **Sentence Classification and Simplification System** is a comprehensive solution using:
- **Backend Logic**: Flask for routing, NLTK/TextBlob for NLP, Gemini for AI
- **Frontend Design**: Accessible HTML/CSS optimized for dyslexia
- **Audio Integration**: Base64-encoded MP3 for seamless playback
- **Automation**: Batch scripts for easy Windows setup and launch

This creates an end-to-end system helping dyslexic readers understand complex text through simplification, metrics, and audio support.

---

## Configuration & Deployment

### Environment Setup
Create `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-pro
```

### Running the Application
**Windows**:
```batch
setup.bat          # One-time setup
start_app.bat      # Launch (every time)
```

**Manual**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python start_app.py
```

### Accessing the Application
- URL: http://localhost:5000
- Input: Any English sentence
- Output: Analysis, simplification, audio files

---

## Future Enhancements

Potential improvements for next versions:
1. **Multiple Languages**: Support beyond English
2. **Saving Results**: Export simplified text and audio
3. **History**: Store previous analyses
4. **Customization**: User preferences for difficulty levels
5. **Batch Processing**: Analyze multiple sentences at once
6. **Mobile App**: Native iOS/Android applications
7. **Advanced Metrics**: Readability levels, readability guides
8. **Alternative AI**: Support for other AI models (OpenAI GPT, etc.)

---

**Report Generated**: March 18, 2026  
**Project**: Sentence Classification and Simplification System  
**Version**: 1.0  
**Target Audience**: Dyslexic readers, educators, developers

