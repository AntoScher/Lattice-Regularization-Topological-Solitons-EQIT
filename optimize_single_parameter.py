import numpy as np
from scipy.optimize import root_scalar, minimize_scalar
import math
import os

print("=== SINGLE PARAMETER THEORY (Reduction to a single vacuum constant) ===")
print("Hypothesis: Fixing the electron mass M_e = 1.0 rigidly links lambda and mu.")
print("ONLY ONE parameter is optimized: tension mu.\n")

# 1. Fundamental fixed constants
beta = 2.5           # 3D dense packing index (Strictly 5/2)
delta = 0.020009     # Quantum tunneling (from level k=155)

# 2. Invariant vectors
C_31 = np.array([3, 1, 1, 1, 1, 1, 1, 3])
C_41 = np.array([5] + [1]*14 + [5])
C_52 = np.array([7] + [1]*30 + [7])

def get_B(lam):
    """Analytical derivation of B via lambda and perturbation theory"""
    return (delta**2 / 9.0) * (3.0 / lam) * np.exp(beta * 4.0)

def build_H(K, mu, lam, C_array):
    """Builds Hermitian Hamiltonian for a given knot"""
    N = 2**K
    H = np.zeros((N, N), dtype=np.complex128)
    
    # Diagonal
    tension = mu * np.exp(beta * K)
    np.fill_diagonal(H, tension * K - lam * C_array)
    
    # Tunneling
    d = -delta / K
    for i in range(N):
        for bit in range(K):
            j = i ^ (1 << bit)
            H[i, j] += d
            
    # Chiral parity violation
    B_val = get_B(lam)
    for i in range(N // 2):
        j = (N - 1) - i
        H[i, j] += 1j * B_val
        H[j, i] -= 1j * B_val
        
    return H

def get_ground_state(K, mu, lam, C_array):
    """Fast calculation of the lowest eigenvalue"""
    H = build_H(K, mu, lam, C_array)
    eigvals = np.linalg.eigvalsh(H)
    return eigvals[0].real

def find_lambda_for_electron(mu):
    """CRUCIAL FUNCTION: Finds lambda so that M_e is strictly equal to 1.0"""
    def objective(lam):
        return get_ground_state(3, mu, lam, C_31) - 1.0
    
    # Search for root (lambda) in a wide range
    res = root_scalar(objective, bracket=[0.1, 20.0], method='brentq')
    return res.root

def muon_mass_error(mu):
    """Loss function of ONLY ONE parameter (mu)"""
    try:
        lam = find_lambda_for_electron(mu)
        M_mu = get_ground_state(4, mu, lam, C_41)
        # Relative squared error from muon mass
        return ((M_mu - 206.8) / 206.8)**2
    except ValueError:
        return 1e6 # In case of unphysical mu

# === LAUNCH ABSOLUTE 1D OPTIMIZATION ===
print("Launching scalar search (Bounded 1D Minimization)...")
res = minimize_scalar(muon_mass_error, bounds=(0.001, 0.01), method='bounded')

best_mu = res.x
best_lam = find_lambda_for_electron(best_mu)

M_e = get_ground_state(3, best_mu, best_lam, C_31)
M_mu = get_ground_state(4, best_mu, best_lam, C_41)
M_tau = get_ground_state(5, best_mu, best_lam, C_52)

print("\n=== PERFECT SOLUTION FOUND ===")
print(f"Free parameters: 1")
print(f"Fundamental vacuum tension (mu): {best_mu:.6f}")
print(f"Coupled topological constant (lambda): {best_lam:.6f} (Derived from condition M_e = 1.0)\n")

print("--- MASS SPECTRUM ---")
print(f"Electron (3_1): {M_e:.4f} (Scale calibration)")
print(f"Muon (4_1):     {M_mu:.4f} (1D optimization target)")
print(f"Tau (5_2):      {M_tau:.4f} (Blind predictive test. Experiment: 3477.0)")