# inSite User Documentation

This is a starting point for user docs for inSite, including some integration notes for use with 3rd party sites/systems.

## Features

Quick list of features here, which can be expanded into full docs later

* basic nav instructions
* double-click to zoom
* keyboard shortcuts
* selecting/editing/deleting annotations
* project marker pins, fade out as you get close
* camera orbit mode


## Loading Data

* edit DATA/dataconfig/default.js
* data structure under DATA can be arbitrary, but best to stick to the convention of DATA/[client]/[project] and to then have model/pano/video sub-folders under there
* linked photos are optional, if used the convention is to have model/cameras.xml, model/photos/ and model/photos/thumbs
* cameras.xml is a BlocksExchange XML file exported from CC in WGS84 including yaw/pan/roll values. You will need to edit this file to search/replace the image paths from where they existed on disk in your CC project, to where they will exist on the server (i.e. DATA/...). If the paths aren't correct it isn't a drama, you will get missing file errors in the log when you try to view them, easy to fix afterwards



## Integration

In order for inSite to work on a 3rd party server/system, here are some things which will need to be configured

* edit INSITE/globalconfig/pre_load.js and post_load.js if needed




