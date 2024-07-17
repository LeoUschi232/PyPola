# PyPola

## Overview

PyPola is a multi-purpose Python project in the topic of light polarization.
The primary purpose of PyPola is to verify the Mueller matrix and Stokes vector formalism for polarization optics.
Polarization states are implemented as Stokes vectors and the transformations performed by optical elements are
implemented as Mueller matrices.
PyPola features simulations of simple optical components such as waveplates and linear polarizers as well as more
complex devices such as polarization controllers and analyzers.
The secondary purpose is to analyze data from polarization state measurements with regards their implications for
polarization-coded quantum key distribution systems.

### Development Background

This project was developed during my work at the german aerospace center institute of communications and navigation.
During that time I was involved with the mathematical framework used for polarization optics but wanted to verify its
legitimacy.
Writing this simulation was not part of my official duties at the DLR.
I developed this project mainly to supplement my confidence that the calculations I performed were correct.
Additionally, the analysis scripts in this project demonstrate the methods I used to process, compute, analyze and plot
the obtained data for my bachelor thesis.
Including all relevant Python scripts into the appendix of the thesis would have been impractical as it would have
extended the page count of the thesis beyond tolerable bounds.
The data itself is not provided as it is the DLR's intellectual property.

## Verification

### Optical Elements

- Linear Polarizer
- Retardation Waveplate
- Magneto-optic Rotator
- Polarization Beam Splitter

### Devices Operational Principles

- Delta-waveplate Polarization Controller
    - For example: EOSpace Lithium Niobate Polarization Controller
- QWP-HWP-QWP Polarization Controller
    - For example: Thorlabs Mickey Mouse Ears Polarization Controller
- 4-Variabale-Retardation-Waveplates Polarization Controller
    - For example: General Photonics' PolaRite II/III Polarization Controller
- Rotating Quarterwaveplate Polarimeter
    - For example: Thorlabs PAX1000 series Polarimeter
- 4-Detector Photopolarimeter
    - For example: General Photonics' PolaFlex Polarization Synthesizer and Analyzer
