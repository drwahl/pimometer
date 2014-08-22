pi-mometer
==========

Raspberry Pi Thermometer project meant for displaying thermometer data collected by an RPi during a bbq/smoker

Data Layout and Input Mapping
=============================
Using the supplied command line options and configuration file, here is the mapping:

[config file]

database = pi_mometer - Name of the database in mongodb

collection = pi_collection - Name of the collection in mongodb

[CLI options]

-e, --event = "Pulled Pork" - The name of the event. This will create new documents for each unique event.

-s1, --sensor1 = "105" - The tempurature of sensor #1. This is a key whose value is a list of dicts. The dicts have keys of the current time and values of the provided tempurature.

-s2, --sensor2 =  "107" - The tempurature of sensor #2. This data is formatted the same as for sensor #1.

Note: the timestamp is determined by system time and can not (yet) be arbitrarly passed in.

```
pi_mometer_db (database)
+-------------------------------------------+
| pi_mometer_collection (collection)        |
| +--------------------------------------+  |
| |  Pulled Pork (document)              |  |
| |  +-------------------------------+   |  |
| |  |- Sensor 1:                    |   |  |
| |  |  [{'07-04-2014-1300': '155'}, |   |  |
| |  |   {'07-04-2014-1301': '154'}, |   |  |
| |  |   {'07-04-2014-1302': '157'}] |   |  |
| |  |- Sensor 2:                    |   |  |
| |  |  [{'07-04-2014-1300': '149'}, |   |  |
| |  |   {'07-04-2014-1301': '149'}, |   |  |
| |  |   {'07-04-2014-1302': '150'}] |   |  |
| |  +-------------------------------+   |  |
| |                                      |  |
| |  Smoked Salmon (document)            |  |
| |  +-------------------------------+   |  |
| |  |- Sensor 1:                    |   |  |
| |  |  [{'12-01-2014-1635': '140'}, |   |  |
| |  |   {'12-01-2014-1636': '142'}, |   |  |
| |  |   {'12-01-2014-1637': '141'}] |   |  |
| |  |- Sensor 2:                    |   |  |
| |  |  [{'12-01-2014-1635': '139'}, |   |  |
| |  |   {'12-01-2014-1636': '139'}, |   |  |
| |  |   {'12-01-2014-1637': '142'}] |   |  |
| |  +-------------------------------+   |  |
| +--------------------------------------+  |
+-------------------------------------------+
```
