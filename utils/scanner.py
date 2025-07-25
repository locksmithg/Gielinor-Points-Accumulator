# scanner.py
import requests
import pandas as pd
import time
from datetime import datetime

from profiles.barrows_repairer import ITEM_WHITELIST as BARROWS_WL
from profiles.costco import ITEM_WHITELIST as COSTCO_WL
from profiles.potion_seller import ITEM_WHITELIST as POTION_WL

def fetch_all_latest_prices():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", {})
    else:
        print(f"[Error] Failed to fetch prices: {response.status_code}")
        return {}

# def fetch_graph_meta(item_id):
#     url = f"https://prices.runescape.wiki/api/v1/osrs/graphs?id={item_id}"
#     resp = requests.get(url)
#     if resp.status_code == 200:
#         return resp.json().get("data", {}).get(str(item_id), {})
#     return {}

# def fetch_item_detail(item_id):
#     url = f"https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={item_id}"
#     return requests.get(url).json()["item"]

# def fetch_price_graph(item_id):
#     url = f"https://secure.runescape.com/m=itemdb_oldschool/api/graph/{item_id}.json"
#     data = requests.get(url).json()["daily"]
#     df = pd.DataFrame(list(data.items()), columns=["timestamp", "price"])
#     df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
#     return df[["date", "price"]]

def fetch_item_data(item_id, retries=3, delay=0.5):
    url = f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json().get("data", {}).get(str(item_id), {})

            elif response.status_code == 429:
                print(f"[Throttle] 429 received for item {item_id}, retrying after delay...")
                time.sleep(delay * (attempt + 1))  # exponential backoff

            else:
                print(f"[Error] {response.status_code} for item {item_id}")
                break

        except requests.RequestException as e:
            print(f"[Exception] {e} for item {item_id}")
            time.sleep(delay)

    return {}  # Return empty if all retries failed

def scan_items(item_whitelist):
    all_data = fetch_all_latest_prices()
    results = []

    for item_id, item_name in item_whitelist.items():
        item_data = all_data.get(str(item_id))

        if item_data:
            high = item_data.get("high", 0)
            low = item_data.get("low", 0)
            high_time = format_timestamp(item_data.get("highTime"))
            low_time = format_timestamp(item_data.get("lowTime"))
            margin = high - low
            roi = round((margin / low) * 100, 2) if low else 0

            results.append({
                "Item": item_name,
                "Item ID": item_id,
                "Low Price": low,
                "Low Time": low_time,
                "High Price": high,
                "High Time": high_time,
                "Margin": margin,
                "ROI %": roi
            })
        else:
            results.append({
                "Item": item_name,
                "Item ID": item_id,
                "Low Price": None,
                "Low Time": None,
                "High Price": None,
                "High Time": None,
                "Margin": None,
                "ROI %": None
            })

    return pd.DataFrame(results).sort_values(by="ROI %", ascending=False)

def format_timestamp(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Unknown"