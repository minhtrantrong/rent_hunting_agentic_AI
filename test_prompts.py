#!/usr/bin/env python3
"""
Automated testing script for app.py with prompts ranging from specific to vague
"""
import subprocess
import time
import sys
from typing import List, Dict

class AppTester:
    def __init__(self):
        self.results = []

    def test_prompts(self):
        """Test the app with various prompts from specific to vague"""

        # Hyper-specific prompts
        specific_prompts = [
            "Show me 2-bedroom apartments in Capitol Hill, Seattle under $2500/month with parking",
            "Find studio apartments in Fremont, Seattle between $1800-$2200 with laundry in unit",
            "Search for 1-bedroom apartments in Ballard, Seattle under $2000 with pet-friendly policies"
        ]

        # Moderately specific prompts
        moderate_prompts = [
            "I need an apartment in Seattle for around $2000 per month",
            "Find me a good rental in downtown Seattle with amenities",
            "Looking for a place in Seattle with good transit access under $2500"
        ]

        # Vague prompts
        vague_prompts = [
            "Help me find an apartment",
            "I need a place to live in Seattle",
            "What's available for rent?",
            "Find me something good"
        ]

        all_tests = [
            ("Hyper-Specific", specific_prompts),
            ("Moderately Specific", moderate_prompts),
            ("Vague", vague_prompts)
        ]

        for category, prompts in all_tests:
            print(f"\n{'='*60}")
            print(f"TESTING {category.upper()} PROMPTS")
            print(f"{'='*60}")

            for i, prompt in enumerate(prompts, 1):
                print(f"\n[{category} Test {i}] Testing prompt: '{prompt}'")
                result = self.run_single_test(prompt)
                self.results.append({
                    'category': category,
                    'prompt': prompt,
                    'success': result['success'],
                    'output': result['output'],
                    'error': result.get('error', ''),
                    'response_time': result.get('response_time', 0)
                })

                # Brief pause between tests
                time.sleep(2)

        self.analyze_results()

    def run_single_test(self, prompt: str) -> Dict:
        """Run a single test with the given prompt"""
        start_time = time.time()

        try:
            # Create input for the app
            input_text = f"{prompt}\nexit\n"

            # Run the app with the prompt
            process = subprocess.Popen(
                ['python', 'app.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(input=input_text, timeout=60)
            end_time = time.time()

            # Check if the process completed successfully
            if process.returncode == 0:
                print(f"✅ SUCCESS - Response in {end_time - start_time:.1f}s")
                print(f"📝 Output preview: {stdout[:200]}...")
                return {
                    'success': True,
                    'output': stdout,
                    'response_time': end_time - start_time
                }
            else:
                print(f"❌ FAILED - Exit code: {process.returncode}")
                print(f"🚨 Error: {stderr[:200]}...")
                return {
                    'success': False,
                    'output': stdout,
                    'error': stderr,
                    'response_time': end_time - start_time
                }

        except subprocess.TimeoutExpired:
            print("⏰ TIMEOUT - Test took longer than 60 seconds")
            process.kill()
            return {
                'success': False,
                'output': '',
                'error': 'Timeout after 60 seconds',
                'response_time': 60
            }
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'response_time': 0
            }

    def analyze_results(self):
        """Analyze and summarize the test results"""
        print(f"\n{'='*60}")
        print("ANALYSIS SUMMARY")
        print(f"{'='*60}")

        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'avg_time': 0}

            categories[cat]['total'] += 1
            if result['success']:
                categories[cat]['success'] += 1
            categories[cat]['avg_time'] += result['response_time']

        # Calculate averages and success rates
        for cat in categories:
            total = categories[cat]['total']
            categories[cat]['success_rate'] = (categories[cat]['success'] / total) * 100
            categories[cat]['avg_time'] = categories[cat]['avg_time'] / total

        # Print summary
        for cat, stats in categories.items():
            print(f"\n{cat}:")
            print(f"  Success Rate: {stats['success_rate']:.1f}% ({stats['success']}/{stats['total']})")
            print(f"  Avg Response Time: {stats['avg_time']:.1f}s")

        # Print detailed failures
        failures = [r for r in self.results if not r['success']]
        if failures:
            print(f"\n🚨 DETAILED FAILURE ANALYSIS:")
            for failure in failures:
                print(f"\nCategory: {failure['category']}")
                print(f"Prompt: '{failure['prompt']}'")
                print(f"Error: {failure['error'][:300]}...")

        # Save detailed results to file
        self.save_results_to_file()

    def save_results_to_file(self):
        """Save detailed results to a file"""
        with open('test_results.txt', 'w') as f:
            f.write("RENT HUNTING AI - TEST RESULTS\n")
            f.write("="*50 + "\n\n")

            for result in self.results:
                f.write(f"Category: {result['category']}\n")
                f.write(f"Prompt: {result['prompt']}\n")
                f.write(f"Success: {result['success']}\n")
                f.write(f"Response Time: {result['response_time']:.1f}s\n")
                f.write(f"Output: {result['output'][:500]}...\n")
                if result.get('error'):
                    f.write(f"Error: {result['error']}\n")
                f.write("-" * 30 + "\n\n")

        print(f"\n📄 Detailed results saved to 'test_results.txt'")

if __name__ == "__main__":
    print("🤖 Starting Rent Hunting AI Test Suite")
    print("This will test the app with prompts ranging from specific to vague")

    tester = AppTester()
    tester.test_prompts()

    print("\n✅ Testing complete!")