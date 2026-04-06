import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Settings for correct font embedding (prevents artifacts during LaTeX compilation)
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def calculate_parametric_penalty():
    print("--- Parametric estimation of phase space volume (Topological Penalty) ---")
    L = 16
    p_target = 1.0 / 3.0  # Effective probability of a step towards vacuum

    prob = p_target ** L
    
    print(f"Braid length (L): {L}")
    print(f"Local probability (p): {p_target:.4f}")
    print(f"Topological penalty (Order estimation): {prob:.4e}")
    print("-------------------------------------------------------------------\n")
    return prob

def plot_mcmc():
    prob_est = calculate_parametric_penalty()
    
    print("Generating honest MCMC plot (Demonstration of entropy growth)...")
    np.random.seed(42)
    
    L_start = 16
    n_steps = 100
    n_trajectories = 10
    
    # Cayley graph distance dynamics (p_down = 1/6, p_up = 5/6)
    p_down = 1.0 / 6.0
    
    steps = np.arange(n_steps + 1)
    plt.figure(figsize=(10, 5))
    
    for _ in range(n_trajectories):
        L = L_start
        trajectory = [L]
        for _ in range(n_steps):
            if np.random.rand() < p_down and L > 0:
                L -= 1
            else:
                L += 1
            trajectory.append(L)
        
        plt.plot(steps, trajectory, linewidth=1.5, alpha=0.7)
        
    plt.xlabel('MCMC Steps (Collision Time / Thermalization)', fontsize=12)
    plt.ylabel('Topological Complexity (Cayley Graph Distance $L$)', fontsize=12)
    plt.title('Ergodic Random Walk on $B_4$: Entropy Growth and Topological Viscosity', fontsize=14)
    
    plt.axhline(0, color='red', linestyle='--', linewidth=2, label='Vacuum State ($L=0$)')
    plt.axhline(L_start, color='gray', linestyle=':', label=f'Initial State ($L={L_start}$)')
    
    # Add text box with parametric estimation
    text_str = (f"Parametric Phase-Space Suppression:\n"
                f"$\\eta \\sim p^L \\approx (1/3)^{{16}} \\sim \\mathcal{{O}}(10^{{-8}})$\n"
                f"Direct simulation hitting vacuum ($L=0$) is entropically suppressed.")
    plt.text(0.05, 0.85, text_str, transform=plt.gca().transAxes, fontsize=11,
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='silver', boxstyle='round,pad=0.5'))

    plt.grid(True, ls=':', color='silver')
    plt.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig('mcmc_trajectories_plot.eps', format='eps', bbox_inches='tight')
    plt.savefig('mcmc_trajectories_plot.png', dpi=300, bbox_inches='tight')
    print("Success: Plot saved as 'mcmc_trajectories_plot.eps' and 'mcmc_trajectories_plot.png'")

if __name__ == '__main__':
    plot_mcmc()