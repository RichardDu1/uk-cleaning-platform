import urllib.request
import json
import time

test_leads = [
    {
        "name": "Sarah Jenkins",
        "phone": "07891 234567",
        "postcode": "RG1 2AB",
        "service": "Full Bathroom Renovation",
        "notes": "Need old tiles stripped off and full waterproofing tanking for new subway tiles. Bathroom is approx 12 sqm."
    },
    {
        "name": "Michael Roberts",
        "phone": "07700 900123",
        "postcode": "OX1 3PE",
        "service": "Kitchen Splashback",
        "notes": "Herringbone pattern behind gas cooker and along 4 metres of quartz worktop."
    }
]

print("=== STARTING AI LEAD DISPATCH SIMULATION ===")
for lead in test_leads:
    print(f"\nSimulating customer enquiry from {lead['name']} ({lead['postcode']})...")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/lead",
        data=json.dumps(lead).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print("Response:", resp.read().decode('utf-8'))
    except Exception as e:
        print("Error submitting to server:", e)
    time.sleep(1)
