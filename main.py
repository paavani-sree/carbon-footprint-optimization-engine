import json
from agents.supervisor import run_cfoe

with open("data/suppliers.json") as f:
    suppliers = json.load(f)

supplier = suppliers[0]  # choose supplier
distance_km = 600

result = run_cfoe(supplier, distance_km)

print("\n🌱 Carbon Footprint Optimization Engine Result\n")
for key, value in result.items():
    print(f"{key}: {value}")
