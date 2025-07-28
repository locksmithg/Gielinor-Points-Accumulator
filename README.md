# 💰 Gielinor Points Accumulator

👉 View the live app: https://gpaccumulator.streamlit.app/ 👈

Author: Gabriel Smith

**Gielinor Points Accumulator** is a Streamlit-based dashboard that tracks Old School RuneScape (OSRS) Grand Exchange data, surfaces flipping opportunities, potion pricing insights, Barrows gear margins, and identifies items that are profitable to high-alch — all in a fast, clean, and easy-to-use interface.

For those who have never played OSRS, the Grand Exchange is just the in-game auction house system that players are able to list items to buy and sell for specific GP prices, GP being the currency. 

If only looking at real world markets were so easy...

---

## 🚀 Features

### Core Functionality
- **Real-Time Data**: Fetches GE prices from the RuneLite-backed OSRS Wiki API.
- **Profile-Based Scanning**: Choose from pre‑defined profiles:
  - **Potion Seller** — price‑per‑dose comparisons across potion variants allowing you to quickly find profitable decanting opportunities (converting cheaper potions in doses of 1, 2, or 3 into the priceier 4 dose potion which is more widely used)
  - **Barrows Repairer** — compare margins between broken and fixed Barrows items and Perilous Moons items which automatically factors in the price of repairing the gear in your Player Owned House based on a provided smithing level.
  - **Costco** — high-volume items & bulk flipping opportunities
  - **Full Metal Alchemist** - Items that are profitable when you cast the *High Alchemy* spell on an item factoring in the cost of a nature rune which is required to cast the spell. High alchemy converts the item directly into GP according to a value hard set in game.

### Scanner Metrics
- Show item name, low/high prices, timestamps converted to **local time**, margin, and ROI %.
- Handles items that weren't traded recenetly, but does not store any of this data permanently, so I am not generating a price history to fall back on, though there are some metrics available from the wiki APIs.

### Nice-to-Have / UI Features
- Scrollable, sortable tables with a quick to use refresh button to make sure you have the latest data.
- Hide/show Item ID column.

---

## 🛠️ Local Installation & Usage

### Requirements
- Python 3.8+
- Packages listed in `requirements.txt`
- Internet access (for OSRS Wiki API)

### Clone & Install Dependencies
```bash
git clone https://github.com/locksmithg/Gielinor-Points-Accumulator.git
cd Gielinor-Points-Accumulator
pip install -r requirements.txt
streamlist run app.py
```

## 📈 Future Plans and Contribution

  Scope creep is something I've been very guilty of for short term projects like this. Here are some other features that I considered or might implement sometime:
- Create your own profiles and templates to contain whatever items you want and make it easy to manipulate the tables and data visualiztion in the UI or maybe a config file. I began work on this, but I simply did not have enough time in one weekend to do this too :(
- Scrape the OSRS News pages and posts for references to items and send a notification to the user that it could affect the price of mentioned items.
- Scrape r/GrandExchangeBets for general sentiment around items or potential hyped items that could see movement. This would be an awesome candidate for some AI integration to interpret what is "positive" or "negative" sentiment towards items.
- Start building predictive models around price movement for items. While certainly impossible in the real world, I suspect it is entirely possible to create a reasonably accurate predictive model for this in-game economy. The big things are that I have access to so, so much more data than is available in the real world. Individual items are not managed by individually run chaotic businesses, just Jagex. That means that it removes an incredible amount of complexity and chaos from the equation.
- A direct in game plugin that could report your actual trades in the game to this external tool and supply metrics on your successes and failures.
- Plenty more! I would love to hear feedback on the idea and other future potential updates!

## 🤓 The cool stuff I learned and implemented

    The main goal with this was to practice data organization stuff that I learned back in college for my Stats degree. ✅
- Streamlit UI and EASY deployment!
    - Extremely happy with the Streamlit library. Wonderfully easy to learn and free to deploy this little app to show this off is just the cherry on top.
- Demonstrate the ability to read external datasets and compile it into a readable and useful output for a user. (Pandas)
- Proficiency with Python
- Hopefully clean, understandable, and expandable code. (This is definitely something I want to get good feedback on.)
- Work on and complete a demo sized thing for a hackathon! Finishing a project up to a Minimum Viable product is just rewarding. 

Thanks to Boot.dev team for running this!