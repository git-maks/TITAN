App serves as a dashboard for viewing active communication channnels like: 
- TETRA BTSs
- TETRA Repeaters
- Satelite Earth Stations (Fixed and Mobile)
- Starlink Gov Terminals
- LoRa Modules located on scritical infrastructure like 
  - Water Treatment Plants
  - Power Stations
  - Hospitals
  - Police Stations
  - Fire Stations
  - Post offices
- Military Mobile Connectivity Hubs (MCC1)
- Emergency Operation Centers
- Airport Control Towers

it should provide a map view, 


Important note:
in the app should be placed dummy, simulated information showing in the real time as some tetra bts's and repeteras get jammed, LoRa's detect it, and Military Mobile Connectivity Hubs (MCC1) take their place, and so on. 
the map should be interactive, allowing users to click on each communication channel to get more details, such as:
- Status (Active, Jammed, Offline)
- Last Updated
- Location coordinates
- Type of communication channel
- Additional notes or alerts

the app will be served as a web application 

on the left bar of the app we should place sections where we will be able to go through:
- map overview
- incident reports
- manual control (for manual communication channel rerouting)
- settings (for configuring the app, adding new communication channels, etc.)

there should also be a navbar that shows app status (online/offline) and a button to refresh the data and signal strengh.

as for the app design:
- use a clean, desktop first design
- the app should be in dark mode by defult
- use a modern, minimalist aesthetic with a focus on usability
- colors should be military oriented with good but pleasent contrast
- use icons and symbols that are easily recognizable and intuitive
- dont use emojis or overly decorative elements, use icons from libraries like FontAwesome or Material Icons instead
- ensure the app is responsive and works well on different screen sizes

the entire app will be made in streamlit and served through streamlit community cloud

## App Workflow:
**Phase 1: Foundation & Basic Setup**

1.  **Project Initialization:**
    *   Create your project folder (e.g., `space25_dashboard`).
    *   Set up a Python virtual environment (`.venv`).
    *   Activate the virtual environment.
2.  **Install Core Dependencies:**
    *   `pip install streamlit pandas plotly` (or `streamlit-folium` if you prefer Folium for maps).
3.  **Create `app.py`:**
    *   Add basic imports (`streamlit as st`, `pandas as pd`, etc.).
    *   Implement `st.set_page_config()` with title, icon, layout, and initial sidebar state.
4.  **Create `.streamlit/config.toml`:**
    *   Define your initial dark theme with military-oriented colors (e.g., `primaryColor`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`).
5.  **Initialize `requirements.txt`:**
    *   Run `pip freeze > requirements.txt`.
6.  **Basic App Layout:**
    *   Sketch out the main areas in `app.py`: title, placeholder for the "navbar" (top columns), sidebar navigation (`st.sidebar.radio`), and a conditional structure for displaying different pages.

**Phase 2: Data Structures & Initial Simulation Logic**

1.  **Define Data Structures in `st.session_state`:**
    *   In `app.py`, initialize `st.session_state.comm_channels` with a small, diverse set of dummy communication channel data (include all fields: id, type, name, lat, lon, status, last_updated, notes).
    *   Initialize `st.session_state.incidents` as an empty list.
    *   Initialize `st.session_state.simulation_time_step = 0`.
2.  **Implement Basic Simulation Functions:**
    *   Create `update_channel_status(channel_id, new_status, notes_update="")`.
    *   Create `log_incident(description, severity="Medium")`.
    *   Create an initial `run_simulation_step()` function that increments `simulation_time_step` and makes one or two simple changes (e.g., change one channel's status after a few steps).
3.  **"Navbar" Functionality:**
    *   Implement the "Refresh Data & Run Sim Step" button in the top columns to call `run_simulation_step()` and `st.rerun()`.
    *   Add the static "App Status" metric.

**Phase 3: Implementing UI Sections - Map & Core Views**

1.  **Map Overview Page:**
    *   If `app_mode == "🗺️ Map Overview"`:
        *   Use `st.subheader()` for the title.
        *   Implement the map using Plotly Express (`px.scatter_mapbox`):
            *   Load data from `st.session_state.comm_channels` into a Pandas DataFrame.
            *   Configure `lat`, `lon`, `color` (by status), `hover_name`, `hover_data`.
            *   Set `mapbox_style="carto-darkmatter"`.
            *   Display using `st.plotly_chart()`.
        *   Display `st.session_state.comm_channels` in a `st.dataframe()` below the map.
2.  **Incident Reports Page:**
    *   If `app_mode == "📊 Incident Reports"`:
        *   Use `st.subheader()` for the title.
        *   Display `st.session_state.incidents` in a `st.dataframe()`, formatting timestamps.

**Phase 4: Implementing UI Sections - Control & Settings**

1.  **Manual Control Page:**
    *   If `app_mode == "⚙️ Manual Control"`:
        *   Use `st.subheader()` for the title.
        *   Use `st.selectbox` to choose a channel.
        *   Use another `st.selectbox` to choose a new status.
        *   Use `st.text_input` for notes.
        *   Use `st.button` to apply changes, calling `update_channel_status()` and `log_incident()`, then `st.rerun()`.
2.  **Settings Page:**
    *   If `app_mode == "🔧 Settings"`:
        *   Use `st.subheader()` for the title.
        *   Implement the "Add New Communication Channel" form using `st.form`.
        *   On submission, append the new (simulated) channel to `st.session_state.comm_channels`.
        *   Add placeholders for theme/display information.

**Phase 5: Enhancing Simulation & Visuals**

1.  **Expand Simulation Logic in `run_simulation_step()`:**
    *   Implement more complex scenarios:
        *   TETRA BTS/Repeaters getting jammed.
        *   LoRa modules detecting these events (update their notes/status).
        *   MCC1 units becoming active to take over.
        *   Vary the timing and conditions for these events.
2.  **Refine Map Visuals:**
    *   Ensure map markers clearly reflect status (colors).
    *   Customize popups/hover tooltips for clarity.
    *   Consider using different symbols for different channel types if Plotly/Folium allows easily.
3.  **Icons & Styling:**
    *   Review app.md for icon requirements. Use emojis where simple. For FontAwesome/Material Icons, you might need to use `st.markdown(..., unsafe_allow_html=True)` and include CDN links. This is more advanced. Start with emojis.
    *   Fine-tune colors in `config.toml` for the desired military aesthetic and contrast.
    *   Ensure the layout is clean and desktop-first. Streamlit is inherently responsive, but test on different browser widths.

**Phase 6: Testing & Iteration**

1.  **Thorough Testing:**
    *   Test all navigation paths.
    *   Verify all interactive elements (buttons, forms, selections).
    *   Run the simulation through many steps to ensure it behaves as expected.
    *   Check data display on the map and in tables.
    *   Check incident logging.
2.  **Refine and Debug:**
    *   Fix any bugs or unexpected behavior.
    *   Improve UI/UX based on testing.
    *   Ensure all requirements from app.md are met.

**Phase 7: Deployment**

1.  **Prepare for Deployment:**
    *   Ensure `requirements.txt` is accurate and up-to-date.
    *   Commit all your code (`app.py`, `.streamlit/config.toml`, `requirements.txt`) to a GitHub repository.
2.  **Deploy to Streamlit Community Cloud:**
    *   Go to [share.streamlit.io](https://share.streamlit.io).
    *   Connect your GitHub account.
    *   Choose your repository and the main app file (`app.py`).
    *   Deploy.

