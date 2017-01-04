Real world OCDS examples
========================

This folder contains real-world examples of OCDS data and scripts for fetching updated selections.

Each folder may contain:

* A ```fetch.py``` script which will get an updated set of examples
* A ```sample``` folder which contains a small number of example records

The ```fetch.py``` script should default to collecting 100 or fewer releases (unless it is downloading a bulk file with a higher number in). It should accept a command line argument ```-a``` to fetch 'all' available releases and save them in an ```all``` folder. 