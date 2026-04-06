import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Settings for correct font embedding (prevents artifacts during LaTeX compilation)
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def plot_annihilation():
    print("Generating knot annihilation dynamics plot...")
    
    # Spatial coordinate x (femtometers)
    x = np.linspace(-10, 10, 1000)
    
    # --- Functions for modeling energy density H(x) ---
    # 1. Soliton (massive knot). Static clump of gradients.
    def soliton_energy(x, pos, width=1.2, amplitude=1.0):
        return amplitude * np.exp(-((x - pos) / width)**2)
        
    # 2. Photon (traveling wave). Oscillating gradients.
    def photon_energy(x, pos, width=2.5, k=4.0, amplitude=0.4):
        # Wave energy is proportional to the derivative squared, so it is always positive and pulsating
        envelope = np.exp(-((x - pos) / width)**2)
        return amplitude * envelope * (np.sin(k * (x - pos))**2 + 0.1)

    # --- Preparation of panels (4 panels for demonstrating quantum branching) ---
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    
    # --- Panel 1: t = -5 fm/c (Approach) ---
    y1 = soliton_energy(x, -5) + soliton_energy(x, 5)
    axs[0].plot(x, y1, 'b-', lw=3, label='Topological Solitons (Knots)')
    axs[0].fill_between(x, 0, y1, color='blue', alpha=0.1)
    axs[0].set_title(r'1. Asymptotic Past ($t < 0$): Stable Knots in EFT Regime', fontsize=14)
    axs[0].annotate('Mass $M_1$', xy=(-5, 1.05), ha='center', fontsize=12)
    axs[0].annotate('Mass $M_2$', xy=(5, 1.05), ha='center', fontsize=12)
    axs[0].annotate(r'$\rightarrow v$', xy=(-3.5, 0.5), fontsize=14)
    axs[0].annotate(r'$\leftarrow -v$', xy=(3.5, 0.5), ha='right', fontsize=14)
    
    # --- Panel 2: t = 0 (Collision and rupture) ---
    # Gradients overlap and amplify non-linearly (Skyrme term)
    y2 = soliton_energy(x, 0, width=0.6, amplitude=3.5) 
    axs[1].plot(x, y2, 'r-', lw=3, label='Non-linear Energy Spike')
    axs[1].fill_between(x, 0, y2, color='red', alpha=0.2)
    axs[1].axvspan(-0.6, 0.6, color='yellow', alpha=0.3, label='EFT Breakdown (Combinatorial Fireball)')
    axs[1].set_title(r'2. Collision ($t = 0$): Gradient Spike & Braid Reconnection', fontsize=14)
    axs[1].annotate('Combinatorial\nHamiltonian $\hat{H}$ active', xy=(0, 1.5), ha='center', fontsize=11, 
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="r", lw=1))

    # --- Panel 3: Outcome A (Annihilation) ---
    # Mass disappeared, energy transferred to traveling vacuum ripples
    y3 = photon_energy(x, -5) + photon_energy(x, 5)
    axs[2].plot(x, y3, 'g-', lw=2, label='Emergent Photons (Twist Waves)')
    axs[2].fill_between(x, 0, y3, color='green', alpha=0.1)
    axs[2].set_title(r'3. Outcome A ($t > 0$): Complete Annihilation (Probability $\eta \sim 10^{-8}$)', fontsize=14, color='darkgreen')
    axs[2].annotate(r'$\leftarrow c$', xy=(-3.5, 0.4), ha='right', fontsize=14)
    axs[2].annotate(r'$\rightarrow c$', xy=(3.5, 0.4), fontsize=14)
    axs[2].annotate(r'$E_{\gamma} = M c^2$', xy=(-5, 0.6), ha='center', fontsize=12)
    axs[2].annotate(r'$E_{\gamma} = M c^2$', xy=(5, 0.6), ha='center', fontsize=12)

    # --- Panel 4: Outcome B (Elastic scattering) ---
    # Solitons bounced off, preserving topological charge. Part of energy went into soft radiation.
    y4_solitons = soliton_energy(x, -6, amplitude=0.9) + soliton_energy(x, 6, amplitude=0.9)
    y4_radiation = photon_energy(x, 0, width=4.0, k=2.0, amplitude=0.15) # Soft ripple in the center
    axs[3].plot(x, y4_solitons, 'b-', lw=3, label='Scattered Solitons (Preserved Topology)')
    axs[3].plot(x, y4_radiation, 'g--', lw=1.5, label='Soft Bremsstrahlung Radiation')
    axs[3].fill_between(x, 0, y4_solitons, color='blue', alpha=0.1)
    axs[3].set_title(r'4. Outcome B ($t > 0$): Elastic/Inelastic Scattering (Probability $1 - \eta \approx 1$)', fontsize=14, color='darkblue')
    axs[3].annotate(r'$\leftarrow v^\prime$', xy=(-4.5, 0.5), ha='right', fontsize=14)
    axs[3].annotate(r'$\rightarrow v^\prime$', xy=(4.5, 0.5), fontsize=14)

    # --- Axis and legend settings ---
    for ax in axs:
        ax.set_ylabel(r'Energy Density $\mathcal{H}$', fontsize=12)
        ax.set_ylim(0, 4.2)
        ax.set_yticks([]) # Remove numbers on Y axis for concept clarity
        ax.grid(True, ls=":", color='silver')
        ax.legend(loc='upper right', fontsize=10)
        
        # Drawing the baseline vacuum level (tension M^2)
        ax.axhline(0, color='k', lw=1)

    axs[3].set_xlabel('Spatial Coordinate $x$ (fm)', fontsize=14)
    axs[3].set_xlim(-10, 10)
    
    plt.tight_layout()
    
    # Saving
    plt.savefig('annihilation_dynamics_plot.eps', format='eps', bbox_inches='tight')
    plt.savefig('annihilation_dynamics_plot.png', dpi=300, bbox_inches='tight')
    print("Success: Plot saved as 'annihilation_dynamics_plot.png'")

if __name__ == '__main__':
    plot_annihilation()