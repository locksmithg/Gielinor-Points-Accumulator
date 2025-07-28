import streamlit as st
import pandas as pd
import time
from datetime import datetime
from utils.scanner import get_item_prices, get_all_mapping, fetch_all_latest_prices

# Import profiles
import profiles.potion_seller as potion_seller
import profiles.barrows_repairer as barrows_repairer
import profiles.costco as costco
from utils.potion_comparator import compare_potion_doses
from utils.repair_costinator import get_repair_costs
from utils.full_metal_alchemist import get_best_alchs

REFRESH_SECONDS = 60

# Configure page for auto-refresh
st.set_page_config(page_title="Gielinor Points Accumulator", layout="wide")

# Initialize session state
if "custom_profile" not in st.session_state:
    st.session_state.custom_profile = None


def fetch_data(profile):
    """Fetch prices and mapping data"""
    with st.spinner("Fetching Grand Exchange data..."):
        if profile:
            prices = get_item_prices(profile.ITEM_WHITELIST)
        else:
            prices = fetch_all_latest_prices()
        all_mapping = get_all_mapping()
        return prices, all_mapping

# Profile selection
profile_name = st.selectbox("Select a profile", ["Potion Seller", "Barrows Repairer", "Costco (Bulk Items)", "Full Metal Alchemist"], index=0)

# Resolve profile module
profile = {
    "Potion Seller": potion_seller,
    "Barrows Repairer": barrows_repairer,
    "Costco (Bulk Items)": costco,
    "Full Metal Alchemist": None
}[profile_name]

prices, all_mapping = fetch_data(profile)

# Create columns for refresh controls
col1, col2 = st.columns([1, 1])
with col1:
    # Manual refresh button
    if st.button("🔄 Refresh Data", help="Click to manually refresh the data"):
        prices, all_mapping = fetch_data(profile)
        st.session_state.last_refresh = time.time()
        st.rerun()

with col2:
    # Display last refresh time
    last_refreshed = st.session_state.get("last_refreshed", time.time())
    local_time_str = datetime.fromtimestamp(last_refreshed).strftime("%H:%M:%S")
    st.write(f"Last updated: {local_time_str}")

# Add a separator
st.divider()


############### Potion Seller Tabs ###############
if profile_name == "Potion Seller":
    tab1, tab2 = st.tabs(["Scanner", "Potion Dose Comparator"])

    with tab1:
        df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
        df.drop(columns=["Item ID"], inplace=True, errors='ignore')
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        potions_compared = compare_potion_doses(prices)
        df = pd.DataFrame(potions_compared).sort_values(by="Margin", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
############### Barrows Repairer Tabs ###############
elif profile_name == "Barrows Repairer":
    tab1, tab2 = st.tabs(["Scanner", "Repair Costinator"])
    with tab1:
        df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
        df.drop(columns=["Item ID"], inplace=True, errors='ignore')
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tab2:
        # input field for smithing level
        smithing_level = st.number_input("Enter your Smithing level (1 - 104 if you're boosting)", min_value=1, max_value=104, value=99)
        repairinator = get_repair_costs(prices, smithing_level)
        df = pd.DataFrame(repairinator).sort_values(by="ROI %", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
############### Costco (Bulk Items) Tab ###############
elif profile_name == "Costco (Bulk Items)":
    df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
    df.drop(columns=["Item ID"], inplace=True, errors='ignore')
    st.dataframe(df, use_container_width=True, hide_index=True)
############### Costco (Bulk Items) Tab ###############
elif profile_name == "Full Metal Alchemist":
    nature_rune, best_alchs = get_best_alchs(prices, all_mapping)
    st.write(f"Nature Rune Price Low: {nature_rune['low']} | High: {nature_rune['high']}")
    df = pd.DataFrame(best_alchs).sort_values(by="Margin", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)