import numpy as np

from where import apriori
from where.lib import config
from where.lib import plugins
from where.lib import log


@plugins.register
def nnt_trf(dset, param_names):
    n = len(param_names)
    d = np.zeros((n, 3))
    stations = set()
    # todo: config
    reference_frame = config.tech.reference_frames.list[0]
    s = 0.0001

    trf = apriori.get("trf", time=dset.time.utc.mean, reference_frames=reference_frame)

    # thaller2008: eq 2.51 (skipping scale factor)
    for idx, column in enumerate(param_names):
        if "_site_pos-" not in column:
            continue
        station = column.split("-", maxsplit=1)[-1].split("_")[0]
        site_id = dset.meta[station]["site_id"]
        if site_id in trf:
            # x0, y0, z0 = trf[site_id].pos.itrs
            if column.endswith("_x"):
                d[idx, :] = np.array([1, 0, 0])
            if column.endswith("_y"):
                d[idx, :] = np.array([0, 1, 0])
            if column.endswith("_z"):
                d[idx, :] = np.array([0, 0, 1])
            stations.add(station)

    constraint = __name__
    log.info(f"Applying {constraint} with {', '.join(stations)} from {reference_frame.upper()}")
    # thaller2008: eq 2.57
    try:
        h = np.linalg.inv(d.T @ d) @ d.T
    except np.linalg.LinAlgError:
        h = np.zeros((3, n))
        log.warn(f"Applying {constraint} failed")
    sigma = np.array([s] * 3)
    return h, sigma
