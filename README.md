# Carto YSWS

The website for the Carto YSWS program, displayed as a tiled web map with [Maptalks](https://maptalks.org/)

## Setup

The main site SVG (see sources below) is composed of 16 pages of size 4096x4096 pixels. Export each page separately as a PNG image to `inkscape_files/export/`, then run `python3 generate_tiles.py` to generate the map tiles in `tiles/`. Serve the project root directory with any static web server.

## Sources

The graphical content for the website is sourced from the following locations:

- [Main site SVG](https://github.com/CyrilSLi/carto_ysws/blob/main/inkscape_tiles/test.svg)
- [Button link images](https://github.com/CyrilSLi/carto_ysws/tree/main/images)
- [Figma design](https://www.figma.com/design/Flm54rw9RGuazMRmAPkCX6/Carto-YSWS-Site-Contents)