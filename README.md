# GTFS shapes.txt Creator 

## Overview
This QGIS plugin enables advanced routing analysis for public transport systems by leveraging processed OpenStreetMap (OSM) data and GTFS (General Transit Feed Specification) datasets. It replace the ancient plugins to provide comprehensive smooth spatial analysis and routing capabilities.

## Features
- **Public Transport Routing**: Calculates optimal routes using OSM road networks and GTFS stop data.
- **Integration with OSM and GTFS**: Utilizes spatial attributes from OSM and GTFS for accurate routing.
- **Customizable Routing Parameters**: Supports various transport modes and user-defined preferences.
- **Layer Generation**: Produces layers optimized for routing and visualization in QGIS.

## Teasing
Watch the teasing for these plugin [here](https://drive.google.com/file/d/1LilcjYFtBTateYkhFQe7UMBH2HwEt9Wo/view?usp=drive_link).

## FlowRide Plugin Series
This plugin is the plugin that put together the ancient 4 plugins:
1. **GTFS Agency Selection**
2. **OSM Import Roads and Public Transport Stops** 
3. **OSM PT Routing** 
4. **GTFS Shapes Tracer** 

## Usage
0. **Prepare Data**: Use the previous plugins to import and process OSM and GTFS data.
1. **Find and move the off-road stops**: with the "Download the separate PT stops" button you can detect the stops, those need to be moved
2. **Run Routing Analysis**: Use OSM PT Routing to calculate and visualize public transport routes.
3. **Visualize Results**: Display optimized routes and layers in QGIS for further analysis.

## Video Tutorial
Watch the video tutorial for this plugin [here](https://drive.google.com/file/d/1LjzkYpu6Bfrb2KlrN3byfVHU8qHSqKoH/view?usp=sharing).

## Installation
1. Clone or download the plugin repository.
2. Place the plugin folder in your QGIS plugins directory:
   ```
   c:\Users\<your_username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
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
