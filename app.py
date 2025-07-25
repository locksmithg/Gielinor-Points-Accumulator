import streamlit as st
import importlib
from utils.scanner import scan_items

st.set_page_config(page_title="Gielinor Points Accumulator", layout="wide")

st.title("📈 Gielinor Points Accumulator")
st.write("Select a profile to scan and detect profitable OSRS items to flip or hold.")

# Map of user-friendly names to module paths
PROFILES = {
    "Potion Seller": "profiles.potion_seller",
    "Barrows Repairer": "profiles.barrows_repairer",
    "Costco": "profiles.costco"
}

profile_name = st.selectbox("Choose a Profile", list(PROFILES.keys()))
if st.button("Run Scan"):
    with st.spinner("Scanning items..."):
        profile_module = importlib.import_module(PROFILES[profile_name])
        whitelist = profile_module.ITEM_WHITELIST

        df = scan_items(whitelist)
        df.drop(columns=["Item ID"], inplace=True, errors='ignore')
        st.success("Scan complete!")
        with st.expander("📊 View Scan Results (Scroll to see all items)", expanded=True):
            st.dataframe(df, use_container_width=True, height=500)
        st.download_button(
            label="Download Results as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"{profile_name.replace(' ', '_').lower()}_scan_results.csv",
            mime='text/csv'
        )