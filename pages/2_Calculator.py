import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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
            margin: 1.5rem auto -4rem auto;  /* SUPER tight top & bottom spacing */
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

# --- Load Data ---
csv_url = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/emission_factor_formated.csv"
csv_url_1 = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/per_capita_filtered_monthly.csv"

try:
    df = pd.read_csv(csv_url)
    df1 = pd.read_csv(csv_url_1)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

available_countries = [col for col in df.columns if col != "Activity"]

# Function to format activity names
def format_activity_name(activity):
    activity_mappings = {
        "Domestic_flight": "How many km of Domestic Flights taken the last month",
        "International_flight": "How many km of International Flights taken the last month",
        "Diesel_train_local": "How many km traveled by diesel-powered local passenger trains the last month",
        "Diesel_train_long": "How many km traveled by diesel-powered long-distant passenger trains the last month",
        "Electric_train": "How many km traveled by electric-powered passenger trains the last month",
        "Bus": "How many km traveled by bus the last month",
        "Petrol_car": "How many km traveled by petrol-powered car the last month",
        "Motorcycle": "How many km traveled by motorcycle the last month",
        "Ev_scooter": "How many km traveled by electric scooter the last month",
        "Ev_car": "How many km traveled by electric-powered car the last month",
        "Diesel_car": "How many km traveled by diesel-powered car the last month",
        "Water": "How much water consumed in liters the last month",
        "Electricity": "How much electricity used in kWh the last month",
        "Beef": "How much beef consumed in kg the last month",
        "Beverages": "How much beverages consumed in liters the last month",
        "Poultry": "How much poultry consumed in Kg the last month",
        "Pork": "How much pork have you consumed in kg the last month",
        "Rice": "How much processed rice consumed in kg the last month",
        "Sugar": "How much sugar have you consumed in kg the last month",
        "Oils_fats": "How much vegetable oils and fats consumed in kg the last month",
        "Other_meat": "How much other meat products consumed in kg the last month",
        "Dairy": "How much dairy products consumed in kg the last month",
        "Fish_products": "How much fish products consumed in kg the last month",
        "Other_food": "How much other food products have you consumed in kg the last month",
        "Hotel_stay": "How many nights stayed in hotels the last month"
    }
    return activity_mappings.get(activity, activity.replace("_", " ").capitalize())

# --- UI Layout ---
st.title("Carbon Footprint Calculator")
st.markdown("Calculate your carbon footprint and compare it to national and global averages!")

# --- Step 1: Country Selection ---
st.markdown("### \U0001F30D Select your country of residence:")
def_country = "-- Select --"
country = st.selectbox(" ", [def_country] + available_countries)

# Continue only if valid country is selected
if country != def_country:
    st.success(
        "✅ **Next steps:**\n"
        "Please go through the **Travel**, **Food**, **Energy & Water**, and **Other** tabs.\n"
        "Fill in any values relevant to you. When you're ready, click *\u201cCalculate My Carbon Footprint\u201d* at the bottom."
    )

    # --- Tabs ---
    tabs = st.tabs(["\U0001F697 Travel", "\U0001F37D Food", "⚡ Energy & Water", "\U0001F3E8 Other"])

    # --- Travel Tab ---
    with tabs[0]:
        travel_activities = [
            "Domestic_flight", "International_flight", "Diesel_train_local",
            "Diesel_train_long", "Electric_train",
            "Bus", "Petrol_car", "Motorcycle",
            "Ev_scooter", "Ev_car", "Diesel_car"
        ]
        for activity in travel_activities:
            st.number_input(format_activity_name(activity), min_value=0.0, key=activity)
       
    # --- Food Tab ---
    with tabs[1]:
        diet_type = st.selectbox("\U0001F957 What is your diet type?", [
            "Select...", "Vegan", "Vegetarian", "Pescatarian", "Omnivore", "Heavy Meat Eater"])

        if diet_type != "Select...":
            st.markdown("#### Now please answer the following questions:")
            st.markdown("How much of the following foods do you consume on average per month?")

            base_foods = [
                "Rice", "Sugar", "Oils_fats",
                "Other_food", "Beverages"]

            diet_foods = {
                "Vegan": [],
                "Vegetarian": ["Dairy", "Other_meat"],
                "Pescatarian": ["Fish_products", "Dairy"],
                "Omnivore": ["Beef", "Poultry", "Pork",
                             "Dairy", "Fish_products"],
                "Heavy Meat Eater": ["Beef", "Poultry", "Pork",
                                     "Dairy", "Fish_products", "Other_meat"]
            }

            food_activities = base_foods + diet_foods.get(diet_type, [])
            for activity in food_activities:
                label = activity.replace("_", " ").replace("products", "").replace("consumed", "").strip().capitalize()
                value = st.number_input(f"{label}", min_value=0.0, key=activity, format="%.1f")
                # st.markdown(f"<div class='unit-label'>kg</div>", unsafe_allow_html=True)

    # --- Energy & Water Tab ---
    with tabs[2]:
        for activity in ["Electricity", "Water"]:
            st.number_input(format_activity_name(activity), min_value=0.0, key=activity)

    # --- Other Tab ---
    with tabs[3]:
        st.number_input(format_activity_name("Hotel_stay"), min_value=0.0, key="Hotel_stay")

    # --- Confirmation Checkbox ---
    st.markdown("---")
    confirmed = st.checkbox("I have reviewed all fields and want to calculate my footprint")
    calculate = st.button("Calculate My Carbon Footprint", disabled=not confirmed)

    if calculate:
        if "emission_values" not in st.session_state:
            st.session_state.emission_values = {}

        for activity in df["Activity"]:
            if activity in st.session_state:
                factor = df.loc[df["Activity"] == activity, country].values[0]
                user_input = st.session_state.get(activity, 0.0)
                st.session_state.emission_values[activity] = user_input * factor

        total_emission = sum(st.session_state.emission_values.values())
        st.subheader(f"\U0001F30D Your Carbon Footprint: {total_emission:.1f} kg CO₂")

        # Tree equivalent
        trees_cut = total_emission / 21.77
        st.markdown(f"\U0001F333 **That’s equivalent to cutting down ~{trees_cut:.0f} trees!**")

        def get_per_capita_emission(country_name):
            match = df1.loc[df1["Country"] == country_name, "PerCapitaCO2"]
            return match.iloc[0] if not match.empty else None

        country_avg = get_per_capita_emission(country)
        eu_avg = get_per_capita_emission("European Union (27)")
        world_avg = get_per_capita_emission("World")

        labels = ['You', country, 'EU', 'World']
        values = [
            total_emission,
            country_avg if country_avg is not None else 0,
            eu_avg if eu_avg is not None else 0,
            world_avg if world_avg is not None else 0
        ]
        user_color = '#4CAF50' if total_emission < values[3] else '#FF4B4B'
        shared_color = '#4682B4'
        colors = [user_color] + [shared_color] * 3

        labels, values, colors = labels[::-1], values[::-1], colors[::-1]

        fig, ax = plt.subplots(figsize=(8, 3.2))
        bars = ax.barh(labels, values, color=colors, height=0.6)
        ax.set_xlim(0, max(values) + 0.1 * max(values))

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f'{width:.1f}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0), textcoords='offset points',
                        ha='left', va='center')

        ax.set_xlabel("Tons CO₂ per year")
        ax.xaxis.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("""
            <div style='text-align: center; color: gray;'>
            Comparison of your estimated annual carbon footprint with national and global averages.
            </div>
        """, unsafe_allow_html=True)
