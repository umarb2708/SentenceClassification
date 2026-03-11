#!/usr/bin/env python
"""
Test Gemini API Connection
This script tests your Gemini API key and lists available models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("  Gemini API Connection Test")
print("=" * 60)
print()

# Check API key
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")
print()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured successfully")
    print()
except Exception as e:
    print(f"❌ ERROR configuring Gemini: {e}")
    exit(1)

# List available models
print("📋 Available Models:")
print("-" * 60)
try:
    models = genai.list_models()
    generative_models = []
    
    for model in models:
        # Check if model supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            generative_models.append(model.name)
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description[:80]}...")
            print()
    
    if not generative_models:
        print("⚠️  No models found that support generateContent")
    
except Exception as e:
    print(f"❌ ERROR listing models: {e}")
    exit(1)

# Test with the first available model
if generative_models:
    print("=" * 60)
    print("  Testing Text Generation")
    print("=" * 60)
    print()
    
    test_model_name = generative_models[0]
    print(f"Using model: {test_model_name}")
    print()
    
    try:
        model = genai.GenerativeModel(test_model_name)
        
        test_prompt = "Say 'Hello, the API is working!' in a simple sentence."
        print(f"Test prompt: {test_prompt}")
        print()
        
        response = model.generate_content(test_prompt)
        print("✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        print()
        
        print("🎉 SUCCESS! Your Gemini API is working correctly!")
        print()
        print(f"Recommended model for your .env file:")
        print(f"GEMINI_MODEL={test_model_name}")
        
    except Exception as e:
        print(f"❌ ERROR generating content: {e}")
        print()
        print("Try using a different model from the list above")

print()
print("=" * 60)
