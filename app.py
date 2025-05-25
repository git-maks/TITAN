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

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
           /* Main content area */
           .block-container {
                padding-top: 1rem !important; /* Reduce top padding in main content */
                padding-bottom: 2rem !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }
            /* Hide the default Streamlit app header */
            .stAppHeader {
                display: none !important;
            }
            /* Forcefully hide sidebar header elements causing spacing */
            div[data-testid="stSidebarHeader"], 
            div[data-testid="stLogoSpacer"] {
                display: none !important;
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            /* Sidebar adjustments */
            section[data-testid="stSidebar"] {
                width: 280px !important; 
                min-width: 250px !important;
                padding-top: 0.5rem !important; /* Try adding padding here and removing from h3 */
            }
            /* Adjust the main sidebar container's direct child if necessary */
            section[data-testid="stSidebar"] > div:first-child {
                 padding-top: 0rem !important;
            }

            /* Target the div containing the sidebar title more specifically */
            section[data-testid="stSidebar"] div[data-testid="stMarkdown"] h3 {
                margin-top: 0rem !important;
                padding-top: 0rem !important; /* Reduced from 0.5rem */
                margin-bottom: 0.5rem !important; 
            }
            /* Ensure the radio buttons are also snug */
            section[data-testid="stSidebar"] div[data-testid="stRadio"] {
                margin-top: 0rem !important;
                padding-top: 0rem !important;
            }
            .sidebar-status-text {
                font-family: 'Consolas', monospace !important;
                font-size: 0.8rem !important;
                line-height: 1.2 !important;
                margin-bottom: 0.2rem !important; /* Reduce space between status lines */
            }
            /* Reduce space around the horizontal rule in sidebar */
            section[data-testid="stSidebar"] hr {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
            }
    </style>
    """, unsafe_allow_html=True)

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
            update_channel_status("tetra_bts_001", "Alert", f"Suspected widespread jamming campaign. {now_str}.")
            log_incident("Warsaw Central BTS (tetra_bts_001) experiencing jamming.", "Critical", "tetra_bts_001")

    if step == 6 and "lora_water_001" in channel_ids:
        if any(c["id"] == "lora_water_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            bts_alert = any(c["id"] == "tetra_bts_001" and c["status"] == "Alert" for c in st.session_state.comm_channels)
            if bts_alert:
                update_channel_status("lora_water_001", "Alert", f"Detected TETRA network anomalies. {now_str}.")
                log_incident("Vistula Water Plant Sensor (lora_water_001) detected TETRA anomalies.", "Medium", "lora_water_001")
    
    if step == 7 and "lora_hospital_001" in channel_ids:
        if any(c["id"] == "lora_hospital_001" and c["status"] == "Active" for c in st.session_state.comm_channels):
            repeater_offline = any(c["id"] == "tetra_rep_001" and c["status"] == "Offline" for c in st.session_state.comm_channels)
            if repeater_offline:
                update_channel_status("lora_hospital_001", "Alert", f"Primary repeater (tetra_rep_001) offline. {now_str}.")
                log_incident("Gdansk Hospital Comms Monitor (lora_hospital_001) reports primary repeater offline.", "High", "lora_hospital_001")

    if step == 8 and "mcc1_001" in channel_ids:
        bts_alert = any(c["id"] == "tetra_bts_001" and c["status"] == "Alert" for c in st.session_state.comm_channels)
        if bts_alert and any(c["id"] == "mcc1_001" for c in st.session_state.comm_channels):
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
        bts_alert = any(c["id"] == "tetra_bts_001" and c["status"] == "Alert" for c in st.session_state.comm_channels)
        repeater_offline = any(c["id"] == "tetra_rep_001" and c["status"] == "Offline" for c in st.session_state.comm_channels)
        if bts_alert and repeater_offline and any(c["id"] == "mcc1_002" for c in st.session_state.comm_channels):
            update_channel_status("mcc1_002", "Active", f"Deployed for wide area backup due to multiple outages. {now_str}.")
            log_incident("MCC1 Unit Bravo (mcc1_002) activated for wide area backup.", "Medium", "mcc1_002")
    
    # Random event: A random LoRa module might go offline temporarily
    if step > 5 and random.random() < 0.1: # 10% chance each step after step 5
        lora_channels = [c for c in st.session_state.comm_channels if c["type"] == "LoRa Module" and c["status"] == "Active"]
        if lora_channels:
            chosen_lora = random.choice(lora_channels)
            update_channel_status(chosen_lora["id"], "Offline", f"Temporary sensor glitch. {now_str}.")
            log_incident(f"LoRa Module {chosen_lora['name']} ({chosen_lora['id']}) went temporarily offline.", "Low", chosen_lora["id"])

    # Random event: A Starlink terminal might experience brief intermittent connectivity
    if step > 8 and random.random() < 0.05: # 5% chance
        starlink_terminals = [c for c in st.session_state.comm_channels if c["type"] == "Starlink Gov Terminal" and c["status"] == "Active"]
        if starlink_terminals:
            chosen_starlink = random.choice(starlink_terminals)
            original_notes = chosen_starlink.get("notes", "")
            update_channel_status(chosen_starlink["id"], "Alert", f"Brief intermittent connectivity reported. {now_str}. Original: {original_notes}")
            log_incident(f"Starlink Terminal {chosen_starlink['name']} ({chosen_starlink['id']}) experiencing intermittent connectivity.", "Medium", chosen_starlink["id"])
            # It could return to "Active" in a subsequent step.

# Sidebar Navigation & Title
st.sidebar.markdown("### Space25 Communications Dashboard") # New Title Location & Size
# st.sidebar.title("Navigation") # Original line, title for radio is now part of radio
app_mode = st.sidebar.radio(
    "", # Removed "Go to" label
    ["🗺️ Map Overview", "📊 Incident Reports", "⚙️ Manual Control", "🔧 Settings"],
    label_visibility="collapsed" # Hide the label space entirely
)

# Add status information at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"<p class='sidebar-status-text'><strong>System Status:</strong> <span style='color:green;'>Online</span></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p class='sidebar-status-text'><strong>Last Update:</strong> {st.session_state.last_refresh_time}</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p class='sidebar-status-text'><strong>Signal Strength:</strong> <span style='color:lightgreen;'>Strong</span></p>", unsafe_allow_html=True)

# Refresh button - moved to main area, will be added to each page or a common spot
if app_mode == "🗺️ Map Overview":
    if st.button("🔄 Refresh Network Status"):
        run_simulation_step()
        st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
    # st.subheader("🗺️ Map Overview") # REMOVED
    if st.session_state.comm_channels:
        df_channels = pd.DataFrame(st.session_state.comm_channels)
        
        # Simplified status colors - using hex codes for explicitness
        status_colors = {
            "Active": "#008000",    # green
            "Offline": "#A9A9A9", # darkgrey
            "Alert": "#FF0000",       # red
            "Jammed": "#FF0000",      # Treat as Alert (maps to red)
            "Standby": "#0000FF"     # blue (simplify_status maps this to Active, so it will use green)
        }
        
        # Map any status not in our simplified list to one of our simplified statuses
        def simplify_status(status):
            if status == "Jammed":
                return "Alert"
            elif status == "Standby":
                return "Active"  # Treat Standby as Active
            else:
                return status

        # Apply the simplification to the dataframe
        df_channels['simplified_status'] = df_channels['status'].apply(simplify_status)

        # Define symbols using basic ASCII characters guaranteed to work everywhere
        symbol_map = {
            "TETRA BTS": "T",            # T for TETRA BTS
            "TETRA Repeater": "R",       # R for Repeater
            "Satellite Earth Station (Fixed)": "S", # S for Satellite
            "Starlink Gov Terminal": "L", # L for Starlink
            "LoRa Module": "M",          # M for Module
            "Military Mobile Connectivity Hub (MCC1)": "H", # H for Hub
            "Airport Control Tower": "A", # A for Airport
            "Emergency Operation Center": "E", # E for Emergency
            "Other": "O"                 # O for Other
        }  
        
        # Debug - print unique types to verify mapping
        print("Unique types in data:", df_channels['type'].str.strip().unique())
        print("Keys in symbol_map:", list(symbol_map.keys()))
        
        size_map = { # Controls the size of the marker
            "TETRA BTS": 22,                      # Bigger for BTS
            "Satellite Earth Station (Fixed)": 22, # Bigger for sat stations
            "Military Mobile Connectivity Hub (MCC1)": 20,
            "Emergency Operation Center": 20,
            "Airport Control Tower": 20,
            "Starlink Gov Terminal": 18,          # Medium for Starlink
            "TETRA Repeater": 18,                 # Medium for repeater
            "LoRa Module": 16,                    # Smaller for LoRa sensors
            "Other": 16
        }
        
        fig = go.Figure()

        # Hybrid approach: add both markers and text for better visibility
        for channel_type, group_by_type in df_channels.groupby('type'):
            channel_type = channel_type.strip()  # Ensure stripped for lookup
            symbol_for_type = symbol_map.get(channel_type, '+')  # Get ASCII symbol
            size_for_type = size_map.get(channel_type, 14)  # Get size
            
            for status, group_by_status_and_type in group_by_type.groupby('simplified_status'):
                color_for_status = status_colors.get(status, '#888888')  # Get color from status

                lats = group_by_status_and_type['lat'].tolist()
                lons = group_by_status_and_type['lon'].tolist()
                hover_names = group_by_status_and_type['name'].tolist()
                symbols = [symbol_for_type] * len(group_by_status_and_type)  # ASCII letters
                
                custom_data_list = []
                for _idx, row in group_by_status_and_type.iterrows():
                    custom_data_list.append([
                        row['type'], 
                        row['simplified_status'], 
                        row['last_updated'], 
                        row['notes']
                    ])                
                
                # First, add a marker for the background shape
                fig.add_trace(go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode='markers',
                    marker=dict(
                        size=size_for_type + 6,  # Make background larger for better visibility
                        color=color_for_status,  # Color by status
                        opacity=0.9,
                    ),
                    hoverinfo='none',
                    showlegend=False
                ))
                
                # Then add text on top for the symbols
                fig.add_trace(go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode='text',  # Using text mode for symbols
                    text=symbols,  # ASCII letters
                    textfont=dict(
                        size=size_for_type,  # Make text larger
                        color='white',  # White text for contrast
                        family="Arial Black, sans-serif",  # Bold font for better visibility
                        weight=900,  # Maximum boldness
                    ),
                    hovertext=hover_names,
                    customdata=custom_data_list,
                    hovertemplate=(
                        "<b>%{hovertext}</b><br><br>" +
                        "Type: %{customdata[0]}<br>" +
                        "Status: %{customdata[1]}<br>" +
                        "Last Updated: %{customdata[2]}<br>" +
                        "Notes: %{customdata[3]}" +
                        "<extra></extra>"
                    ),
                    name=f"{channel_type} - {status}",
                    showlegend=False
                ))

        # Add legend items for infrastructure types
        legend_items_symbols = {}
        for channel_type in df_channels['type'].str.strip().unique():
            if channel_type not in legend_items_symbols:
                symbol_for_legend = symbol_map.get(channel_type, '+')
                
                # Background marker for legend item
                fig.add_trace(go.Scattermapbox(
                    lat=[None], lon=[None],
                    mode='markers',
                    marker=dict(
                        size=20,  # Make the marker larger
                        color='#333333',  # Dark color for legend
                        opacity=0.9,
                    ),
                    name=f"{channel_type} ({symbol_for_legend})",  # Include symbol in name for clarity
                    legendgroup="Symbols",
                    legendgrouptitle_text="Infrastructure Type",
                ))
                
                # Symbol text for legend item
                fig.add_trace(go.Scattermapbox(
                    lat=[None], lon=[None], 
                    mode='text',
                    text=[symbol_for_legend],
                    textfont=dict(
                        size=10,
                        color='white',
                        family="Arial Black, sans-serif",
                        weight=700,
                    ),
                    name=f"{channel_type}",
                    legendgroup="Symbols",
                    legendgrouptitle_text="Infrastructure Type",
                    showlegend=False  # Don't show duplicate entry
                ))
                legend_items_symbols[channel_type] = True
                
        # Add legend items for simplified status colors
        legend_items_status = {}
        simplified_statuses = ["Active", "Offline", "Alert"]
        for status_val in simplified_statuses:
            color_val = status_colors.get(status_val, '#888888')
            if status_val not in legend_items_status:
                fig.add_trace(go.Scattermapbox(
                    lat=[None], lon=[None], 
                    mode='markers',  # Use markers for status
                    marker=dict(
                        size=10,
                        color=color_val,
                        opacity=0.9,
                    ),
                    name=status_val,
                    legendgroup="Statuses",
                    legendgrouptitle_text="Status"
                ))
                legend_items_status[status_val] = True
        
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox_center_lat=52.0, 
            mapbox_center_lon=19.0,
            mapbox_zoom=5.5, 
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)", 
                font=dict(color="black"),
                traceorder="grouped", # Group legend items by legendgroup
                # title_text="Legend" # Optional main legend title
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("All Communication Channels")
        st.dataframe(df_channels[['id', 'name', 'type', 'status', 'last_updated', 'lat', 'lon', 'notes']], use_container_width=True)
    else:
        st.write("No communication channels to display.")

elif app_mode == "📊 Incident Reports":
    if st.button("🔄 Refresh Network Status"):
        run_simulation_step()
        st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
    st.subheader("📊 Incident Reports")
    if st.session_state.incidents:
        df_incidents = pd.DataFrame(st.session_state.incidents)
        # Reorder columns for better readability
        df_incidents_display = df_incidents[["timestamp", "description", "severity", "affected_channel_id"]]
        st.dataframe(df_incidents_display, use_container_width=True)
    else:
        st.write("No incidents reported yet.")
elif app_mode == "⚙️ Manual Control":
    if st.button("🔄 Refresh Network Status"):
        run_simulation_step()
        st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
    st.subheader("⚙️ Manual Control")
    if st.session_state.comm_channels:
        channel_options = {channel["id"]: f"{channel['name']} ({channel['id']})" for channel in st.session_state.comm_channels}
        selected_channel_id = st.selectbox("Select Channel to Update:", options=list(channel_options.keys()), format_func=lambda x: channel_options[x])

        if selected_channel_id:
            current_channel = next((ch for ch in st.session_state.comm_channels if ch["id"] == selected_channel_id), None)
            
            # Simplify the current status for display
            current_display_status = current_channel['status']
            if current_display_status == "Jammed":
                current_display_status = "Alert"
            elif current_display_status == "Standby":
                current_display_status = "Active"
                
            st.write(f"Current status: {current_display_status}")

            # Simplified status options
            status_options = ["Active", "Offline", "Alert"]
            
            # Map the current status to one of our simplified statuses for the selectbox default
            if current_channel['status'] in ["Active", "Standby"]:
                current_status_index = status_options.index("Active")
            elif current_channel['status'] == "Offline":
                current_status_index = status_options.index("Offline")
            else:  # "Alert", "Jammed", etc.
                current_status_index = status_options.index("Alert")

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
    if st.button("🔄 Refresh Network Status"): # Adding refresh to settings page as well for consistency
        run_simulation_step()
        st.session_state.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
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
    
    # Simplified status options
    available_statuses = ["Active", "Offline", "Alert"]

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
