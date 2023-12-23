# MQTT topic structure

## Main display
The Button+ main display can have several display items, listening to MQTT topics for its configuration. Currently, Button+ only listens to the value topic.

Attribute | Topic | Eventtype | Future
 --- | --- | --- | ---
 Value | `buttonplus/<deviceID>/main/<sequence number>/value`  | 15 |
 Label above the value | `buttonplus/<deviceID>/main/<sequence number>/label`  | 16 | x
 Unit of measurement | `buttonplus/<deviceID>/main/<sequence number>/uom` |  17 | x
