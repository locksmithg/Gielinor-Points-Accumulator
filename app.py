import streamlit as st
import pandas as pd
from utils.scanner import get_item_prices

# Import profiles
import profiles.potion_seller as potion_seller
import profiles.barrows_repairer as barrows_repairer
import profiles.costco as costco
from utils.potion_comparator import compare_potion_doses

# Profile selection
profile_name = st.selectbox("Select a profile", ["potion_seller", "barrows_repairer", "costco"])

# Resolve profile module
profile = {
    "potion_seller": potion_seller,
    "barrows_repairer": barrows_repairer,
    "costco": costco
}[profile_name]

# Fetch prices
with st.spinner("Fetching Grand Exchange data..."):
    prices = get_item_prices(profile.ITEM_WHITELIST)

# Handle potion_seller special tabs
if profile_name == "potion_seller":
    tab1, tab2 = st.tabs(["Scanner", "Potion Dose Comparator"])

    with tab1:
        df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
        df.drop(columns=["Item ID"], inplace=True, errors='ignore')
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        potions_compared = compare_potion_doses(prices)
        df = pd.DataFrame(potions_compared).sort_values(by="Margin", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
    df.drop(columns=["Item ID"], inplace=True, errors='ignore')
    st.dataframe(df, use_container_width=True, hide_index=True)
