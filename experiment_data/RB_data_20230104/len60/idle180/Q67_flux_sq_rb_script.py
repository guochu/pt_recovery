import numpy as np
from quantify_core.measurement import MeasurementControl
from qudacs.custom_gettables import RBPopulationGettable
from qudacs.characterize import Charact
from qudacs_externals.nmkv_noise_bmk.flux_sq_rb import flux_sq_standard_rb

charact = Charact(2)
charact._meas_ctrl.instr_plotmon.get_instr().tuids_max_num(15)

charact._sweetspots["q0"] = -0.03
charact._anti_sweetspots["q0"] = 4
charact._sweetspots["q1"] = 0.65

charact._anti_sweetspots["q1"] = 4.2
charact.prepare_single_qubit_characterizing("q1")
charact._qdev.cfg_sched_repetitions(2048)

# A测参数
charact.transmon_eles["q1"].submodules["clock_freqs"].f01(5.154353391e9+143860-140594)
charact.transmon_eles["q1"].submodules["rxy"].duration(20e-9)
charact.transmon_eles["q1"].submodules["rxy"].amp180(0.554)
charact.transmon_eles["q1"].submodules["rxy"].motzoi(-0.23)

# # B测参数#
# charact.transmon_eles["q1"].submodules["clock_freqs"].f01(5.1548e9-89463+6143)
# charact.transmon_eles["q1"].submodules["rxy"].duration(20e-9)
# charact.transmon_eles["q1"].submodules["rxy"].amp180(0.5265)
# charact.transmon_eles["q1"].submodules["rxy"].motzoi(-0.16)

charact.transmon_eles["q1"].submodules["measure"].acq_delay(180e-9)
charact.transmon_eles["q1"].submodules["clock_freqs"].readout(6.63796e9)
charact.transmon_eles["q1"].submodules["measure"].pulse_duration(600e-9)
charact.transmon_eles["q1"].submodules["measure"].integration_time(2.2e-6)
charact.transmon_eles["q1"].submodules["measure"].pulse_amp(0.480)

charact.transmon_eles["q1"].submodules["reset"].duration(700e-6)

from quantify_core.analysis.calibration import rotate_to_calibrated_axis
import matplotlib.pyplot as plt

class RBDataAnalysis:
    def __init__(self, data: np.ndarray, cal0_index: int = -2, cal1_index: int = -1):
        processed_data = np.array([val[0] + val[1] * 1j for val in data.values()])
        # np.save(f_raw, processed_data)
        self.data = processed_data[:-2]  # FIXME
        self.cal0 = processed_data[cal0_index]
        self.cal1 = processed_data[cal1_index]

    def run(self):
        p1 = rotate_to_calibrated_axis(self.data, self.cal0, self.cal1).real
        self.p0 = np.ones(len(p1)) - p1
        return self.p0

res_list_withflux = []


# for DC_amp in [0,1.4065]:
#     charact._sweetspots["q0"] = DC_amp
#     charact.prepare_single_qubit_characterizing("q1")
#     charact.measure_gate_fidelities_rb("q1", clifford_seq_lengths=2**np.arange(11), nr_samples=100)


for flux_pulse_amp in [0.1,0.2,0.3,0.4,0.5,0.52,0.54,0.56,0.58,0.6,0.61,0.62,0.63,0.64]:
    # f = open(f"rb_data_40_{flux_pulse_amp}.npy", "wb")
    # # f = open(f"rb_data_1024.npy", "ab")

    # sched_kwargs = {
    #     "qubit_rb": "q1",
    #     "qubit_flux": "q0",
    #     "flux_pulse_amp": flux_pulse_amp,
    #     # "n_cl": 2**np.arange(0, 11),
    #     "n_cl":np.arange(1,40),
    #     "use_cal_points": True,
    #     "seed": None,
    #     "repetitions": 2048,
    # }
    # for j in range(200):
    #     res = charact.run_external(
    #         sched_gen=flux_sq_standard_rb,
    #         sched_kwargs=sched_kwargs,
    #         analysis_cls=RBDataAnalysis,
    #     )
    #     np.save(f, res)
    #     res_list_withflux.append(res)
    # # f_raw.close()
    # f.close()

    f = open(f"rb_data_60_{flux_pulse_amp}.npy", "wb")
    sched_kwargs = {
        "qubit_rb": "q1",
        "qubit_flux": "q0",
        "flux_pulse_amp": flux_pulse_amp,
        "n_cl":np.arange(1,60),
        "use_cal_points": True,
        "seed": None,
        "repetitions": 2048,
    }

    for j in range(200):
        res = charact.run_external(
            sched_gen=flux_sq_standard_rb,
            sched_kwargs=sched_kwargs,
            analysis_cls=RBDataAnalysis,
        )
        np.save(f, res)
        res_list_withflux.append(res)
    f.close()


