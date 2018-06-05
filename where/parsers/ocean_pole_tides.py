"""A parser for reading data ocean pole tide coefficients

Description:
------------

Reads ocean pole tide coefficients. The file contains the real and imaginary coefficients for the enu components in
a lat-lon grid. The data is ordered in columns.



$Revision: 15011 $
$Date: 2018-05-04 16:19:35 +0200 (Fri, 04 May 2018) $
$LastChangedBy: hjegei $

"""

import numpy as np

# Where imports
from where.parsers._parser_line import LineParser
from where.lib import plugins


@plugins.register
class OceanPoleTidesParser(LineParser):
    """A parser for reading Ocean Pole Tides data
    """

    def setup_parser(self):
        return dict(names=["lon", "lat", "u_r_R", "u_r_I", "u_n_R", "u_n_I", "u_e_R", "u_e_I"], skip_header=14)