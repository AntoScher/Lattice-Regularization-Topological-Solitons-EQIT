import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

# Import our strict mathematical Hamiltonian generator
from topological_hamiltonian import TopologicalHamiltonian

# =====================================================================
# 1. Physical Parameters Module with constraints
# =====================================================================
class TopologicalParameters(nn.Module):
    def __init__(self, lambda_max=5.0):
        super().__init__()
        # "Warm start": initialization closer to the physical basin of attraction
        self.tilde_mu = nn.Parameter(torch.tensor(-1.2, dtype=torch.float64))     # -> mu ~ 0.003
        self.tilde_lambda = nn.Parameter(torch.tensor(1.2, dtype=torch.float64))  # -> lam ~ 4.16
        
        self.lambda_max = lambda_max

    @property
    def mu(self):
        return 0.01 * torch.exp(self.tilde_mu) # mu > 0, scaling down
        
    @property
    def beta(self):
        # PHENOMENOLOGICAL CONSTRAINT: Rational critical index 5/2 (polymer statistics)
        return torch.tensor(2.5, dtype=torch.float64, device=self.tilde_mu.device)

    @property
    def lambda_param(self):
        return self.lambda_max * torch.tanh(self.tilde_lambda) # |lambda| < lambda_max

    @property
    def delta(self):
        # FUNDAMENTAL CONSTANT: Phenomenological tunneling phase.
        # Derived from prior lower-dimensional Chern-Simons approximations (level k=155).
        # Kept frozen here to prevent over-parameterization of the inverse problem.
        return torch.tensor(0.020009, dtype=torch.float64, device=self.tilde_mu.device)
        
    @property
    def B(self):
        # PERTURBATIVE DERIVATION: Dynamic generation of parity violation phase.
        # Derived perturbatively as B_0 = (delta^2 / 9) * (3 / lambda).
        B_0 = (self.delta**2 / 9.0) * (3.0 / self.lambda_param)
        # Macroscopic amplification via amphichiral condensate 4_1
        return B_0 * torch.exp(self.beta * 4.0)

# =====================================================================
# 1.1 Generation of strict topological weights C_i (Determinants)
# =====================================================================
def generate_topological_weights(K: int) -> torch.Tensor:
    """
    Dynamically request strict invariants from the Hamiltonian generator,
    excluding any manual fitting (hardcode).
    """
    topo_ham = TopologicalHamiltonian()
    knot_map = {3: '3_1', 4: '4_1', 5: '5_2'}
    knot_type = knot_map[K]
    return topo_ham.get_invariant_tensor(K, knot_type)

# =====================================================================
# 2. Hamiltonian Assembly (Exact hypercube algebra)
# =====================================================================
def build_hamiltonian(K: int, mu: torch.Tensor, beta: torch.Tensor, lambda_param: torch.Tensor, delta: torch.Tensor, B: torch.Tensor, C_array: torch.Tensor) -> torch.Tensor:
    N = 2**K
    # Initialize a clean complex matrix of zeros
    H = torch.zeros((N, N), dtype=torch.complex128, device=mu.device)
    
    i = torch.arange(N).view(N, 1)
    j = torch.arange(N).view(1, N)
    
    # 1. Tunneling (off-diagonal elements)
    xor_matrix = torch.bitwise_xor(i, j)
    is_power_of_2 = (torch.bitwise_and(xor_matrix, xor_matrix - 1) == 0) & (xor_matrix != 0)
    d = (-delta / float(K)).to(torch.complex128)
    H[is_power_of_2] = d
    
    # 2. Parity violation (Complex coupling of mirror states)
    for idx in range(N // 2):
        mirror_idx = (N - 1) - idx
        H[idx, mirror_idx] = H[idx, mirror_idx] + 1j * B.to(torch.complex128)
        H[mirror_idx, idx] = H[mirror_idx, idx] - 1j * B.to(torch.complex128)
    
    # 3. Diagonal: Exponential RG-flow + Topology
    tension = mu * torch.exp(beta * float(K))
    diag_energies = (tension * float(K) - lambda_param * C_array.to(mu.device)).to(torch.complex128)
    diag_indices = torch.arange(N)
    H[diag_indices, diag_indices] = H[diag_indices, diag_indices] + diag_energies
    
    return H

# =====================================================================
# 3. Loss Function (Calibration + Stability)
# =====================================================================
def compute_loss(H_e, H_mu, beta_neg=1000.0):
    eigvals_e = torch.linalg.eigvalsh(H_e)
    eigvals_mu = torch.linalg.eigvalsh(H_mu)
    
    # Matrix is Hermitian, eigenvalues are real, take .real
    E0_e = eigvals_e[0].real
    E0_mu = eigvals_mu[0].real
    
    # 1. Anchor: Electron mass must be 1.0 (sets the energy scale)
    loss_e_scale = ((E0_e - 1.0) / 1.0)**2
    
    # 2. Full lepton sector calibration: Relative squared error
    mass_ratio_mu = E0_mu / E0_e
    loss_mu_ratio = ((mass_ratio_mu - 206.768) / 206.768)**2
    
    # Protection against tachyons (E0 < 0)
    penalty_tachyon = beta_neg * (F.relu(-E0_e)**2 + F.relu(-E0_mu)**2)
    
    total_loss = loss_e_scale + loss_mu_ratio + penalty_tachyon
    return total_loss, mass_ratio_mu

# =====================================================================
# 4. Two-stage optimization loop
# =====================================================================
if __name__ == "__main__":
    print("=== Start Sub-stage 1.1: Vacuum Calibration ===")
    # Strict weights generation
    C_array_e = generate_topological_weights(3)
    C_array_mu = generate_topological_weights(4)
    
    model = TopologicalParameters()
    
    # Use multi-rate step, as in the verified optimize_mass_ratio.py
    optimizer = torch.optim.Adam([
        {'params': [model.tilde_mu], 'lr': 0.005},
        {'params': [model.tilde_lambda], 'lr': 0.05}
    ])
    
    for epoch in range(2001): # Reduced preliminary Adam phase
        optimizer.zero_grad()
        
        H_e = build_hamiltonian(3, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_e)
        H_mu = build_hamiltonian(4, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_mu)
        
        loss, r_mu = compute_loss(H_e, H_mu)
        loss.backward()
        optimizer.step()
        
        if epoch % 500 == 0 or epoch == 2000:
            print(f"Epoch {epoch:4d} | Loss: {loss.item():10.8f} | M_mu: {r_mu.item():8.2f}")
            print(f"       Params -> mu: {model.mu.item():.6f}, beta: {model.beta.item():.6f}, lam: {model.lambda_param.item():.6f}, delta: {model.delta.item():.6f}, B: {model.B.item():.6f}\n")

    # === PHASE 2: L-BFGS (Hessian descent to absolute minimum) ===
    print("=== Launch L-BFGS for ultra-precise fine-tuning (Second-Order Method) ===")
    optimizer_lbfgs = torch.optim.LBFGS(model.parameters(), lr=0.5, max_iter=20, tolerance_grad=1e-9, tolerance_change=1e-9, line_search_fn='strong_wolfe')
    
    def closure():
        optimizer_lbfgs.zero_grad()
        H_e = build_hamiltonian(3, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_e)
        H_mu = build_hamiltonian(4, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_mu)
        loss, _ = compute_loss(H_e, H_mu)
        loss.backward()
        return loss

    for step in range(15):
        loss_val = optimizer_lbfgs.step(closure)
        
        with torch.no_grad():
            H_e = build_hamiltonian(3, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_e)
            H_mu = build_hamiltonian(4, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_mu)
            l_val, r_mu = compute_loss(H_e, H_mu)
            
        print(f"L-BFGS Step {step:2d} | Loss: {l_val.item():10.8e} | M_mu: {r_mu.item():8.2f}")
        if l_val.item() < 1e-10:
            print("Perfect L-BFGS convergence achieved!\n")
            break
            
    print(f"FINAL Params -> mu: {model.mu.item():.6f}, beta: {model.beta.item():.6f}, lam: {model.lambda_param.item():.6f}, delta: {model.delta.item():.6f}, B: {model.B.item():.6f}\n")

    # =====================================================================
    # Sub-stage 1.2: Blind Predictive Test for tau-lepton mass
    # =====================================================================
    print("\n=== Sub-stage 1.2: Blind predictive test of tau-lepton mass (Knot 5_2, K=5) ===")
    
    with torch.no_grad(): # DISABLE GRADIENTS! No fitting!
        # 1. Get final electron mass for ratio calculation
        H_e_final = build_hamiltonian(3, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_e)
        E0_e_final = torch.linalg.eigvalsh(H_e_final)[0].real
        
        # 2. Build 5_2 Hamiltonian with frozen parameters
        C_array_tau = generate_topological_weights(5)
        H_tau = build_hamiltonian(5, model.mu, model.beta, model.lambda_param, model.delta, model.B, C_array_tau)
        E0_tau = torch.linalg.eigvalsh(H_tau)[0].real
        
        mass_ratio_tau = (E0_tau / E0_e_final).item()
        m_tau_pred = mass_ratio_tau * 0.510998
        m_tau_exp = 1776.86
        error = abs(m_tau_pred - m_tau_exp) / m_tau_exp * 100
        
        print(f"Predicted Tau mass:                          {m_tau_pred:.2f} MeV")
        print(f"Experimental value (CODATA):                 {m_tau_exp:.2f} MeV")
        print(f"Prediction error:                            {error:.2f}%\n")