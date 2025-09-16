#!/usr/bin/env python3
"""
Simple test to check individual prompts manually
"""
import sys
import os

# Add the current directory to path to import modules
sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')

def test_individual_prompts():
    """Test specific prompts one by one"""

    # Test prompts from specific to vague
    test_prompts = [
        # Hyper-specific
        {
            "category": "Hyper-Specific",
            "prompt": "Show me 2-bedroom apartments in Capitol Hill, Seattle under $2500/month with parking",
            "expected": "Should return specific apartment listings with detailed criteria"
        },
        {
            "category": "Hyper-Specific",
            "prompt": "Find studio apartments in Fremont, Seattle between $1800-$2200 with laundry in unit",
            "expected": "Should filter by location, price range, and amenities"
        },

        # Moderately specific
        {
            "category": "Moderate",
            "prompt": "I need an apartment in Seattle for around $2000 per month",
            "expected": "Should understand general price range and location"
        },
        {
            "category": "Moderate",
            "prompt": "Find me a good rental in downtown Seattle with amenities",
            "expected": "Should interpret 'downtown' and 'amenities' broadly"
        },

        # Vague
        {
            "category": "Vague",
            "prompt": "Help me find an apartment",
            "expected": "Should ask clarifying questions"
        },
        {
            "category": "Vague",
            "prompt": "I need a place to live in Seattle",
            "expected": "Should ask for budget, size, preferences"
        }
    ]

    print("📋 MANUAL TESTING GUIDE")
    print("="*50)
    print("Copy and paste these prompts into the app.py when it runs:")
    print()

    for i, test in enumerate(test_prompts, 1):
        print(f"{i}. [{test['category']}]")
        print(f"   Prompt: {test['prompt']}")
        print(f"   Expected: {test['expected']}")
        print()

    print("After testing each prompt, note:")
    print("- Does it understand the request?")
    print("- Does it ask relevant follow-up questions?")
    print("- Does it provide relevant results?")
    print("- Does response quality degrade with vagueness?")

if __name__ == "__main__":
    test_individual_prompts()