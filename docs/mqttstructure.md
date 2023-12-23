# MQTT topic structure

## Main display
The Button+ main display can have several display items, listening to MQTT topics for its configuration. Currently, Button+ only listens to the value topic. Each of these attributes have individual MQTT broker setting.

Attribute | Topic | Eventtype | Future | Home Assistant
 --- | --- | --- | --- | ---
 Value | `buttonplus/<deviceID>/main/<sequence number>/value`  | 15 | | sensor
 Label above the value | `buttonplus/<deviceID>/main/<sequence number>/label`  | 16 | x | sensor attribute
 Unit of measurement | `buttonplus/<deviceID>/main/<sequence number>/uom` |  17 | x | sensor attribute

Each display item has additional attributes which can be set in the Button+ software.

Attribute | Description | Home Assistant 
--- | --- | ---
x | Horizontal postion of the item within the lcd (in % of the display width) | sensor attribute
y | Vertical postion of the item within the lcd (in % of the display width)| sensor attribute
fontsize | Smallest size is 1, largest size is 4| sensor attribute
width | Width of the item in % of display width| sensor attribute
round | Round the incoming payload to decimal places, 0 is round to whole numbers| sensor attribute
Alignment | numeric: | sensor attribute
0            | Top Left
1            | Top Center
2            | Top Right
3            | Center Left
4            | Center Center
5            | Center Right
6            | Bottom Left
7            | Bottom Center
8            | Bottom Right    

## Buttons
Each button has a button, a display a front LED and a wall LED. The device will publish topics (P) and subscribe to topics (S).
Attribute | Topic | P/S | value | Home Assistant
--- | --- | --- | --- | ---
click | `buttonplus/<deviceID>/bars/<buttonID>/click` | P | true/false | binary_sensor
longclick | `buttonplus/<deviceID>/bars/<buttonID>/longclick` | P | true/false | attribute
label | `buttonplus/<deviceID>/bars/<buttonID>/label` | S | text | attribute
toplabel | `buttonplus/<deviceID>/bars/<buttonID>/toplabel` | S | text | attribute
unit | `buttonplus/<deviceID>/bars/<buttonID>/uom` | S | text | attribute
label | `buttonplus/<deviceID>/bars/<buttonID>/label` | S | text | attribute
led_front | `buttonplus/<deviceID>/bars/<buttonID>/led_front` | S | true/false | attribute
ledcolorfront | `buttonplus/<deviceID>/bars/<buttonID>/ledcolorfront` | S | decimal color (for instance 15140872) | attribute
led_wall | `buttonplus/<deviceID>/bars/<buttonID>/led_wall` | S | true/false | attribute
ledcolorwall | `buttonplus/<deviceID>/bars/<buttonID>/ledcolorwall` | S | decimal color (for instance 15140872) | attribute

## General
General topics for the Button+ are the following:

Attribute | Topic | P/S | value | Home Assistant
--- | --- | --- | --- | ---
name | | | 
location |||
temperature | `buttonplus/<deviceID>/sensors/temperature` | P | number | sensor
