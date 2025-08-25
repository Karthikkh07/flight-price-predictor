import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# -------------------- Page Config --------------------
st.set_page_config(
    layout="wide",
    page_title="✈️ Flight Price Predictor",
    page_icon="✈️"
)

# -------------------- Custom CSS & Background --------------------
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1504198266280-5c4f47d3b3df?auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Sidebar */
    .stSidebar .css-1d391kg {
        background-color: rgba(10, 25, 50, 0.85);
        color: #ffffff;
    }

    /* Button */
    .stButton>button {
        background-color:#0077b6;
        color:white;
        border:none;
        padding: 0.5em 1em;
        font-weight: bold;
    }

    /* Text & headers */
    h1, h2, h3, h4, h5 {
        color: #caf0f8;
        text-shadow: 1px 1px 2px black;
    }
    
    /* Table colors */
    .stDataFrame table {
        color: #03045e;
        background-color: rgba(255,255,255,0.85);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Sidebar: Flight Input --------------------
st.sidebar.title("✈️ Enter Flight Details")

# Airline icons
airline_icons = {
    "IndiGo": "🛩️",
    "Air India": "🇮🇳",
    "SpiceJet": "✈️",
    "GoAir": "🛫",
    "Vistara": "🌟"
}

airline = st.sidebar.selectbox(
    "Airline",
    [f"{icon} {name}" for name, icon in airline_icons.items()]
)
source = st.sidebar.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai", "Bangalore"])
destination = st.sidebar.selectbox("Destination", ["Cochin", "Delhi", "New Delhi", "Hyderabad", "Kolkata"])
total_stops = st.sidebar.selectbox("Total Stops", [0, 1, 2, 3, 4])
journey_date = st.sidebar.date_input("Date of Journey")
dep_time = st.sidebar.time_input("Departure Time")
arr_time = st.sidebar.time_input("Arrival Time")
route = st.sidebar.text_input("Route (optional)", "NA")
additional_info = st.sidebar.text_input("Additional Info", "No info")

# Filters
st.sidebar.subheader("Flight Filters")
direct_only = st.sidebar.checkbox("Direct Flights Only")
max_stops = st.sidebar.slider("Max Stops", 0, 4, total_stops)

# -------------------- Main Title & Subtitle --------------------
st.markdown(
    """
    <h1 style="color:#00b4d8; text-shadow: 1px 1px 2px black;">✈️ Flight Price Predictor</h1>
    <h3 style="color:#caf0f8; text-shadow: 1px 1px 2px black;">
    Predict flight ticket prices using Machine Learning + Streamlit 💡
    </h3>
    """,
    unsafe_allow_html=True
)

# -------------------- Dummy Prediction --------------------
predicted_price = np.random.randint(4300, 4700) + np.random.randint(-100, 100)
actual_avg_price = 4500
difference = predicted_price - actual_avg_price

if st.sidebar.button("🚀 Predict Fare"):
    st.text("Fetching flight data... ⏳")
    time.sleep(1.5)  # Simulate API delay

    st.success(f"💰 Predicted Flight Price: ₹{predicted_price:.2f}")
    
    # Prediction Summary Card
    st.markdown(f"""
    <div style="background-color: rgba(0,119,182,0.6); padding: 15px; border-radius: 10px;">
        <h3>🛫 Flight Prediction Summary</h3>
        <p><b>Airline:</b> {airline}</p>
        <p><b>Source → Destination:</b> {source} → {destination}</p>
        <p><b>Journey Date:</b> {journey_date}</p>
        <p><b>Actual Avg Price:</b> ₹{actual_avg_price}</p>
        <p><b>Predicted Price:</b> ₹{predicted_price} ± 300</p>
        <p><b>Difference:</b> {'+' if difference > 0 else ''}₹{difference}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Prices fluctuate based on season, demand, and availability!")

    # -------------------- Prediction History --------------------
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    st.session_state['history'].append({
        "Airline": airline,
        "Source": source,
        "Destination": destination,
        "Date": journey_date,
        "Predicted Price": predicted_price
    })

# Show history table
if 'history' in st.session_state and st.session_state['history']:
    df_history = pd.DataFrame(st.session_state['history'])
    st.markdown("### 🗂️ Prediction History")
    st.dataframe(df_history, use_container_width=True)

    st.download_button(
        "⬇️ Download History CSV",
        df_history.to_csv(index=False),
        "flight_prediction_history.csv",
        "text/csv"
    )

# -------------------- Flight Fare Dashboard --------------------
st.markdown("## 📊 Flight Fare Dashboard")

# Example Data for Charts
df = pd.DataFrame({
    "Airline": ["IndiGo", "Air India", "SpiceJet", "GoAir", "Vistara"],
    "Actual Price": [4800, 6300, 3900, 5200, 7500],
    "Duration (mins)": [150, 180, 120, 160, 190],
    "Predicted Price": [4283, 4595, 3469, 4063, 4239]
})

# Chart 1: Actual vs Predicted
fig1 = px.bar(
    df.melt(id_vars="Airline", value_vars=["Actual Price", "Predicted Price"], 
            var_name="Type", value_name="Value"),
    x="Airline", y="Value", color="Type", barmode="group", 
    title="Actual vs Predicted Flight Prices",
    color_discrete_map={"Actual Price": "#0077b6", "Predicted Price": "#caf0f8"}
)
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                   font_color="white", transition={'duration': 500, 'easing': 'cubic-in-out'})
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Airline vs Duration
fig2 = px.line(df, x="Airline", y="Duration (mins)", markers=True,
               title="Airline vs Duration", line_shape='spline')
fig2.update_traces(line=dict(color='#90e0ef', width=4))
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                   font_color="white")
st.plotly_chart(fig2, use_container_width=True)

# Table
st.dataframe(df, use_container_width=True)
