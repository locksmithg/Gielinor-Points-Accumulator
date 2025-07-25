import streamlit as st
from utils.fetch_ge import fetch_item_data
import matplotlib.pyplot as plt

st.title("🪙 Gielinor Points Accumulator")

item_id = st.number_input("Enter Item ID (e.g. Abyssal Whip = 4151)", value=4151)
if st.button("Fetch Item Data"):
    try:
        detail, df = fetch_item_data(item_id)
        st.subheader(detail['name'])
        st.write(f"Current Price: {detail['current']['price']} gp")

        # Plot
        fig, ax = plt.subplots()
        ax.plot(df['date'], df['price'], label=detail['name'])
        ax.set_ylabel("Price (gp)")
        ax.set_title("Price History")
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
