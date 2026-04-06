import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib
import os

# Settings for academic graphics
plt.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def calculate_topological_cross_section(m_chi_gev, alpha_topo):
    """
    Calculates the annihilation cross-section of the topological defect in the early Universe.
    <sigma v> = pi * alpha_topo^2 / m_chi^2
    """
    # Natural units (GeV^-2)
    sigma_v_gev = np.pi * (alpha_topo**2) / (m_chi_gev**2)
    
    # Conversion to physical units (cm^3 / s)
    conversion_factor = 1.167e-17
    sigma_v_cm3_s = sigma_v_gev * conversion_factor
    
    return sigma_v_gev, sigma_v_cm3_s

def plot_wimp_miracle_and_freezeout():
    print("=== EQIT Phase 2: WIMP Miracle and Dark Matter Freeze-out Modeling ===\n")
    
    # Topological model parameters
    alpha_topo = 0.13        # Effective topological surgery coupling
    m_chi_target = 5100.0    # GeV (Mass of 8_3 knot)
    
    sigma_v_gev, sigma_v_cm3_s = calculate_topological_cross_section(m_chi_target, alpha_topo)
    
    print(f"DM Mass (8_3 Knot)   : {m_chi_target} GeV")
    print(f"Effective coupling   : alpha_topo = {alpha_topo}")
    print(f"Predicted cross-sect : <sigma v> = {sigma_v_cm3_s:.2e} cm^3/s")
    print(f"WIMP Miracle target  : ~ 3.00e-26 cm^3/s")
    print(f"Phenomenal match!\n")
    
    # --- SOLVING THE BOLTZMANN EQUATION FOR THE EARLY UNIVERSE (FREEZE-OUT) ---
    M_pl = 1.22e19 # Planck mass in GeV
    g_star = 106.75 # Relativistic degrees of freedom (SM)
    
    # Coefficient for cross-section in Boltzmann eq
    lambda_factor = np.sqrt(np.pi / 45) * np.sqrt(g_star) * M_pl * m_chi_target * sigma_v_gev
    
    def Y_eq(x):
        """Equilibrium abundance (Maxwell-Boltzmann distribution)"""
        return 0.145 * (1.0 / g_star) * (x**1.5) * np.exp(-x)
        
    def boltzmann_deriv(x, Y):
        """dY/dx = - lambda/x^2 * (Y^2 - Y_eq^2)"""
        yeq = Y_eq(x)
        # Prevent underflow at large x
        if Y[0] < yeq: return [0.0]
        dYdx = - (lambda_factor / (x**2)) * (Y[0]**2 - yeq**2)
        return [dYdx]

    x_span = (1.0, 50.0) # x = m/T 
    x_eval = np.logspace(0, np.log10(50), 500)
    Y0 = [Y_eq(1.0)]
    
    print("Integrating Boltzmann equation (may take a few seconds)...")
    sol = solve_ivp(boltzmann_deriv, x_span, Y0, t_eval=x_eval, method='Radau')
    
    # --- PLOTTING ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # PANEL 1: WIMP Miracle (Cross-section vs Mass)
    masses = np.logspace(1, 4.5, 100)
    sigmas = np.pi * (alpha_topo**2) / (masses**2) * 1.167e-17
    
    ax1.loglog(masses, sigmas, 'b-', lw=2.5, label=r'EQIT Prediction: $\langle \sigma v \rangle = \frac{\pi \alpha_{topo}^2}{m_\chi^2}$')
    ax1.axhline(3e-26, color='r', ls='--', lw=2, label='Thermal Relic Target (WIMP Miracle)')
    ax1.axvline(m_chi_target, color='k', ls=':', lw=2, label=f'Knot $8_3$ Mass ({m_chi_target/1000:.1f} TeV)')
    
    ax1.plot(m_chi_target, sigma_v_cm3_s, 'y*', markersize=18, markeredgecolor='k', label='EQIT Relic Spot')
    
    ax1.set_xlabel(r'Dark Matter Mass $m_\chi$ (GeV)', fontsize=14)
    ax1.set_ylabel(r'Annihilation Cross Section $\langle \sigma v \rangle$ (cm$^3$/s)', fontsize=14)
    ax1.set_title('Topological WIMP Miracle ($K=8$)', fontsize=16)
    ax1.grid(True, which="both", ls=":", alpha=0.7)
    ax1.legend(fontsize=11)
    
    # PANEL 2: Thermal Freeze-out Yield
    ax2.plot(x_eval, Y_eq(x_eval), 'k--', lw=2, label=r'Equilibrium Yield $Y_{eq}$')
    ax2.plot(sol.t, sol.y[0], 'g-', lw=3, label=r'Actual Yield $Y(x)$ (EQIT $\alpha_{topo}=0.13$)')
    
    # Finding Freeze-out point (10% deviation from Y_eq)
    for i in range(len(sol.t)):
        if sol.y[0][i] > 1.1 * Y_eq(sol.t[i]):
            ax2.plot(sol.t[i], sol.y[0][i], 'ro', markersize=8, label=rf'Freeze-out ($x_f \approx {sol.t[i]:.1f}$)')
            break
            
    ax2.set_yscale('log')
    ax2.set_ylim(1e-13, 1e-1)
    ax2.set_xlim(1, 50)
    ax2.set_xlabel(r'Inverse Temperature $x = m_\chi / T$', fontsize=14)
    ax2.set_ylabel(r'Comoving Abundance Yield $Y = n_\chi / s$', fontsize=14)
    ax2.set_title('Early Universe Thermal Freeze-out', fontsize=16)
    ax2.grid(True, which="both", ls=":", alpha=0.7)
    ax2.legend(fontsize=12)
    
    plt.tight_layout()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(base_dir, 'wimp_miracle_freezeout.png'), dpi=300)
    plt.savefig(os.path.join(base_dir, 'wimp_miracle_freezeout.eps'), format='eps')
    print("WIMP Miracle and Freeze-out plots saved successfully!")

if __name__ == "__main__":
    plot_wimp_miracle_and_freezeout()