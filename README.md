# GTFS shapes.txt Creator 

## Overview
This QGIS plugin generates GTFS `shapes.txt` files by routing transit lines on OpenStreetMap (OSM) road and rail networks. It integrates public transport data from opentransportdata.swiss with OSM geographic data to automatically trace transit routes and create standardized GTFS shape files for various transport modes (buses, trams, regional trains, and funiculars).

## Features
- **Multi-Transport Support**: Handles buses, trams, regional trains, and funiculars with mode-specific routing
- **GTFS Integration**: Processes transit data from opentransportdata.swiss GTFS feeds
- **OSM Network Routing**: Automatically downloads and uses OpenStreetMap road and rail networks for routing
- **Stop Validation**: Detects and manages off-road public transport stops with interactive positioning tools
- **Automatic Shape Generation**: Creates GTFS-compliant `shapes.txt` files from routed transit lines
- **Multi-Layer Support**: Generates organized QGIS layers for roads, rails, and individual trip routes

## Plugin Architecture
This plugin consolidates the functionality of 4 legacy plugins:
1. **GTFS Agency Selection** - Manages transit agencies from GTFS feeds
2. **OSM Import Roads and Public Transport Stops** - Downloads and imports OSM network data
3. **OSM PT Routing** - Performs route-finding on networks
4. **GTFS Shapes Tracer** - Converts routes to GTFS shapes format
## Video Tutorial (not up to date yet)
Watch the video tutorial for those plugin [here](https://drive.google.com/file/d/1LjzkYpu6Bfrb2KlrN3byfVHU8qHSqKoH/view?usp=sharing).


## Workflow
1. **Select GTFS Folder**: Point to your GTFS dataset directory
2. **Update Agencies**: Load available transit agencies from the GTFS feed
3. **Select Transit Routes**: Choose specific routes by transport mode
4. **Download OSM Data**: Import road/rail networks for the selected routes
5. **Validate Stops**: Identify and reposition stops that don't align with roads
6. **Create Trips**: Generate routing trips on the OSM network
7. **Display Routes**: Visualize routed trips in QGIS
8. **Generate Shapes**: Create final GTFS `shapes.txt` file



## Installation
1. Clone or download the plugin repository.
2. Place the plugin folder in your QGIS plugins directory:
   for Windows
   ```
   c:\Users\<your_username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
   ```
   for linux
   ```
   /home/user_name/.local/share/QGIS/QGIS3/profiles/default/python/plugins
   ```
3. Restart QGIS and enable the plugin from the Plugin Manager.

## Dependencies
- QGIS 3.x
- Python libraries: `pandas`, `numpy`, `statistics`
- QGIS Processing Toolbox
- QuickOSM

## License
This plugin is distributed under the GNU General Public License v2.0 or later.

## Author
Luigi Dal Bosco  
Email: luigi.dalbosco@gmail.com  
Generated using [QGIS Plugin Builder](http://g-sherman.github.io/Qgis-Plugin-Builder/).
