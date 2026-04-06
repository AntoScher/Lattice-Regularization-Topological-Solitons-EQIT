import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# Settings for academic look of plots
plt.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def plot_ckm():
    print("Generating CKM matrices comparison plot...")
    
    labels = [r'$|V_{ud}|$', r'$|V_{us}|$ (Cabibbo)', r'$|V_{cd}|$', r'$|V_{cs}|$']
    
    # Experimental data (PDG)
    exp_vals = [0.9740, 0.2250, 0.2210, 0.9730]
    
    # Bare topological amplitudes directly yielding 54% probability leakage
    # (Before 3D framing and Gram-Schmidt orthogonalization)
    bare_vals = [0.626, 0.397, 0.397, 0.626] 

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Experiment (Gray, hatched)
    rects1 = ax.bar(x - width/2, exp_vals, width, label='Experiment (PDG)', color='lightgray', edgecolor='black', hatch='//')
    # EQIT Theory (Blue)
    rects2 = ax.bar(x + width/2, bare_vals, width, label='EQIT (Bare 1D Braid, 54% Leakage)', color='royalblue', edgecolor='black')
    
    # Unitarity threshold lines (probability leakage demonstration)
    ax.axhline(1.0, color='red', linestyle='--', lw=2, label=r'Unitarity Bound ($\Sigma |V_{ij}|^2 = 1$)')

    ax.set_ylabel('Transition Probability Amplitude $|V_{ij}|$', fontsize=14)
    ax.set_title('Topological CKM Matrix Elements vs Standard Model', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=14)
    ax.legend(fontsize=12, loc='upper right', framealpha=1.0)
    ax.grid(True, axis='y', linestyle=':')
    ax.set_ylim(0, 1.15)

    # Add text values above bars
    for i, rect in enumerate(rects1):
        ax.annotate(f'{exp_vals[i]:.3f}', xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11)
    for i, rect in enumerate(rects2):
        ax.annotate(f'{bare_vals[i]:.3f}', xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11, color='darkred' if i > 1 else 'darkblue')

    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ckm_matrix_comparison.png')
    plt.savefig(save_path, dpi=300)
    plt.savefig(save_path.replace('.png', '.eps'), format='eps')
    print(f"Success! Plot saved: {save_path}")

if __name__ == '__main__':
    plot_ckm()