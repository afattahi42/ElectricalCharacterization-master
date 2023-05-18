<h1>Electrical Characterization Setup Code for Breznay Lab</h1>


Used for the following projects:
<ol>
  <li>Thin Film Growth and Characterization of DyTe2 (Kaveh Pezeshki Thesis)</li>
  <li>Characterization of thin-film gold (Emma Lickey misc.)</li>
  <li>Characterization of graphene field effect transistors (Emma Lickey Thesis)</li>
</ol>


The manual for making use of this repository can be found at the link below:
https://docs.google.com/document/d/1XUEJyOQIHJrHLE_vnaivs8qQtfJ8ZIHhpnAM22L-ZRY/edit?usp=sharing

Contact [first letter of my first name + my last name][at symbol] hmc.edu for access.


This repository contains the supplementary information discussed in the Kaveh's thesis text. This includes:

<ol>
  <li>Scripts for automated temperature control and measurement</li>
  <li>Scripts for data processing and fitting</li>
  <li>CAD for the design of the vacuum transport stage</li>
  <li>CAD for the design of the four-point vacuum stage</li>
  <li>Design files for custom PCBs</li>
</ol>


<h3>Automated temperature control and measurement </h3>

Scripts interface with measurement instruments over GPIB, GPIB via USB, and RS-232. Users must therefore have functional pyserial and pyvisa installations. Similarly, users must have functioning NI-VISA libraries, which can be downloaded from the National Instruments [website](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#442805).

The raw scripts used for data logging in this work are given in `sortedelectricaldata/datalogging`. In general, the scripts expect the following equipment:

1) Keithley 2110 connected to the K-type thermocouple, connected to the host computer over USB
2) Keithley 2000 connected to the thermistor, connected to the host computer over RS-232
3) Siglent SPD3303X connected to the Peltier element, conencted to the host computer over USB
4) Arduino relay control box, connected to the computer over USB. This lies between the Peltier element and SIglent SPD3303X
5) SRS SR830, connected to the computer over RS-232, and wired as described in the thesis text depending on application
6) BK Precision BK5491, connected to the computer over USB
