from typing import Union

import numpy as np
from quantify_scheduler.schedules.schedule import Schedule
from quantify_scheduler.operations.pulse_library import SquarePulse
from qudacs.rb.standard_rb import decomp_epstein, single_qubit_standard_rb_sched


def flux_sq_standard_rb(
    qubit_rb: str,
    qubit_flux: str,
    flux_pulse_amp: float,
    n_cl: Union[np.ndarray, int],
    seed=None,
    use_cal_points: bool = True,
    repetitions: int = 1024,
) -> Schedule:
    if isinstance(n_cl, int):
        n_cl = np.array([n_cl])

    sched = single_qubit_standard_rb_sched(
        qubit=qubit_rb,
        n_cl=n_cl,
        seed=seed,
        use_cal_points=use_cal_points,
        repetitions=repetitions,
    )

    for cur_n in n_cl:
        sched.add(
            # long enough for covering all possible epstein decompositions
            SquarePulse(
                amp=flux_pulse_amp,
                duration=(cur_n + 1) * (3 * 20e-9 +180e-9)-180e-9+ 20e-9,
                port=f"{qubit_flux}:flux",
            ),
            ref_op=f"RB-seq n_cl={cur_n}, measure",
            ref_pt="start",
            ref_pt_new="end",
            rel_time=-20e-9,
        )

    return sched

