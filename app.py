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

REFRESH_SECONDS = 60

# Configure page for auto-refresh
st.set_page_config(page_title="Gielinor Points Accumulator", layout="wide")

# Initialize session state
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True  # Default to auto-refresh enabled
if 'prices' not in st.session_state:
    st.session_state.prices = None
if 'all_mapping' not in st.session_state:
    st.session_state.all_mapping = None

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
profile_name = st.selectbox("Select a profile", ["Potion Seller", "Barrows Repairer", "Costco (Bulk Items)"])

# Resolve profile module
profile = {
    "Potion Seller": potion_seller,
    "Barrows Repairer": barrows_repairer,
    "Costco (Bulk Items)": costco
}[profile_name]

# Create columns for refresh controls
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    # Manual refresh button
    if st.button("🔄 Refresh Data", help="Click to manually refresh the data"):
        st.session_state.prices, st.session_state.all_mapping = fetch_data(profile)
        st.session_state.last_refresh = time.time()
        st.rerun()

with col2:
    # Auto-refresh toggle
    auto_toggle = st.checkbox(f"Auto-refresh ({REFRESH_SECONDS}s)", value=st.session_state.auto_refresh, 
                              help=f"Automatically refresh data every {REFRESH_SECONDS} seconds")
    st.session_state.auto_refresh = auto_toggle  # Update session state for auto-refresh toggle. This still feels circular to me i have read too many docs on this and still ????

with col3:
    # Display last refresh time and countdown
    last_refreshed = st.session_state.get("last_refreshed", time.time())
    local_time_str = datetime.fromtimestamp(last_refreshed).strftime("%H:%M:%S")
    st.write(f"Last updated: {local_time_str}")

# Auto-refresh logic
time_since_refresh = int(time.time() - last_refreshed)
if st.session_state.auto_refresh and time_since_refresh >= REFRESH_SECONDS:
    st.session_state.last_refreshed = time.time()

# Use cached data or fetch if not available
if st.session_state.prices is None:
    st.session_state.prices, st.session_state.all_mapping = fetch_data(profile)
    st.session_state.last_refresh = time.time()

prices = st.session_state.prices
all_mapping = st.session_state.all_mapping

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
