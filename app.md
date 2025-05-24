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

the app will be served as a web application in a static website on github pages, do it shiuldnt have to rely on dynamic backend services

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
