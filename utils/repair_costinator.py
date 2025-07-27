MOONS_BASE = 1500000
HEAD_BASE = 60000
BODY_BASE = 90000
LEGS_BASE = 80000
WEAPON_BASE = 100000

def get_repair_costs(prices: list[dict], smithing_level: int) -> list[dict]:
    results = {}
    # Create a dictionary to hold the item prices for paired broken and fixed items
    for item in prices:
        name = item["Item"]
        low = item["Low Price"]
        high = item["High Price"]
        item_name = ''
        if is_moon(name):
            item_name = name.split("(")[0].strip()
        else:
            item_name = name.split("0")[0].strip()
        if item_name not in results:
            results[item_name] = {
                "Item": item_name,
                "Broken Low": 0,
                "Fixed High": 0,
                "Repair Cost": 0,
                "Margin": 0,
                "ROI %": 0
            }
        if 'broken' in name or '0' in name:
            results[item_name]["Broken Low"] = low
        else:
            results[item_name]["Fixed High"] = high
    
    # Post-process: calculate Repair Cost, Margin, and ROI
    for entry in results.values():
        broken_low = entry["Broken Low"]
        fixed_high = entry["Fixed High"]
        if broken_low and fixed_high:
            repair_cost = get_base_cost(entry["Item"])
            if repair_cost == 0:
                print(f"Unknown base cost for {entry['Item']}, skipping.")
                continue
            repair_cost = int(repair_cost * (1 - (smithing_level / 200.0)))
            entry["Repair Cost"] = repair_cost
            entry["Margin"] = int(fixed_high - broken_low - repair_cost)
            entry["ROI %"] = round((entry["Margin"] / (broken_low + repair_cost)) * 100, 2) if repair_cost else 0
    
    return list(results.values())

def get_base_cost(item_name: str) -> int:
    item_name = item_name.lower()
    if is_helm(item_name):
        return HEAD_BASE
    elif is_body(item_name):
        return BODY_BASE
    elif is_legs(item_name):
        return LEGS_BASE
    elif is_moon(item_name):
        return MOONS_BASE
    else:
        return WEAPON_BASE

def is_helm(item_name: str) -> bool:
    item_name = item_name.lower()
    return ("helm" in item_name or "coif" in item_name or "hood" in item_name) and not is_moon(item_name)

def is_body(item_name: str) -> bool:
    item_name = item_name.lower()
    return "body" in item_name or "top" in item_name

def is_legs(item_name: str) -> bool:
    item_name = item_name.lower()
    return "legs" in item_name or "skirt" in item_name

def is_moon(item_name: str) -> bool:
    item_name = item_name.lower()
    return "moon" in item_name