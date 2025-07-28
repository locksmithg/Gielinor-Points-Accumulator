def compare_potion_doses(prices: list[dict]) -> list[dict]:
    results = {}

    for potion in prices:
        name = potion["Item"]
        low = potion["Low Price"]
        high = potion["High Price"]
        potion_name = name.split("(")[0].strip()
        if potion_name not in results:
            results[potion_name] = {
                "Potion": potion_name,
                "1-dose PPD": 0,
                "2-dose PPD": 0,
                "3-dose PPD": 0,
                "4-dose PPD high": 0,
                "Sell Price": 0,
                "Lowest PPD": 0,
                "Margin": 0
            }
        if '(1)' in name:
            results[potion_name]["1-dose PPD"] = low
        elif '(2)' in name:
            results[potion_name]["2-dose PPD"] = round(low / 2, 2)
        elif '(3)' in name:
            results[potion_name]["3-dose PPD"] = round(low / 3, 2)
        elif '(4)' in name:
            results[potion_name]["4-dose PPD high"] = round(high / 4, 2) if high else None
            results[potion_name]["Sell Price"] = high

    # Post-process: compute Lowest PPD and Margin
    for entry in results.values():
        ppds = {d: entry[f"{d}-dose PPD"] for d in [1, 2, 3] if entry[f"{d}-dose PPD"] is not None}
        if ppds:
            lowest_dose = min(ppds, key=lambda k: ppds[k])
            entry["Lowest PPD"] = lowest_dose
            lowest_ppd_value = ppds[lowest_dose]
            sell_ppd = entry["4-dose PPD high"]
            if sell_ppd is not None:
                entry["Margin"] = round(sell_ppd - lowest_ppd_value, 2)
   

    return list(results.values())