# PyPola

## Overview

PyPola is a custom simulation of lightwave propagation through optical instruments written in Python.
At its core, PyPola uses the Stokes vector representation to describe lightwaves and applies instrument-specific Stokes
matrices to simulate the effect of various optical polarization instruments on the lightwave.
This approach allows for the simulation of light passing through an arbitrary sequence of instruments, enabling the
analysis of complex optical systems and their impact on light polarization.

## Features

- __Simulation of Lightwave Propagation:__ Model the behavior of light as it interacts with different optical
  polarization instruments.
- __Stokes Vector and Matrix Operations:__ Utilize the mathematical foundation of Stokes vectors and matrices to
  describe light and its interaction with instruments.
- __Support for Multiple Instruments:__ Includes models for a Linear Polarizer, Retarders (such as Quarter-wave and
  Half-wave plates), and Rotators (e.g., Magneto-Optic Rotator).
- __Sequence Simulation:__ Concatenate multiple instruments into lengthy sequences to analyze the cumulative effect on
  light polarization.
- __Design and Analysis Tool:__ Serve as a valuable tool for testing the validity of mathematical models and device
  designs in the field of light and polarization analysis.

