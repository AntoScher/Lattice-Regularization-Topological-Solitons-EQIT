import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# Settings for academic graphics
plt.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def plot_exclusion_limits():
    print("=== EQIT Phase 2: Direct Detection Modeling (XENONnT/LZ) ===\n")
    
    # 1. Physical constants and EQIT parameters
    m_chi_target = 5100.0  # GeV (8_3 knot)
    C_83 = 17.0            # Strict Alexander polynomial det for 8_3
    alpha_topo = 0.13      # Topological surgery constant
    
    # Bare weak scalar exchange cross-section
    sigma_bare_weak = 1e-39 
    
    # 2. Topological suppression of elastic scattering
    P_elastic = (alpha_topo**2) * np.exp(-C_83)
    
    sigma_eqit = sigma_bare_weak * P_elastic
    
    print(f"DM Candidate Mass         : {m_chi_target} GeV")
    print(f"Bare weak cross-section   : {sigma_bare_weak:.1e} cm^2")
    print(f"Rigidity penalty (C=17)   : exp(-17) = {np.exp(-C_83):.2e}")
    print(f"Total elastic factor      : {P_elastic:.2e}")
    print(f"Predicted cross-section   : {sigma_eqit:.2e} cm^2\n")
    
    # 3. Generating data for experimental limits
    masses = np.logspace(1, 4, 100)
    
    # Approximation of XENON1T limit (2018)
    limit_xenon1t = 1e-46 * (masses / 30.0) * np.exp(30.0 / masses)
    
    # Approximation of LZ / XENONnT limit (2023)
    limit_lz = 1e-47 * (masses / 30.0) * np.exp(30.0 / masses)
    
    # Approximation of Neutrino Floor (CEvNS)
    neutrino_floor = 1e-49 * (masses / 30.0) * np.exp(10.0 / masses)
    
    # 4. Plotting
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.loglog(masses, limit_xenon1t, color='gray', linestyle='--', lw=2, label='XENON1T (2018)')
    ax.loglog(masses, limit_lz, color='blue', linestyle='-', lw=2.5, label='XENONnT / LZ Current Limit')
    ax.loglog(masses, neutrino_floor, color='orange', linestyle='-', lw=2, alpha=0.7)
    
    # Fill exclusion zones
    ax.fill_between(masses, limit_lz, 1e-38, color='blue', alpha=0.05)
    ax.fill_between(masses, 1e-55, neutrino_floor, color='orange', alpha=0.15, hatch='//', label=r'Neutrino Floor (CE$\nu$NS)')
    
    # EQIT Prediction Point
    ax.plot(m_chi_target, sigma_eqit, 'y*', markersize=24, markeredgecolor='black', label=r'EQIT Knot $8_3$ Prediction')
    
    # Annotations
    ax.annotate(f"Rigidity Suppression\n$\\propto \\exp(-C_{{8_3}})$", xy=(m_chi_target, sigma_eqit), xytext=(m_chi_target*0.15, sigma_eqit*2e2),
                arrowprops=dict(facecolor='darkred', shrink=0.05, width=1.5, headwidth=8),
                fontsize=12, color='darkred', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="darkred", lw=1))
    
    ax.set_xlim(10, 10000)
    ax.set_ylim(1e-53, 1e-42)
    ax.set_xlabel(r'Dark Matter Mass $m_\chi$ (GeV)', fontsize=14)
    ax.set_ylabel(r'Spin-Independent Elastic Cross Section $\sigma_{SI}$ (cm$^2$)', fontsize=14)
    ax.set_title('Direct Detection Exclusions vs EQIT Topological Dark Matter', fontsize=16)
    ax.grid(True, which="both", ls=":", alpha=0.7)
    ax.legend(loc='upper left', fontsize=12)
    
    plt.tight_layout()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(base_dir, 'elastic_scattering_exclusion.png'), dpi=300)
    plt.savefig(os.path.join(base_dir, 'elastic_scattering_exclusion.eps'), format='eps')
    print("Exclusion limits plot saved successfully!")

if __name__ == "__main__":
    plot_exclusion_limits()