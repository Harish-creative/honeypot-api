import requests
from colorama import Fore, Style, init
from tabulate import tabulate
import json
from datetime import datetime

init(autoreset=True)

API_URL = "http://127.0.0.1:8000/honeypot"
API_KEY = "test_api_key"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

print(Fore.CYAN + "=" * 60)
print(Fore.YELLOW + "🐝  AGENTIC HONEYPOT API TESTER")
print(Fore.CYAN + "=" * 60)

results = []

with open("messages.txt") as f:
    messages = f.read().splitlines()

for i, msg in enumerate(messages, start=1):
    print(Fore.BLUE + f"\n🔍 Test Case {i}")
    print(Fore.WHITE + f"Message: {msg}")

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"message": msg},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            print(Fore.GREEN + "✅ Response OK")
            print(Fore.YELLOW + json.dumps(data, indent=4))

            results.append([
                i,
                data["scam_type"],
                data["risk_score"],
                data["honeypot_reply"]
            ])

        else:
            print(Fore.RED + f"❌ HTTP Error {response.status_code}")
            results.append([i, "ERROR", "-", "-"])

    except Exception as e:
        print(Fore.RED + f"❌ Request Failed: {e}")
        results.append([i, "FAILED", "-", "-"])

# 📊 SUMMARY
print(Fore.CYAN + "\n" + "=" * 60)
print(Fore.YELLOW + "📊 TEST SUMMARY")
print(Fore.CYAN + "=" * 60)

print(tabulate(
    results,
    headers=["#", "Scam Type", "Risk Score", "Honeypot Reply"],
    tablefmt="fancy_grid"
))

# 📝 Save log
with open("tester_log.txt", "a") as log:
    log.write(f"\n--- Test Run {datetime.now()} ---\n")
    for r in results:
        log.write(str(r) + "\n")

print(Fore.GREEN + "\n📁 Results saved to tester_log.txt")
