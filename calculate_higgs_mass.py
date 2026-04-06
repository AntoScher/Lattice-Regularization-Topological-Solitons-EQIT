import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def plot_linear_o3_potential():
    print("=== ILQC: Linear O(3) Model & Mexican Hat Potential ===")
    
    rho = np.linspace(-2.0, 2.0, 400)
    v = 1.0 # Vacuum Expectation Value (VEV)
    lam = 1.5 # Self-coupling lambda
    
    # Mexican Hat Potential V(rho) = lambda * (rho^2 - v^2)^2
    V_rho = lam * (rho**2 - v**2)**2
    
    plt.figure(figsize=(9, 6))
    plt.plot(rho, V_rho, 'b-', linewidth=2.5, label=r'$V(\rho) = \lambda(\rho^2 - v^2)^2$')
    
    # Mark VEV
    plt.plot([v, -v], [0, 0], 'ro', markersize=8, label=r'Vacuum Expectation Value $\pm v$')
    plt.axvline(v, color='r', linestyle=':', alpha=0.6)
    plt.axvline(-v, color='r', linestyle=':', alpha=0.6)
    
    # Annotate Higgs mode
    plt.annotate('Radial Higgs Mode (Fluctuations of $\\rho$)', xy=(v+0.2, lam*0.5), xytext=(v+0.4, lam*1.5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=11)
    
    plt.title('Linear $O(3)$ Sigma Model: The Emergent Higgs Potential', fontsize=14)
    plt.xlabel(r'Radial Amplitude $\rho$ (Order Parameter)', fontsize=12)
    plt.ylabel(r'Potential Energy Density $V(\rho)$', fontsize=12)
    plt.ylim(-0.2, 4.0)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    
    save_path = 'higgs_potential.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.savefig('higgs_potential.eps', format='eps', dpi=300, bbox_inches='tight')
    print(f"График потенциала Мексиканской шляпы сохранен как '{save_path}'")

if __name__ == '__main__':
    plot_linear_o3_potential()
