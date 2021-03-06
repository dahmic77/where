"""Calculate total zenith delay

Description:
------------

This model determines the total zenith delay following Mendes and Pavlis [1].

References:
-----------

[1] Mendes, V.B. and E.C. Pavlis, 2004,
    "High-accuracy zenith delay prediction at optical wavelengths,"
    Geophysical Res. Lett., 31, L14602, doi:10.1029/2004GL020308, 2004

[2] Petit, G. and Luzum, B. (eds.), IERS Conventions (2010),
    IERS Technical Note No. 36, BKG (2010)



"""
# External library imports
import numpy as np

# Midgard imports
from midgard.dev import plugins
from midgard.math.unit import Unit

# Where imports
from where.ext import iers_2010 as iers


@plugins.register
def pavlis_mendes(dset):
    """Calculate zenith delay for all observations

    Args:
        dset:     Dataset containing the data

    Returns:
        Numpy array:  Correction in meters for each observation
    """
    output = np.zeros(dset.num_obs)

    # Compute WVP = Water Vapour Pressure from temperature and humidity:
    #   https://en.wikipedia.org/wiki/Vapour_pressure_of_water
    lat, _, height = dset.site_pos.llh.T
    pressure = dset.pressure
    wavelength = dset.wavelength
    elevation = dset.site_pos.elevation
    temperature = dset.temperature
    humidity = dset.humidity

    wvp = np.exp(20.386 - 5132 / temperature) * Unit.mmHg2hPa * humidity * Unit.percent2unit

    for obs in range(dset.num_obs):
        # Compute total zenith delay:
        output[obs] = iers.fculzd_hpa(
            np.degrees(lat[obs]), height[obs], pressure[obs], wvp[obs], wavelength[obs] * Unit.nanometer2micrometer
        )[0]
        # Mapping function:
        output[obs] *= iers.fcul_a(np.degrees(lat[obs]), height[obs], temperature[obs], np.degrees(elevation[obs]))

    return output
