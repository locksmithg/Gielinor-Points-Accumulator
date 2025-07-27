MOONS_BASE = 1500000
HEAD_BASE = 60000
BODY_BASE = 90000
LEGS_BASE = 80000
WEAPON_BASE = 100000

def get_repair_cost(prices: list[dict], smithing_level: int) -> list[dict]:
    results = {}
    for item in prices:
        name = item["Item"]
        low = item["Low Price"]
        high = item["High Price"]

        item_name = name.split("(")[0].strip()
        if item_name not in results:
            results[item_name] = {
                "Item": item_name,
                "Broken Low": 0,
                "Fixed High": 0,
                "Repair Cost": 0,
                "Margin": 0,
                "ROI %": 0
            }
        if 'broken' in name.lower():
            results[item_name]["Broken Low"] = low
        else:
            results[item_name]["Fixed High"] = high
        
