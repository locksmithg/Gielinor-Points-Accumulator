

def get_best_alchs(prices, mapping):
    results = {}

    for item in prices:
        name = item["Item"]
        low = item["Low Price"]
        high = item["High Price"]
        item_name = mapping.get(name, name).split("(")[0].strip()
        
        if item_name not in results:
            results[item_name] = {
                "Item": item_name,
                "Low Alch": 0,
                "High Alch": 0,
                "Margin": 0
            }
        
        if 'low alch' in name.lower():
            results[item_name]["Low Alch"] = low
        elif 'high alch' in name.lower():
            results[item_name]["High Alch"] = high
    
    # Post-process: calculate Margin
    for entry in results.values():
        low_alch = entry["Low Alch"]
        high_alch = entry["High Alch"]
        if low_alch and high_alch:
            entry["Margin"] = high_alch - low_alch
    
    return list(results.values())