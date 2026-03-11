# Quick Start Guide

## First Time Setup

1. Double-click `setup.bat` or run in terminal:
   ```
   setup.bat
   ```

2. Edit `.env` file and add your Gemini API key:
   - Get key from: https://makersuite.google.com/app/apikey
   - Open `.env` in notepad
   - Replace `your_gemini_api_key_here` with your actual key
   - Save and close

## Starting the Application

Option 1: Double-click `start_app.bat`

Option 2: Run in terminal:
```
start_app.bat
```

Option 3: Use Python directly:
```
python start_app.py
```

## Accessing the Application

Open your browser and go to:
- http://localhost:5000
- http://127.0.0.1:5000

## Stopping the Application

Press `Ctrl + C` in the terminal window

## Troubleshooting

### Python not found
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Virtual environment issues
- Delete the `venv` folder
- Run `setup.bat` again

### API key errors
- Make sure `.env` file exists
- Check that your API key is valid
- Ensure there are no extra spaces in the API key

### Port already in use
- Edit `start_app.py` and change port number from 5000 to another port (e.g., 5001)

## Manual Virtual Environment Commands

Activate virtual environment:
```
venv\Scripts\activate
```

Deactivate virtual environment:
```
deactivate
```

Install new dependency:
```
pip install package-name
pip freeze > requirements.txt
```
