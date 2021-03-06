"""Edits data based on SLR handling file

Description:
------------

Asdf.

"""
# External library imports
import numpy as np

# Midgard imports
from midgard.dev import plugins
from midgard.math.unit import Unit
from midgard.math import constant

# Where imports
from where import apriori
from where.lib import log
from where.data.time import Time


@plugins.register
def data_handling(dset):
    """Edits data based on SLR handling file

    Args:
        dset:     A Dataset containing model data.

    Returns:
        Array containing False for observations to throw away
    """
    handling = apriori.get("slr_handling_file", time=dset.time)

    for station in dset.unique("station"):
        # Estimate range bias E
        intervals = handling.get(station, {}).get("E", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)

            if np.any(int_idx):
                log.info(
                    f"ILRS handling: Will estimate range bias for station {station} in interval {start_x}-{end_x} in estimate stage"
                )
                dset.estimate_range[:] = np.logical_or(int_idx, dset.estimate_range)
        # Apply range bias R
        intervals = handling.get(station, {}).get("R", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)
            if np.any(int_idx):
                log.info(f"ILRS handling: Applying range bias for station {station} in interval {start_x}-{end_x}")
                RB = info["e_value"]
                if info["unit"] == "mm":
                    dset.range_bias[:] += int_idx * RB * Unit.mm2m
                elif info["unit"] == "ms":
                    dset.range_bias[:] += int_idx * RB * Unit.millisec2seconds * constant.c
                else:
                    log.fatal("Unknown unit on ILRS Data handling file for range bias applied")
        # Estimate time bias U
        intervals = handling.get(station, {}).get("U", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)
            if np.any(int_idx):
                log.info(
                    f"ILRS handling: Will estimate time bias for station {station} in interval {start_x}-{end_x} in estimate stage"
                )
                dset.estimate_time[:] = np.logical_or(int_idx, dset.estimate_time)
        # Apply time bias T
        intervals = handling.get(station, {}).get("T", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)
            if np.any(int_idx):
                log.info(f"ILRS handling: Applying time bias for station {station} in interval {start_x}-{end_x}")
                t_midInterval = Time(start_x + 1 / 2 * (end_x - start_x), fmt="datetime", scale="utc")
                TB = info["e_value"]
                drift = info["e_rate"]
                if info["unit"] == "us":
                    time_drifted = (dset.time.datetime - t_midInterval).jd * drift
                    dset.time_bias[:] += int_idx * (-np.repeat(TB, dset.num_obs) - time_drifted) * Unit.microsec2sec
                else:
                    log.fatal("Unknown unit on ILRS Data handling file for time bias applied")
        # Apply pressure bias P
        intervals = handling.get(station, {}).get("P", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)
            if np.any(int_idx):
                log.info(f"ILRS handling: Applying pressure bias for station {station} in interval {start_x}-{end_x}")
                PB = info["e_value"]
                if info["unit"] == "mB":
                    dset.pressure[:] += int_idx * PB
                else:
                    log.fatal("Unknown unit on ILRS Data handling file for pressure bias applied")
        # Target signature bias C
        intervals = handling.get(station, {}).get("C", [])
        for interval, info in intervals:
            start_x, end_x = interval
            int_idx = dset.filter(station=station) & (dset.time.datetime >= start_x) & (dset.time.datetime <= end_x)
            if np.any(int_idx):
                log.fatal(f"ILRS handling: TODO: Implement target signature bias!")
