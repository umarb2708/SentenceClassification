#!/usr/bin/env python
"""
Sentence Classification System - Application Starter
This script starts the Flask application with proper configuration.
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files and configurations are present."""
    errors = []
    warnings = []
    
    # Check if app.py exists
    if not Path('app.py').exists():
        errors.append("app.py not found!")
    
    # Check if .env file exists
    if not Path('.env').exists():
        warnings.append(".env file not found. Please configure your API keys.")
    
    # Check if templates directory exists
    if not Path('templates').exists():
        errors.append("templates/ directory not found!")
    
    # Check if static directory exists
    if not Path('static').exists():
        errors.append("static/ directory not found!")
    
    return errors, warnings

def check_environment():
    """Check if required environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("\n⚠️  WARNING: GEMINI_API_KEY not configured in .env file")
        print("   The application will not work without a valid API key.")
        print("   Get your free API key from: https://makersuite.google.com/app/apikey")
        print()
        
        response = input("Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("\nPlease configure your API key in .env file and try again.")
            sys.exit(1)

def main():
    """Main function to start the Flask application."""
    print("=" * 50)
    print("  Sentence Classification System")
    print("  Starting Application...")
    print("=" * 50)
    print()
    
    # Check requirements
    errors, warnings = check_requirements()
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease fix these errors and try again.")
        sys.exit(1)
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    # Check environment variables
    try:
        check_environment()
    except ImportError:
        print("❌ ERROR: Required packages not installed!")
        print("   Please run setup.bat first to install dependencies.")
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        print("✅ All checks passed!")
        print()
        print("Starting Flask server...")
        print("-" * 50)
        print()
        print("🌐 Application will be available at:")
        print("   http://localhost:5000")
        print("   http://127.0.0.1:5000")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        print()
        
        # Import and run the app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"\n❌ ERROR: Failed to import application: {e}")
        print("   Please make sure all dependencies are installed.")
        print("   Run setup.bat to install dependencies.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thank you for using Sentence Classification System!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
