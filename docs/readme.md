# Probe class documentation


- Defines a class 'probe'. Every probe instance has the following attributes;
  - Resistance estimate
  - Probe type (i.e, C1, N4, K)
    - Cutouts, Non-Cutouts, and KNT-style probes.
    - Number indicates sensor size of C and NC types.
  - Max current (based on sensor size)
  - Bridge resistor layout (based on resistance estimate and max current)

- Data can be added based upon the Vin/Vout sweep that is the first test we do to probes.
  - Can load a probe instance with previously saved bridge sweep data or collect the data based on user input
  - Can apply a fit to the data of the form y=sx + ax^3, which is appropriate for a bridge imbalance and self-heating contributions
    - Coefficients s and a can be parsed out to give information about the system.
      - S is the magnitude of the linear imbalance, and should be a measure of the resistance difference between the probe and its matching resistor
      - A is the coefficient describing self heating behaviour. It should have contributions from the probe resistance, TCR, thermal resistance of the probe and environment and perhaps others.
    - Once sx is known, it can be removed from the curve, giving a direct comparison of output regardless of bridge imbalance
  - Can convert x axis to current based upon the resistance of the side of the bridge. This gives a much more meaningful output than Vin/Vout.

- With the Vin/Vout, gain, and bridge resistors known, it is simple to calculate the resistance of the probe at any point.
  - Can give a good idea of probe room temperature resistance.
  - Should do this based on the corrected Vout of ax^3 to remove any influence from the bridge imbalance.
