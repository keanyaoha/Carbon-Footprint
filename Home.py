import streamlit as st

# --- App Config ---
st.set_page_config(
    page_title="Green Tomorrow",
    page_icon="🌿",
    layout="centered"
)

# --- Force Logo to Appear at Top of Sidebar ---
st.markdown(
    """
    <style>
      [data-testid="stSidebar"]::before {
      content: "";
      display: block;
      background-image: url('/static/GreenPrint_logo.png');
      background-size: 90% auto;
      background-repeat: no-repeat;
      background-position: center;
      height: 140px;
      margin: 1.5rem auto -4rem auto;
   }

        section[data-testid="stSidebar"] {
            background-color: #d6f5ec;
        }

        .stApp {
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Main App Content ---
st.title("Welcome to GreenPrint")
st.subheader("Your Personal Carbon Footprint Tracker")

st.markdown("""
**GreenPrint** is an interactive tool designed to help you measure your **carbon footprint** — the total amount of greenhouse gas emissions, that your lifestyle and choices emit into the atmosphere.

---

### 🧠 What is a Carbon Footprint?

A **carbon footprint** includes emissions from:
- 🏠 Household energy use (heating, electricity)
- 🚗 Transportation (car, flights, public transport)
- 🍔 Food and consumption habits
- 🛒 Shopping, waste, and more

It's measured in **kg of CO₂ equivalent (CO₂e)**.

---

### 🚨 Why It Matters

At GreenPrint we believe that our planet is finite and there is a need for sustainability. 
Consumption of resources leads to greenhouse gas emissions, 
which are responsible for global warming and other environmental challenges such as floods, forest fires,
drought, conflict and ecological damage.

The higher our carbon footprint, the more we contribute to climate change. By understanding your own emissions, you can:

- Reduce your environmental impact  
- Save money through efficient choices  
- Join the global effort to combat the climate crisis  

---

### 🛠️ How This App Works

1. Go to the **Profile** page and create your profile, which brings you directly to the **Calculator** and enter details about your daily habits.  
2. Get an estimate of your **monthly carbon footprint**.  
3. Compare your score to **national, European and global averages**.  
4. See personalized suggestions on how to **reduce** it.

---

### 🌿 Ready to make a difference?

Start by heading to the **Profile** page in the sidebar!
""")
