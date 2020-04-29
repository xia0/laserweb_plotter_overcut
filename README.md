# Laserweb overcut script for cutters

There's no way to define an overcut on Laserweb for vinyl cutting so here's a simple script to modify the GCode output.

## Screenshot
![Screenshot of overcut generator](https://github.com/xia0/laserweb_plotter_overcut/raw/master/screenshot.PNG)

## Usage
python overcut.py [input file] [float overcut distance] [output file]

e.g. `python overcut.py input.gcode 1.5 output.gcode`
