# Sentence Classification and Simplification System 📚

A web-based application designed to help dyslexic readers by analyzing sentence difficulty, identifying complex words using AI, and providing simplified alternatives with audio pronunciation support.

## Features ✨

- **AI-Powered Analysis**: Uses Google Gemini AI to identify complex words and suggest simpler alternatives
- **Difficulty Classification**: Categorizes sentences as Easy, Medium, or Hard based on readability metrics
- **Automatic Simplification**: Creates simplified versions of complex sentences while maintaining meaning
- **Text-to-Speech**: Audio pronunciation for both original and simplified text
- **User-Friendly Interface**: Clean, accessible design optimized for readability
- **Flesch Reading Ease Score**: Provides quantitative readability metrics

## Project Structure 📁

```
SentenceClassification/
│
├── app.py                 # Main Flask application
├── start_app.py          # Application starter with checks
├── setup.bat             # Automated setup script (Windows)
├── start_app.bat         # Quick start script (Windows)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
│
├── templates/
│   ├── index.html        # Input page
│   └── result.html       # Results page
│
└── static/
    └── style.css         # Stylesheet
```

## Quick Start 🚀 (Recommended)

### Easy Setup with Scripts

1. **Run the setup script** (one-time setup):
   ```batch
   setup.bat
   ```
   This will:
   - Check if Python is installed
   - Create a virtual environment
   - Install all dependencies
   - Create .env file from template

2. **Configure your API key**:
   - Open `.env` file in a text editor
   - Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace `your_gemini_api_key_here` with your actual API key
   - Save the file

3. **Start the application**:
   ```batch
   start_app.bat
   ```
   Or use Python directly:
   ```batch
   python start_app.py
   ```

4. **Open your browser** to `http://localhost:5000`

That's it! 🎉

---

## Manual Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (free tier available)

### Step 1: Clone or Download the Project

```bash
cd c:\Users\ub080081\Box\Personal\Website\SentenceClassification
```

### Step 2: Create a Virtual Environment (Recommended)

```batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### Step 3: Install Dependencies

```batch
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```batch
   copy .env.example .env
   ```

2. Get your Gemini API key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

3. Edit the `.env` file and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Step 5: Run the Application

```batch
python app.py
```

The application will start on `http://localhost:5000`

## Usage 📖

1. **Enter Text**: Open your browser and navigate to `http://localhost:5000`
2. **Input Sentence**: Type or paste a sentence in the text area
3. **Analyze**: Click the "Analyze & Simplify" button
4. **View Results**: See the difficulty classification, complex words, and simplified version
5. **Listen**: Click the speaker buttons to hear the pronunciation

## How It Works 🔧

### 1. Readability Analysis
- Calculates Flesch Reading Ease score
- Counts syllables, words, and sentences
- Analyzes average word length

### 2. AI-Powered Word Identification
Uses Google Gemini to:
- Identify complex words
- Suggest simpler alternatives
- Maintain contextual meaning

### 3. Sentence Simplification
- Breaks long sentences into shorter ones
- Replaces complex vocabulary
- Preserves original meaning

### 4. Text-to-Speech
- Converts text to audio using gTTS (Google Text-to-Speech)
- Plays directly in browser
- Available for both original and simplified versions

## API Configuration 🔑

### Using Google Gemini (Default)
The application is configured to use Google Gemini API by default. Get your free API key at [Google AI Studio](https://makersuite.google.com/app/apikey).

### Alternative: Using LLaMA
To use LLaMA instead, modify `app.py`:

1. Install additional dependencies:
   ```bash
   pip install llama-cpp-python
   ```

2. Update the AI initialization code in `app.py`

3. Add LLaMA configuration to `.env`

## Customization 🎨

### Adjusting Difficulty Thresholds
Edit the `classify_difficulty()` function in `app.py`:

```python
def classify_difficulty(text):
    flesch_score = calculate_flesch_reading_ease(text)
    
    # Adjust these thresholds as needed
    if flesch_score >= 70:  # Easy threshold
        return "Easy"
    elif flesch_score >= 50:  # Medium threshold
        return "Medium"
    else:
        return "Hard"
```

### Changing the AI Model
Modify the model selection in `app.py`:

```python
# Change model version
model = genai.GenerativeModel('gemini-pro')
# Or try: 'gemini-1.5-pro', 'gemini-1.5-flash'
```

### Styling
Edit `static/style.css` to customize colors, fonts, and layout.

## Troubleshooting 🔧

### Common Issues

**Issue**: ModuleNotFoundError
```
Solution: Make sure all dependencies are installed:
pip install -r requirements.txt
```

**Issue**: API Key Error
```
Solution: Check that your .env file exists and contains a valid API key:
GEMINI_API_KEY=your_key_here
```

**Issue**: Audio Not Playing
```
Solution: Ensure gTTS is properly installed:
pip install gTTS --upgrade
```

**Issue**: Port Already in Use
```
Solution: Change the port in app.py:
app.run(debug=True, port=5001)
```

## Dependencies 📦

- **Flask**: Web framework
- **python-dotenv**: Environment variable management
- **google-generativeai**: Gemini AI integration
- **gTTS**: Text-to-speech conversion
- **textblob**: Natural language processing
- **nltk**: Text analysis toolkit

## Future Enhancements 🚀

- [ ] Support for multiple languages
- [ ] User account system with progress tracking
- [ ] Batch processing for multiple sentences
- [ ] Export results as PDF
- [ ] Integration with LLaMA local models
- [ ] Mobile app version
- [ ] Vocabulary learning games
- [ ] Reading comprehension tests

## Educational Use 🎓

This system can be used for:
- **Reading assistance** for dyslexic students
- **Language learning** for ESL students
- **Writing improvement** by understanding readability
- **Accessibility tools** in educational platforms

## Contributing 🤝

Feel free to fork this project and submit pull requests for improvements!

## License 📄

This project is designed for educational and assistive purposes. Feel free to use and modify as needed.

## Support 💬

For issues or questions, please refer to the documentation or create an issue in the project repository.

## Acknowledgments 🙏

- Google Gemini AI for powerful text analysis
- OpenDyslexic font for improved readability
- Flask community for excellent documentation
- gTTS for text-to-speech capabilities

---

**Made with ❤️ to improve reading accessibility for everyone** 
