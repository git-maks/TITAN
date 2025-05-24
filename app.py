import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Added for go.Scattermapbox
import time
import datetime # Added for timestamps
import random # For more varied simulation

# Page Configuration
st.set_page_config(
    page_title="Space25 Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'comm_channels' not in st.session_state:
    # Define Poland's approximate bounding box for LoRa generation
    POLAND_BOUNDS = {"min_lat": 49.0, "max_lat": 54.8, "min_lon": 14.1, "max_lon": 24.1}
    NUM_LORA_MODULES = 40 # Increased number of LoRa modules

    initial_channels = [
        # TETRA BTS
        {"id": "tetra_bts_001", "type": "TETRA BTS", "name": "Warsaw Central BTS", "lat": 52.2370, "lon": 21.0175, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Nominal operation."},
        {"id": "tetra_bts_002", "type": "TETRA BTS", "name": "Krakow Main BTS", "lat": 50.0647, "lon": 19.9450, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Covering southern region."},
        {"id": "tetra_bts_003", "type": "TETRA BTS", "name": "Gdansk Port BTS", "lat": 54.3721, "lon": 18.6383, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Maritime and city coverage."},
        {"id": "tetra_bts_004", "type": "TETRA BTS", "name": "Wroclaw Industrial BTS", "lat": 51.1079, "lon": 17.0385, "status": "Offline", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Under maintenance."},


        # TETRA Repeaters
        {"id": "tetra_rep_001", "type": "TETRA Repeater", "name": "Mazovian Plains Repeater", "lat": 52.5000, "lon": 21.5000, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Coverage extension for Warsaw outskirts."},
        {"id": "tetra_rep_002", "type": "TETRA Repeater", "name": "Silesian Uplands Repeater", "lat": 50.2649, "lon": 19.0238, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Enhancing coverage in Katowice area."},
        {"id": "tetra_rep_003", "type": "TETRA Repeater", "name": "Pomeranian Lakes Repeater", "lat": 54.0000, "lon": 17.5000, "status": "Alert", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Intermittent signal issues reported."},

        # Satellite Earth Stations (Fixed)
        {"id": "sat_fixed_001", "type": "Satellite Earth Station (Fixed)", "name": "Poznan Uplink Center", "lat": 52.4064, "lon": 16.9252, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Primary national uplink."},
        {"id": "sat_fixed_002", "type": "Satellite Earth Station (Fixed)", "name": "Lublin Backup Hub", "lat": 51.2465, "lon": 22.5684, "status": "Standby", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Backup satellite gateway."},

        # Starlink Gov Terminals
        {"id": "starlink_gov_001", "type": "Starlink Gov Terminal", "name": "Rzeszow Gov Starlink", "lat": 50.0412, "lon": 21.9990, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "High-speed government comms."},
        {"id": "starlink_gov_002", "type": "Starlink Gov Terminal", "name": "Border Guard East Starlink", "lat": 51.5000, "lon": 23.5000, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Eastern border surveillance support."},
        {"id": "starlink_gov_003", "type": "Starlink Gov Terminal", "name": "Szczecin Port Authority Starlink", "lat": 53.4289, "lon": 14.5530, "status": "Jammed", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Suspected GPS spoofing affecting terminal."},


        # Military Mobile Connectivity Hub (MCC1)
        {"id": "mcc1_001", "type": "Military Mobile Connectivity Hub (MCC1)", "name": "MCC1 Unit Alpha (Warsaw)", "lat": 52.2500, "lon": 20.9800, "status": "Standby", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Ready for deployment."},
        {"id": "mcc1_002", "type": "Military Mobile Connectivity Hub (MCC1)", "name": "MCC1 Unit Bravo (Krakow)", "lat": 50.0800, "lon": 19.9000, "status": "Standby", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Reserve unit, ready for deployment."},
        {"id": "mcc1_003", "type": "Military Mobile Connectivity Hub (MCC1)", "name": "MCC1 Unit Charlie (Poznan)", "lat": 52.4100, "lon": 16.9000, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Deployed for training exercise."},

        # Airport Control Towers
        {"id": "act_001", "type": "Airport Control Tower", "name": "Warsaw Chopin Airport Tower", "lat": 52.1657, "lon": 20.9671, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Full operational capacity."},
        {"id": "act_002", "type": "Airport Control Tower", "name": "Krakow Balice Airport Tower", "lat": 50.0777, "lon": 19.7848, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Nominal operations."},
        {"id": "act_003", "type": "Airport Control Tower", "name": "Gdansk Lech Walesa Airport Tower", "lat": 54.3775, "lon": 18.4661, "status": "Alert", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Radar system undergoing checks."},

        # Emergency Operation Centers
        {"id": "eoc_001", "type": "Emergency Operation Center", "name": "National EOC Warsaw", "lat": 52.2400, "lon": 21.0300, "status": "Active", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Coordinating national emergency response."},
        {"id": "eoc_002", "type": "Emergency Operation Center", "name": "Regional EOC Wroclaw", "lat": 51.1100, "lon": 17.0300, "status": "Standby", "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "notes": "Ready for regional activation."},
    ]

    # Generate LoRa Modules
    for i in range(NUM_LORA_MODULES):
        lat = random.uniform(POLAND_BOUNDS["min_lat"], POLAND_BOUNDS["max_lat"])
        lon = random.uniform(POLAND_BOUNDS["min_lon"], POLAND_BOUNDS["max_lon"])
        status = random.choice(["Active", "Offline", "Alert"])
        initial_channels.append({
            "id": f"lora_sensor_{i+1:03d}",
            "type": "LoRa Module",
            "name": f"LoRa Sensor {i+1}",
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "status": status,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": f"Automated sensor node. Status: {status}"
        })
    
    st.session_state.comm_channels = initial_channels
if 'incidents' not in st.session_state:
    st.session_state.incidents = []

if 'simulation_time_step' not in st.session_state:
    st.session_state.simulation_time_step = 0 # Retain for internal logic, but don't display directly
if 'last_refresh_time' not in st.session_state:
    st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Simulation Functions ---
def update_channel_status(channel_id, new_status, notes_update=""):
    for channel in st.session_state.comm_channels:
        if channel["id"] == channel_id:
            channel["status"] = new_status
            channel["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if notes_update:
                channel["notes"] = notes_update
            break

def log_incident(description, severity="Medium", affected_channel_id=None):
    st.session_state.incidents.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": description,
        "severity": severity,
        "affected_channel_id": affected_channel_id
    })

def run_simulation_step():
    st.session_state.simulation_time_step += 1
    step = st.session_state.simulation_time_step
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # More varied and complex scenarios
    # Ensure channels exist before trying to update them
    channel_ids = [c['id'] for c in st.session_state.comm_channels]

    if step == 2 and "tetra_rep_001" in channel_ids:
        if any(c["id"] == "tetra_rep_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            update_channel_status("tetra_rep_001", "Offline", f"Power failure reported at {now_str}.")
            log_incident("Mazovian Plains Repeater (tetra_rep_001) Offline due to power failure.", "High", "tetra_rep_001")

    if step == 4 and "tetra_bts_001" in channel_ids:
        if any(c["id"] == "tetra_bts_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            update_channel_status("tetra_bts_001", "Jammed", f"Suspected widespread jamming campaign. {now_str}.")
            log_incident("Warsaw Central BTS (tetra_bts_001) Jammed.", "Critical", "tetra_bts_001")

    if step == 6 and "lora_water_001" in channel_ids:
        if any(c["id"] == "lora_water_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            bts_jammed = any(c["id"] == "tetra_bts_001" and c["status"] == "Jammed" for c in st.session_state.comm_channels)
            if bts_jammed:
                update_channel_status("lora_water_001", "Alert", f"Detected TETRA network anomalies. {now_str}.")
                log_incident("Vistula Water Plant Sensor (lora_water_001) detected TETRA anomalies.", "Medium", "lora_water_001")
    
    if step == 7 and "lora_hospital_001" in channel_ids:
        if any(c["id"] == "lora_hospital_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            repeater_offline = any(c["id"] == "tetra_rep_001" and c["status"] == "Offline" for c in st.session_state.comm_channels)
            if repeater_offline:
                update_channel_status("lora_hospital_001", "Alert", f"Primary repeater (tetra_rep_001) offline. {now_str}.")
                log_incident("Gdansk Hospital Comms Monitor (lora_hospital_001) reports primary repeater offline.", "High", "lora_hospital_001")

    if step == 8 and "mcc1_001" in channel_ids:
        bts_jammed = any(c["id"] == "tetra_bts_001" and c["status"] == "Jammed" for c in st.session_state.comm_channels)
        mcc1_standby = any(c["id"] == "mcc1_001" and c["status"] == "Standby" for c in st.session_state.comm_channels)
        if bts_jammed and mcc1_standby:
            update_channel_status("mcc1_001", "Active", f"Deployed to cover Warsaw Central BTS outage. {now_str}.")
            log_incident("MCC1 Unit Alpha (mcc1_001) activated for Warsaw BTS.", "Low", "mcc1_001")

    if step == 10 and "starlink_gov_001" in channel_ids:
        if any(c["id"] == "starlink_gov_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            # Condition: if any major TETRA component is down
            tetra_issues = any(c["type"].startswith("TETRA") and c["status"] != "Active" for c in st.session_state.comm_channels)
            if tetra_issues:
                update_channel_status("starlink_gov_001", "Active", f"Increased bandwidth demand due to regional outages. {now_str}.")
                # No new incident, just updating notes of an active channel
    
    if step == 12 and "mcc1_002" in channel_ids:
        bts_jammed = any(c["id"] == "tetra_bts_001" and c["status"] == "Jammed" for c in st.session_state.comm_channels)
        repeater_offline = any(c["id"] == "tetra_rep_001" and c["status"] == "Offline" for c in st.session_state.comm_channels)
        mcc2_standby = any(c["id"] == "mcc1_002" and c["status"] == "Standby" for c in st.session_state.comm_channels)
        if (bts_jammed and repeater_offline) and mcc2_standby:
            update_channel_status("mcc1_002", "Active", f"Deployed for wide area backup due to multiple outages. {now_str}.")
            log_incident("MCC1 Unit Bravo (mcc1_002) activated for wide area backup.", "Medium", "mcc1_002")
    
    # Random event: A random LoRa module might go offline temporarily
    if step > 5 and random.random() < 0.1: # 10% chance each step after step 5
        lora_channels = [c for c in st.session_state.comm_channels if c["type"] == "LoRa Module" and c["status"] == "Active"]
        if lora_channels:
            chosen_lora = random.choice(lora_channels)
            update_channel_status(chosen_lora["id"], "Offline", f"Temporary sensor glitch. {now_str}.")
            log_incident(f"LoRa Module {chosen_lora['name']} ({chosen_lora['id']}) went temporarily offline.", "Low", chosen_lora["id"])
            # Add a recovery step for this LoRa?
            # For now, it stays offline to show the event. Could add logic for it to come back online later.

    # Random event: A Starlink terminal might experience brief intermittent connectivity
    if step > 8 and random.random() < 0.05: # 5% chance
        starlink_terminals = [c for c in st.session_state.comm_channels if c["type"] == "Starlink Gov Terminal" and c["status"] == "Active"]
        if starlink_terminals:
            chosen_starlink = random.choice(starlink_terminals)
            original_notes = chosen_starlink.get("notes", "")
            update_channel_status(chosen_starlink["id"], "Alert", f"Brief intermittent connectivity reported. {now_str}. Original: {original_notes}")
            log_incident(f"Starlink Terminal {chosen_starlink['name']} ({chosen_starlink['id']}) experiencing intermittent connectivity.", "Medium", chosen_starlink["id"])
            # It could return to "Active" in a subsequent step.

# Main App Title
st.title("Space25 Communications Dashboard")

# Navbar
col1, col2, col3 = st.columns([1,2,1])
with col1:
    # Display last refresh time instead of simulation step
    st.metric(label="System Status", value="Online", delta=f"Last Update: {st.session_state.last_refresh_time}")
with col3:
    # Change button label
    if st.button("🔄 Refresh Network Status"):
        run_simulation_step() # Internally, this still advances the simulation state
        st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Go to",
    ["🗺️ Map Overview", "📊 Incident Reports", "⚙️ Manual Control", "🔧 Settings"],
)

# Conditional Page Display
if app_mode == "🗺️ Map Overview":
    st.subheader("🗺️ Map Overview")
    if st.session_state.comm_channels:
        df_channels = pd.DataFrame(st.session_state.comm_channels)
        
        status_colors = {
            "Active": "green",
            "Offline": "darkgrey", 
            "Jammed": "red",
            "Alert": "orange",
            "Standby": "blue"
        }

        symbol_map = {
            "TETRA BTS": "triangle-up",
            "TETRA Repeater": "triangle-down",
            "Satellite Earth Station (Fixed)": "star",
            "Starlink Gov Terminal": "diamond",
            "LoRa Module": "circle", 
            "Military Mobile Connectivity Hub (MCC1)": "hexagon",
            "Airport Control Tower": "square",
            "Emergency Operation Center": "pentagon",
            "Other": "cross"
        }
        
        # --- Fallback to plotly.graph_objects due to persistent TypeError ---
        # This typically indicates an older Plotly version or environment issue.
        # Strongly consider:
        # 1. Verifying Plotly version: In a Python terminal, run:
        #    import plotly
        #    print(plotly.__version__)
        #    (Should be >= 5.0 for best compatibility with px.scatter_mapbox symbol argument)
        # 2. Forcing environment update: 
        #    pip uninstall plotly
        #    pip install -r requirements.txt --force-reinstall --no-cache-dir
        #    (Ensure requirements.txt contains 'plotly>=5.10.0')

        fig = go.Figure()

        for channel_type, group_by_type in df_channels.groupby('type'):
            symbol_for_type = symbol_map.get(channel_type, 'cross') # Default symbol
            
            for status, group_by_status_and_type in group_by_type.groupby('status'):
                color_for_status = status_colors.get(status, 'grey') # Default color

                hover_texts = []
                custom_data_list = []
                for _idx, row in group_by_status_and_type.iterrows():
                    hover_texts.append(row['name'])
                    custom_data_list.append([
                        row['type'], 
                        row['status'], 
                        row['last_updated'], 
                        row['notes']
                    ])
                
                fig.add_trace(go.Scattermapbox(
                    lat=group_by_status_and_type['lat'],
                    lon=group_by_status_and_type['lon'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=12,
                        symbol=symbol_for_type,
                        color=color_for_status
                    ),
                    name=f"{channel_type} - {status}", # Legend entry
                    text=hover_texts,
                    customdata=custom_data_list,
                    hovertemplate=
                        "<b>%{text}</b><br><br>" +
                        "Type: %{customdata[0]}<br>" +
                        "Status: %{customdata[1]}<br>" +
                        "Last Updated: %{customdata[2]}<br>" +
                        "Notes: %{customdata[3]}" +
                        "<extra></extra>" # Hides trace info from hover
                ))
        
        fig.update_layout(
            mapbox_style="carto-positron", # Bright map style
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox_center_lat=52.0,  # Center on Poland
            mapbox_center_lon=19.0,  # Center on Poland
            mapbox_zoom=5.5,         # Zoom level for Poland
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.7)", 
                font=dict(color="black"),
                traceorder="grouped+reversed" # Groups legend items
            )
        )
        # The df_channels['symbol'] column and fig.update_traces(marker=dict(size=12)) are no longer needed with this approach.
        
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("All Communication Channels")
        st.dataframe(df_channels[['id', 'name', 'type', 'status', 'last_updated', 'lat', 'lon', 'notes']], use_container_width=True)
    else:
        st.write("No communication channels to display.")

elif app_mode == "📊 Incident Reports":
    st.subheader("📊 Incident Reports")
    if st.session_state.incidents:
        df_incidents = pd.DataFrame(st.session_state.incidents)
        # Reorder columns for better readability
        df_incidents_display = df_incidents[["timestamp", "description", "severity", "affected_channel_id"]]
        st.dataframe(df_incidents_display, use_container_width=True)
    else:
        st.write("No incidents reported yet.")
elif app_mode == "⚙️ Manual Control":
    st.subheader("⚙️ Manual Control")
    if st.session_state.comm_channels:
        channel_options = {channel["id"]: f"{channel['name']} ({channel['id']})" for channel in st.session_state.comm_channels}
        selected_channel_id = st.selectbox("Select Channel to Update:", options=list(channel_options.keys()), format_func=lambda x: channel_options[x])

        if selected_channel_id:
            current_channel = next((ch for ch in st.session_state.comm_channels if ch["id"] == selected_channel_id), None)
            st.write(f"Current status: {current_channel['status']}")

            status_options = ["Active", "Offline", "Jammed", "Alert", "Standby"]
            # Ensure current status is first in list if it's a valid option, otherwise add it
            if current_channel['status'] in status_options:
                current_status_index = status_options.index(current_channel['status'])
            else:
                status_options.insert(0, current_channel['status']) # Add if not standard
                current_status_index = 0

            new_status = st.selectbox("Select New Status:", options=status_options, index=current_status_index)
            notes_update = st.text_input("Update Notes (optional):", value=current_channel.get("notes", ""))

            if st.button("Apply Status Change"):
                original_status = current_channel['status']
                update_channel_status(selected_channel_id, new_status, notes_update)
                log_incident(
                    description=f"Manual status change for {channel_options[selected_channel_id]}. Status changed from '{original_status}' to '{new_status}'. Notes: '{notes_update}'",
                    severity="Medium", # Or allow user to set severity
                    affected_channel_id=selected_channel_id
                )
                st.success(f"Status for {channel_options[selected_channel_id]} updated to {new_status}.")
                st.rerun()
    else:
        st.write("No communication channels available to control.")

elif app_mode == "🔧 Settings":
    st.subheader("🔧 Settings")
    
    st.markdown("---")
    st.subheader("Add New Communication Channel")

    # Define available channel types and initial statuses
    available_channel_types = [
        "TETRA BTS", "TETRA Repeater", "Satellite Earth Station (Fixed)", 
        "Satellite Earth Station (Mobile)", "Starlink Gov Terminal", "LoRa Module", 
        "Military Mobile Connectivity Hub (MCC1)", "Emergency Operation Center", 
        "Airport Control Tower", "Other"
    ]
    available_statuses = ["Active", "Offline", "Standby", "Jammed", "Alert"]

    with st.form("new_channel_form", clear_on_submit=True):
        st.write("Enter details for the new communication channel:")
        new_id = st.text_input("Channel ID (unique, e.g., tetra_bts_002)", key="new_id")
        new_name = st.text_input("Channel Name (e.g., Bravo Base BTS)", key="new_name")
        new_type = st.selectbox("Channel Type:", options=available_channel_types, key="new_type")
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            new_lat = st.number_input("Latitude (e.g., 52.2297)", format="%.4f", key="new_lat")
        with col_lon:
            new_lon = st.number_input("Longitude (e.g., 21.0122)", format="%.4f", key="new_lon")
            
        new_status = st.selectbox("Initial Status:", options=available_statuses, key="new_status")
        new_notes = st.text_area("Initial Notes (optional):", key="new_notes")

        submitted = st.form_submit_button("Add Channel")

        if submitted:
            if not new_id or not new_name or new_type is None or new_lat is None or new_lon is None:
                st.error("Please fill in all required fields (ID, Name, Type, Latitude, Longitude).")
            elif any(channel['id'] == new_id for channel in st.session_state.comm_channels):
                st.error(f"Channel ID '{new_id}' already exists. Please use a unique ID.")
            else:
                new_channel_data = {
                    "id": new_id,
                    "type": new_type,
                    "name": new_name,
                    "lat": new_lat,
                    "lon": new_lon,
                    "status": new_status,
                    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "notes": new_notes
                }
                st.session_state.comm_channels.append(new_channel_data)
                log_incident(f"New channel '{new_name}' ({new_id}) added via settings.", "Low")
                st.success(f"Channel '{new_name}' added successfully!")
                # No st.rerun() needed here as form submission handles state updates and Streamlit reruns.
                # However, if we want to immediately clear form or see it in a list above, a rerun might be desired.
                # For now, success message is enough. Consider st.experimental_rerun() if needed.

    st.markdown("---")
    st.subheader("Theme and Display")
    st.write("Theme settings are managed in `.streamlit/config.toml`.")
    st.write("Further display options can be added here in the future.")
