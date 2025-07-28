

def get_best_alchs(prices, mapping):
    results = []
    NR_ID = "561"  # Nature rune ID
    nature_rune = prices.get(NR_ID, {"low": 0, "high": 0})
    for item in mapping:
        item_id = str(item["id"])
        if item_id not in prices.keys():
            continue
        item_name = item["name"]
        lp = prices[item_id]["low"]
        hp = prices[item_id]["high"]
        if "highalch" not in item:
            continue
        if item["highalch"] < lp + nature_rune["low"]:
            continue
        results.append({
            "Item": item_name,
            "High Alch": item["highalch"],
            "Low Price": lp,
            "High Price": hp,
            "Margin": item["highalch"] - (lp + nature_rune["low"]),
        })

    return nature_rune, results