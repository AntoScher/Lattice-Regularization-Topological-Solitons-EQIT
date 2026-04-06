===========================================================================
SUPPLEMENTARY CODE REPOSITORY
"Lattice Regularization of Topological Solitons: 3D Framing, the Mass Hierarchy, and the WIMP Miracle"
===========================================================================

This repository contains the complete, reproducible computational framework 
accompanying the manuscript. The codebase is designed to be transparent, 
deterministic, and free of "black-box" machine learning algorithms.

### 🚀 Interactive Model Demonstration
You can run the core phenomenological mass predictions directly in your browser without installing any dependencies:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AntoScher/EQIT-Continuous-Limit/blob/main/Model_Demonstration.ipynb)

--- DEPENDENCIES ---
Python 3.8+
Install requirements via:
pip install -r requirements.txt

--- FILE ARCHITECTURE ---

1. THE MASS HIERARCHY & INVERSE SPECTRAL PROBLEM
   - topological_hamiltonian.py 
     Core mathematical engine. Generates the discrete NxN Hamiltonian 
     matrices based on knot topology (Hamming distance tunneling, 
     chiral parity violation).
   - run_calibration.py
     Executes the Inverse Spectral Problem. Uses PyTorch (L-BFGS) to 
     calibrate vacuum parameters (\mu, \lambda) exclusively on the 
     electron and muon masses, followed by a blind prediction of the 
     tau-lepton mass.
   - verify_alexander_polynomials.py
     Algebraic proof using SymPy. Computes the knot determinants |Delta(-1)|
     from Alexander polynomials, rigidly proving C=7 for the 5_2 tau knot 
     and C=5 for the degenerate 5_1 knot.
   - vacuum_bridge.py
     Maps the discrete parameters (\mu, \lambda) back to the continuous 
     Faddeev-Niemi EFT parameters (v, c_2) in natural lattice units.
   - sensitivity_analysis.py
     Performs a Monte Carlo sensitivity analysis of the Hamiltonian. 
     Injects 0.2% structural noise into the vacuum parameters to prove 
     the topological protection and robustness of the tau-lepton mass prediction.
   - Model_Demonstration.ipynb
     A self-contained Jupyter Notebook for interactive step-by-step execution 
     of the core mass predictions.

2. DARK MATTER & WIMP MIRACLE
   - calculate_dm_mass.py
     Generates the Hamiltonian for the 8_3 amphichiral knot (C=17) and 
     computes its ground state energy to predict the 5.1 TeV dark matter mass.
   - simulate_relic_annihilation.py
     Computes the thermal relic density cross-section for the topological WIMP.
   - simulate_elastic_scattering.py
     Estimates the exponential suppression of the direct detection cross-section 
     based on the topological rigidity of the 8_3 knot.

3. QUARK MIXING & 3D FRAMED CKM MATRIX
   - framed_braid_algebra.py
     Computes the transition amplitudes between topological quark states 
     using the 3D framed braid algebra. Applies Gram-Schmidt orthogonalization 
     to mathematically restore CKM unitarity and generate the Jarlskog invariant.

4. SCHEMATIC FIGURES & DYNAMICS (Figs 1-6)
   The conceptual diagrams and dynamic plots in the paper are mathematically 
   generated using Python scripts (e.g., generate_schematics.py, calculate_higgs_mass.py, 
   plot_annihilation_dynamics.py, plot_ckm_matrix.py) included in this repository.

5. ADDITIONAL VERIFICATION SCRIPTS [SUPPLEMENTARY]
   - verify_higher_invariants.py
     Strict SymPy verification of knot determinants for 6_1 (4th gen fermion) 
     and 8_3 (dark matter) topological sectors.
   - visualize_coarse_graining.py
     Quantitative demonstration of Kadanoff coarse-graining RG flow supporting Fig. 1.
   - optimize_single_parameter.py
     [Optional] Demonstrates reduction of the framework to a single free parameter.
   - simulate_b4_monte_carlo.py
     [Supplementary] Monte Carlo demonstration of topological phase-space suppression 
     and entropy growth on the B_4 braid group.

--- HOW TO RUN ---
All scripts are standalone. You can verify the core results by running:
> python run_calibration.py
> python verify_alexander_polynomials.py
> python calculate_dm_mass.py
> python framed_braid_algebra.py
> python sensitivity_analysis.py
> python verify_higher_invariants.py
> python visualize_coarse_graining.py