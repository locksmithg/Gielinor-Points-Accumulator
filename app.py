import streamlit as st
import pandas as pd
from utils.scanner import get_item_prices, get_all_mapping

# Import profiles
import profiles.potion_seller as potion_seller
import profiles.barrows_repairer as barrows_repairer
import profiles.costco as costco
from utils.potion_comparator import compare_potion_doses
from utils.repair_costinator import get_repair_costs

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
    all_mapping = get_all_mapping()


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
elif profile_name == "barrows_repairer":
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
else:
    df = pd.DataFrame(prices).sort_values(by="ROI %", ascending=False)
    df.drop(columns=["Item ID"], inplace=True, errors='ignore')
    st.dataframe(df, use_container_width=True, hide_index=True)
