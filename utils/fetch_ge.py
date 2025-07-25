import requests
import pandas as pd
from datetime import datetime

def fetch_item_data(item_id):
    base_url = "https://secure.runescape.com/m=itemdb_oldschool/api"
    
    detail_url = f"{base_url}/catalogue/detail.json?item={item_id}"
    graph_url = f"{base_url}/graph/{item_id}.json"
    
    detail = requests.get(detail_url).json()['item']
    graph = requests.get(graph_url).json()['daily']

    df = pd.DataFrame(list(graph.items()), columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    return detail, df[['date', 'price']]
