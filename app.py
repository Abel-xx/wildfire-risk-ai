import streamlit as st
import requests
from geopy.geocoders import Nominatim
import plotly.express as px
import pandas as pd

# 1. Page Configuration & Space-Borne Theme Injection
st.set_page_config(page_title="BlazeTrack AI | Radar", layout="wide", page_icon="🔥")

# Advanced UI CSS styling for the rectangle popup container card
st.markdown("""
    <style>
    .alert-card {
        background-color: #0d1117;
        border: 2px solid #ff4b4b;
        border-radius: 8px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
    }
    .alert-card-low {
        background-color: #0d1117;
        border: 2px solid #00ffcc;
        border-radius: 8px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
    }
    .card-title {
        color: #ff4b4b;
        font-family: 'Courier New', monospace;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .card-title-low {
        color: #00ffcc;
        font-family: 'Courier New', monospace;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .section-header {
        color: #66fcf1;
        font-weight: bold;
        margin-top: 10px;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ BLAZETRACK AI : TARGET INTELLIGENCE RADAR")
st.caption("Advanced Multi-Modal Satellite Synthesis Engine // Pure Python Protocol")
st.divider()

# 2. Extract NASA Key Securely from Cloud Settings
NASA_API_KEY = st.secrets.get("NASA_API_KEY", "MISSING")

# Initialize Geocoding Engine
geolocator = Nominatim(user_agent="blazetrack_ai_popup_intelligence")

# Main Dashboard Layout Grid
col_ctrl, col_globe = st.columns([1, 1.2])

with col_ctrl:
    st.markdown("### 🔍 Area Targeting")
    location_input = st.text_input(
        "INPUT GEOGRAPHIC AREA TO ANALYZE:", 
        value="Amazon Rainforest",
        help="Type any city, state, country, or geographical region across the globe."
    )
    st.divider()

    # Default baseline variables if search fails or is empty
    lat, lon = -3.4653, -62.2159  
    temp, rh, wind, soil_moist, vulnerability_score, active_fires_count = 25, 40, 15, 0.25, 30, 0
    map_data = []

    if location_input:
        try:
            # STEP A: Dynamic Area Geocoding
            location = geolocator.geocode(location_input)
            if location:
                lat, lon = location.latitude, location.longitude
                st.caption(f"TELEMETRY RECOGNIZED // ADDR: {location.address}")
                st.caption(f"COORD LOCK // LAT: {lat:.4f} // LON: {lon:.4f}")
                
                # STEP B: Live Atmospheric Streaming (Open-Meteo API)
                weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_moisture_0_to_7cm&forecast_days=1"
                weather_res = requests.get(weather_url).json()
                
                current_data = weather_res["current"]
                temp = current_data["temperature_2m"]
                rh = current_data["relative_humidity_2m"]
                wind = current_data["wind_speed_10m"]
                soil_moist = current_data.get("soil_moisture_0_to_7cm", 0.25)

                # STEP C: NASA Thermal Satellite Pipeline
                if NASA_API_KEY != "MISSING" and NASA_API_KEY != "":
                    buffer = 0.5  
                    bbox = f"{lon-buffer},{lat-buffer},{lon+buffer},{lat+buffer}"
                    firms_url = f"https://nasa.gov{NASA_API_KEY}/VIIRS_SNPP_NRT/{bbox}/1"
                    firms_res = requests.get(firms_url)
                    
                    if firms_res.status_code == 200 and "latitude" in firms_res.text:
                        lines = firms_res.text.strip().split('\n')[1:]
                        active_fires_count = len(lines)
                        for idx, line in enumerate(lines):
                            f_data = line.split(',')
                            map_data.append({
                                "Point ID": f"NASA-SPOT-{idx+1}",
                                "Latitude": float(f_data), 
                                "Longitude": float(f_data), 
                                "Status": "NASA Anomaly Spot", 
                                "Indicator Size": 12,
                                "Local Temp": f"{temp} °C",
                                "Vulnerability": 95,
                                "Main Causes": f"Active satellite thermal trigger at coordinates. High heat spikes ({temp}°C) combined with wind velocities.",
                                "Precautions": "Enact immediate local containment. Evacuate non-essential personnel within a 15km perimeter zone.",
                                "Suggestions": "Deploy aerial tracking assets. Coordinate real-time satellite updates every 3 hours to monitor line vector shifts."
                            })
                
                # STEP D: Predictive Risk Engine Calculation
                temp_factor = min(max((temp - 10) / 30, 0), 1) * 30
                rh_factor = min(max((100 - rh) / 80, 0), 1) * 30
                wind_factor = min(max(wind / 50, 0), 1) * 20
                fuel_factor = min(max((1.0 - soil_moist) / 1.0, 0), 1) * 20
                vulnerability_score = int(temp_factor + rh_factor + wind_factor + fuel_factor)
                
                if active_fires_count > 0:
                    vulnerability_score = min(vulnerability_score + 15, 100)

                # Determine explicit causes based on atmospheric weights
                causes_list = []
                if temp > 30: causes_list.append(f"Extreme air temperature ({temp}°C)")
                if rh < 35: causes_list.append(f"Critical low relative humidity ({rh}%) causing combustible atmosphere")
                if wind > 25: causes_list.append(f"High wind velocity ({wind} km/h) accelerating oxygen feed risk")
                if soil_moist < 0.20: causes_list.append(f"Arid soil fuel density ({soil_moist} m³/m³) causing high ignition vulnerability")
                if active_fires_count > 0: causes_list.append(f"Proximity to {active_fires_count} active thermal satellite anomalies")
                
                main_causes_str = " // ".join(causes_list) if causes_list else "All atmospheric variables operating within safe baseline parameters."
                
                precautions_str = "Issue red flag warnings. Pre-position local suppression assets. Ban all agricultural burning lines." if vulnerability_score >= 50 else "Maintain routine drone observation streams. Standard agricultural protocols remain active."
                suggestions_str = "Integrate live satellite synthetic aperture radar (SAR) tracking to map underlying canopy moisture changes." if vulnerability_score >= 50 else "Optimize backend algorithms; refresh system records in 24 hours."

                # Append Searched Target Center data parameters for map plot
                map_data.append({
                    "Point ID": "TARGET-CENTER",
                    "Latitude": lat, 
                    "Longitude": lon, 
                    "Status": "Primary Search Center", 
                    "Indicator Size": 18,
                    "Local Temp": f"{temp} °C",
                    "Vulnerability": vulnerability_score,
                    "Main Causes": main_causes_str,
                    "Precautions": precautions_str,
                    "Suggestions": suggestions_str
                })
            else:
                st.error("❌ Location query failed. System unable to resolve area name.")
        except Exception as e:
            st.error(f"Telemetry Pipeline Error: {e}")

    # Render UI Telemetry Panels
    st.markdown("### 📊 Live Core Indicators")
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("AIR TEMP", f"{temp} °C")
    m_col2.metric("HUMIDITY", f"{rh} %")
    
    m_col3, m_col4 = st.columns(2)
    m_col3.metric("WIND VELOCITY", f"{wind} km/h")
    m_col4.metric("SATELLITE ALARMS", f"{active_fires_count}")

with col_globe:
    st.markdown("### 🌐 Interoperable 3D Earth Globe View")
    
    # Generate DataFrame for Plotly Engine
    if not map_data:
        map_data.append({
            "Point ID": "TARGET-CENTER", "Latitude": lat, "Longitude": lon, 
            "Status": "Primary Search Center", "Indicator Size": 18, "Local Temp": f"{temp} °C", 
            "Vulnerability": vulnerability_score, "Main Causes": "Initialization pending...",
            "Precautions": "N/A", "Suggestions": "N/A"
        })
    df_globe = pd.DataFrame(map_data)
    
    # Render 3D Globe with Clickable Interactivity attributes
    fig = px.scatter_geo(
        df_globe, lat="Latitude", lon="Longitude", color="Status", size="Indicator Size",
        color_discrete_map={"Primary Search Center": "#00ffff", "NASA Anomaly Spot": "#ff4b4b"},
        hover_data={"Status": True, "Vulnerability": True, "Local Temp": True, "Latitude": ":.4f", "Longitude": ":.4f", "Indicator Size": False},
        projection="orthographic"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
        geo=dict(showland=True, landcolor="#11161d", showocean=True, oceancolor="#07090c", showcountries=True, countrycolor="#232b35", projection_rotation=dict(lon=lon, lat=lat, roll=0))
    )
    st.plotly_chart(fig, use_container_width=True)

# 3. Interactive Data Table Inspector with Click Capture
st.markdown("### 📑 Multi-Modal Target Telemetry Inspector")
st.caption("👉 Click on any row entry in the table below to open the stylish, advanced tactical alert popup card.")

selection = st.dataframe(df_globe[["Point ID", "Status", "Vulnerability", "Local Temp", "Latitude", "Longitude"]],use_container_width=True,hide_index=True,on_select="rerun", # Forces application to execute instantly upon selection clickselection_mode="single-row")
if selection and selection["rows"]:selected_row_index = selection["rows"][0]selected_node = df_globe.iloc[selected_row_index]# Extract row parametersv_score = selected_node["Vulnerability"]card_style = "alert-card" if v_score >= 50 else "alert-card-low"title_style = "card-title" if v_score >= 50 else "card-title-low"icon = "🚨" if v_score >= 50 else "🛡️"# Render the custom card HTML container wrapper blockst.markdown(f"""{icon} DETAILED TARGET INTELLIGENCE: {selected_node['Point ID']}{v_score}% Vulnerability{selected_node['Main Causes']}{selected_node['Precautions']}{selected_node['Suggestions']}""", unsafe_allow_html=True)
else:
st.info("ℹ️ Select a telemetry row inside the inspector grid above to generate the specialized tactical response briefing card.")
