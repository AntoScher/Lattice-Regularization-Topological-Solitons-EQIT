import torch
import math

def build_hamiltonian(K, C_inv, mu, beta, lam, delta, B):
    """
    Generates the Hermitian Hamiltonian matrix 2^K x 2^K for a given topological knot.
    """
    N = 2**K
    H = torch.zeros((N, N), dtype=torch.complex128)
    
    # 1. Diagonal elements (Geometric tension)
    tension = mu * math.exp(beta * K)
    base_energy = tension * K
    
    # Topological penalty (applied only to macroscopically coherent states)
    C_array = torch.ones(N, dtype=torch.float64)
    C_array[0] = C_inv
    C_array[-1] = C_inv
    
    diag_energies = base_energy - lam * C_array
    diag_indices = torch.arange(N)
    H[diag_indices, diag_indices] = diag_energies.to(torch.complex128)
    
    # 2. Off-diagonal elements (Quantum Reidemeister tunneling)
    i = torch.arange(N).view(N, 1)
    j = torch.arange(N).view(1, N)
    xor_matrix = torch.bitwise_xor(i, j)
    is_power_of_2 = (torch.bitwise_and(xor_matrix, xor_matrix - 1) == 0) & (xor_matrix != 0)
    
    d = -delta / K
    H[is_power_of_2] = complex(d, 0)
            
    # 3. Parity violation (Coupling of absolute mirror states)
    for idx in range(N // 2):
        mirror_idx = (N - 1) - idx
        H[idx, mirror_idx] += 1j * B
        H[mirror_idx, idx] -= 1j * B
        
    return H

if __name__ == "__main__":
    print("=== EQIT Phase 2: Exact Mass Calculation for Dark Matter & Heavy Fermions ===\n")
    
    # Frozen vacuum parameters from Phase 1 (Inverse Spectral Problem)
    mu = 0.002588
    lam = 4.108225
    beta = 2.5
    delta = 0.020009
    B = 0.715517
    
    m_e_MeV = 0.51099895
    
    print("Frozen vacuum parameters:")
    print(f"  mu = {mu}, lam = {lam}, beta = {beta}, delta = {delta}, B = {B}\n")
    
    # --- Calculation for 6_1 knot (Candidate for 4th generation fermion) ---
    K_6 = 6
    C_61 = 9.0  # Proven via SymPy
    print(f"--- Generating Hamiltonian for 6_1 knot (K={K_6}, C={C_61}) ---")
    H_6 = build_hamiltonian(K_6, C_61, mu, beta, lam, delta, B)
    E0_6 = torch.linalg.eigvalsh(H_6)[0].real.item()
    mass_6_GeV = E0_6 * m_e_MeV / 1000.0
    print(f"Matrix dimension: {2**K_6}x{2**K_6}")
    print(f"Dimensionless energy E_0: {E0_6:.2f} m_e")
    print(f"Physical mass of 4th generation: {mass_6_GeV:.4f} GeV\n")
    
    # --- Calculation for 8_3 knot (Dark Matter Candidate) ---
    K_8 = 8
    C_83 = 17.0 # Proven via SymPy
    print(f"--- Generating Hamiltonian for 8_3 knot (DM) (K={K_8}, C={C_83}) ---")
    H_8 = build_hamiltonian(K_8, C_83, mu, beta, lam, delta, B)
    E0_8 = torch.linalg.eigvalsh(H_8)[0].real.item()
    mass_8_TeV = (E0_8 * m_e_MeV / 1000.0) / 1000.0
    
    print(f"Matrix dimension: {2**K_8}x{2**K_8}")
    print(f"Dimensionless energy E_0: {E0_8:.2f} m_e")
    print(f"Physical mass of Dark Matter: {mass_8_TeV * 1000:.2f} GeV ({mass_8_TeV:.3f} TeV)\n")