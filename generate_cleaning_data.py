import json
import random

# 1. 第 1 维 (Service): 深挖细分服务 (End of Tenancy & Cleaning)
SERVICES = [
    {
        "id": "end-of-tenancy-cleaning",
        "name": "End of Tenancy Cleaning",
        "base_price": 150,
        "description": "Professional end of tenancy cleaning with a 100% deposit return guarantee."
    },
    {
        "id": "professional-carpet-cleaning",
        "name": "Professional Carpet Cleaning",
        "base_price": 50,
        "description": "Deep steam carpet cleaning to remove stubborn stains and allergens."
    },
    {
        "id": "rubbish-waste-clearance",
        "name": "Rubbish & Waste Clearance",
        "base_price": 80,
        "description": "Fast and eco-friendly waste removal and furniture disposal."
    },
    {
        "id": "deep-cleaning",
        "name": "Deep Cleaning Services",
        "base_price": 180,
        "description": "Thorough deep cleaning for your entire property, reaching every corner."
    },
    {
        "id": "move-in-cleaning",
        "name": "Move-In Cleaning",
        "base_price": 160,
        "description": "Fresh and sanitized home preparation before you move in."
    },
    {
        "id": "oven-cleaning",
        "name": "Professional Oven Cleaning",
        "base_price": 45,
        "description": "Specialist oven detailing to remove burnt-on grease and carbon."
    },
    {
        "id": "upholstery-cleaning",
        "name": "Upholstery Cleaning",
        "base_price": 60,
        "description": "Revive your sofas and armchairs with our deep upholstery wash."
    },
    {
        "id": "mattress-cleaning",
        "name": "Mattress Deep Cleaning",
        "base_price": 40,
        "description": "Eliminate dust mites and stains for a healthier sleep."
    },
    {
        "id": "builders-cleans",
        "name": "After Builders Cleaning",
        "base_price": 200,
        "description": "Intensive cleaning to remove post-construction dust and debris."
    },
    {
        "id": "student-accommodation-cleaning",
        "name": "Student Accommodation Cleaning",
        "base_price": 120,
        "description": "Affordable and fast cleaning tailored for university students."
    }
]

# 2. 第 2 维 (Location) - 选取主要城市 + 伦敦 32 区
CITIES = [
    {"name": "Birmingham", "region": "West Midlands", "postcode": "B1", "nearby": ["Solihull", "Wolverhampton", "Dudley"]},
    {"name": "Manchester", "region": "North West", "postcode": "M1", "nearby": ["Salford", "Stockport", "Bolton"]},
    {"name": "Glasgow", "region": "Scotland", "postcode": "G1", "nearby": ["Paisley", "East Kilbride", "Hamilton"]},
    {"name": "Leeds", "region": "Yorkshire", "postcode": "LS1", "nearby": ["Bradford", "Wakefield", "Halifax"]},
    {"name": "Liverpool", "region": "North West", "postcode": "L1", "nearby": ["Birkenhead", "Bootle", "St Helens"]},
    {"name": "Newcastle", "region": "North East", "postcode": "NE1", "nearby": ["Gateshead", "Sunderland", "South Shields"]},
    {"name": "Sheffield", "region": "Yorkshire", "postcode": "S1", "nearby": ["Rotherham", "Barnsley", "Chesterfield"]},
    {"name": "Bristol", "region": "South West", "postcode": "BS1", "nearby": ["Bath", "Weston-super-Mare", "Clevedon"]},
    {"name": "Nottingham", "region": "East Midlands", "postcode": "NG1", "nearby": ["Derby", "Mansfield", "Newark"]},
    {"name": "Leicester", "region": "East Midlands", "postcode": "LE1", "nearby": ["Loughborough", "Hinckley", "Melton Mowbray"]},
    {"name": "Edinburgh", "region": "Scotland", "postcode": "EH1", "nearby": ["Livingston", "Dunfermline", "Musselburgh"]},
    {"name": "Cardiff", "region": "Wales", "postcode": "CF10", "nearby": ["Newport", "Barry", "Caerphilly"]},
    {"name": "Coventry", "region": "West Midlands", "postcode": "CV1", "nearby": ["Nuneaton", "Rugby", "Leamington Spa"]},
    {"name": "Belfast", "region": "Northern Ireland", "postcode": "BT1", "nearby": ["Lisburn", "Bangor", "Newtownabbey"]},
    {"name": "Reading", "region": "South East", "postcode": "RG1", "nearby": ["Wokingham", "Bracknell", "Newbury"]},
    {"name": "Southampton", "region": "South East", "postcode": "SO14", "nearby": ["Portsmouth", "Winchester", "Eastleigh"]},
]

# 伦敦 32 行政区 (Boroughs)
LONDON_BOROUGHS = [
    "Camden", "Greenwich", "Hackney", "Hammersmith and Fulham", "Islington", "Royal Borough of Kensington and Chelsea", 
    "Lambeth", "Lewisham", "Southwark", "Tower Hamlets", "Wandsworth", "Westminster", "Barking and Dagenham", 
    "Barnet", "Bexley", "Brent", "Bromley", "Croydon", "Ealing", "Enfield", "Haringey", "Harrow", "Havering", 
    "Hillingdon", "Hounslow", "Kingston upon Thames", "Merton", "Newham", "Redbridge", "Richmond upon Thames", 
    "Sutton", "Waltham Forest"
]

for borough in LONDON_BOROUGHS:
    CITIES.append({
        "name": borough,
        "region": "London",
        "postcode": "London", # Simplified for generation
        "nearby": [random.choice(LONDON_BOROUGHS) for _ in range(3)]
    })


def get_pain_points(city_name, region):
    if region == "London":
        return f"In {city_name}, dealing with high-rise apartment logistics, strict landlord standards, and Victorian terraced house dust accumulation can make end of tenancy cleaning extremely stressful. We handle the parking permits, staircase access, and rigorous inventory checks."
    elif city_name == "Glasgow":
        return "Glasgow's traditional red sandstone tenements often suffer from high ceilings and stubborn window grime. We have the specialist equipment to tackle deep-seated dirt in older properties."
    elif city_name == "Birmingham":
        return "From modern city centre apartments in Birmingham to sprawling post-war housing, we know exactly what local letting agents look for during check-out inspections."
    elif city_name == "Edinburgh":
        return "Cleaning Edinburgh's historic New Town properties requires care. We tackle sash windows, ornate cornices, and tough limescale typical in the area."
    else:
        return f"Whether you are moving out of a student house or a family home in {city_name}, we know the exact standards local letting agents and landlords demand to return your deposit in full."

def generate_pricing(base_price, region):
    multiplier = 1.0
    if region == "London":
        multiplier = 1.3
    elif region in ["South East", "South West"]:
        multiplier = 1.15
        
    adjusted = base_price * multiplier
    
    return {
        "small": round(adjusted * 0.8 / 5) * 5,
        "medium": round(adjusted / 5) * 5,
        "large": round(adjusted * 1.5 / 5) * 5
    }

def generate_faqs(service_name, city_name, region):
    faqs = [
        {
            "question": f"Do you guarantee my deposit return for the cleaning in {city_name}?",
            "answer": "Yes, our end of tenancy cleaning comes with a 48-hour guarantee. If your landlord or inventory clerk is not happy with the cleaning, we will return and re-clean the problematic areas for free."
        },
        {
            "question": f"Do I need to provide cleaning supplies?",
            "answer": f"No, our professional {city_name} based teams bring all their own commercial-grade equipment and eco-friendly cleaning detergents."
        }
    ]
    
    if region == "London":
        faqs.append({
            "question": "How do you handle parking in London?",
            "answer": "We usually ask customers to arrange a parking permit. If parking is not available, any pay-and-display charges will be added to the final bill."
        })
        
    return faqs

output_data = []

# Generate cross product of Services x Cities
for service in SERVICES:
    for city in CITIES:
        # 3. 第 3 维 (Architecture Context)
        pain_points = get_pain_points(city["name"], city["region"])
        
        # 4. 第 4 维 (Economic Context)
        pricing = generate_pricing(service["base_price"], city["region"])
        faqs = generate_faqs(service["name"], city["name"], city["region"])
        
        # 5. 第 5 维 (Proximity Context)
        # city["nearby"]
        
        page_data = {
            "slug": f"{service['id']}/{city['name'].lower().replace(' ', '-')}",
            "service": service,
            "city": city,
            "content": {
                "h1": f"Expert {service['name']} in {city['name']} ({city['postcode']})",
                "pain_points": pain_points,
                "pricing": pricing,
                "faqs": faqs,
                "nearby_areas": city["nearby"]
            }
        }
        output_data.append(page_data)

with open('data/seo_pages.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(output_data)} page combinations in data/seo_pages.json")
