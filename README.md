# Living-Lab-concept
Multiple sensor data acquisition project

This project is a 4 tier architecture that is rigged up in a lab environment to monitor various parameters.

Tier 1 - MSP430 as Data acquisition system where most of the sensors are connected

Tier 2 - Raspberry Pi hosts a light server and pushes the data from Tier 1 to Tier 3

Tier 3 - Client's main server that pulls data from Tier 2

Tier 4 - Rapsberry Pi actuates a few solenoids based on the commands pulled from Tier 3

The list of sensors used:

GPS

Loadcell

Motion sensor

switches

and a few others

Testing the branch functionality in git.
Making the branch stay and commit only to the branch and not the master.