"""Get coefficients for ocean tides

Description:

Reads ocean tides coefficients from file.

"""

# Midgard imports
from midgard.dev import plugins

# Where imports
from where.lib import config
from where import parsers


@plugins.register
def get_ocean_tides():
    """Get ocean tidal loading coefficients

    Reads ocean tidal coefficients from file using OceanTidesFes2004Parser for satellitte
    displacements.

    Returns:
        A dictionary with information about ocean tidal coefficients.
    """
    model = config.tech.orbit_ocean_tides.str
    file_key = f"ocean_tides_{model}" if model else "ocean_tides"

    return parsers.parse_key(file_key).as_dict()
