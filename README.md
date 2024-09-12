### Data and csource code for the paper "Learning and forecasting open quantum dynamics with correlated noise"

- The folder "experiment_data" contains all the experiment data, together with the reconstructed process tensor, for example, the subpath len40/idle100/rb_data_0.1/data.json is the raw experiment data for Vibas = 0.4 * 0.1 (the actual Vbias is rescaled by 0.4). The files starting with processtensor, unitaryfidelities, unitaryprocesstensor under the same folder are data produced in the reconstruction algorithm.
- The folder "result" contains the reconstruction results, which are used for plotting
- The file "two_qubit_model_rb_unitary.jl" is the main file used to reconstruct the process tensor and then store them, the open source package UnitaryMatrices is also used 
- The files starting with plot will plot the data figures (partially) used in the paper