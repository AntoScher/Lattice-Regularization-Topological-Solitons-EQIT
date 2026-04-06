import torch

class TopologicalHamiltonian:
    def __init__(self):
        # Alexander polynomial coefficients for fundamental knots (generations)
        # Format: {degree_t: coefficient}
        self.alexander_coeffs = {
            '3_1': {1: 1, 0: -1, -1: 1},               # Electron
            '4_1': {1: -1, 0: 3, -1: -1},              # Muon
            '5_1': {2: 1, 1: -1, 0: 1, -1: -1, -2: 1}, # Degenerate with muon (C=5)
            '5_2': {1: 2, 0: -3, -1: 2}                # Tau-lepton
        }

    def calculate_determinant(self, knot_type):
        """
        Strict mathematical calculation of the knot determinant |Δ(-1)|.
        Replaces empirical fitting (hardcode) with first-principles calculation.
        """
        if knot_type not in self.alexander_coeffs:
            raise ValueError(f"Unknown knot type: {knot_type}")
            
        coeffs = self.alexander_coeffs[knot_type]
        poly_val = sum(c * ((-1) ** p) for p, c in coeffs.items())
        return float(abs(poly_val))

    def get_invariant_tensor(self, K, knot_type, phase_A=None):
        """
        Dynamically generates the vector of topological invariants C_i.
        """
        states = 2**K
        tensor = torch.ones(states, dtype=torch.float64)
        
        # Calculate strict invariant (determinant) on the fly
        base_inv = self.calculate_determinant(knot_type)
            
        # Assign invariant to full mirror states (all zeros or all ones)
        tensor[0] = base_inv
        tensor[-1] = base_inv
        return tensor

    def build_hamiltonian(self, K, knot_type, mu, beta, lam, delta, B):
        """
        Universal discrete Hamiltonian generator for any knot of complexity K.
        Uses PyTorch tensor operations for dynamic creation of 2^K x 2^K matrices.
        """
        N = 2**K
        # Initialize a clean complex matrix of zeros
        H = torch.zeros((N, N), dtype=torch.complex128, device=mu.device)
        
        # 1. Diagonal: Exponential RG-flow + Strict Topology
        C_array = self.get_invariant_tensor(K, knot_type).to(mu.device)
        tension = mu * torch.exp(beta * float(K))
        diag_energies = (tension * float(K) - lam * C_array).to(torch.complex128)
        diag_indices = torch.arange(N)
        H[diag_indices, diag_indices] = diag_energies
        
        # 2. Off-diagonal elements (Tunneling) - Dynamic Hamming neighbor search
        i = torch.arange(N).view(N, 1)
        j = torch.arange(N).view(1, N)
        xor_matrix = torch.bitwise_xor(i, j)
        is_power_of_2 = (torch.bitwise_and(xor_matrix, xor_matrix - 1) == 0) & (xor_matrix != 0)
        d = (-delta / float(K)).to(torch.complex128)
        H[is_power_of_2] = d
                
        # 3. Parity violation (Complex coupling of mirror states)
        for idx in range(N // 2):
            mirror_idx = (N - 1) - idx
            H[idx, mirror_idx] = 1j * B.to(torch.complex128)
            H[mirror_idx, idx] = -1j * B.to(torch.complex128)
            
        return H

# --- Usage example (forward pass) ---
if __name__ == "__main__":
    # Set parameters as PyTorch tensors
    mu = torch.tensor(1.0, requires_grad=True)
    beta = torch.tensor(0.5, requires_grad=True)
    lam = torch.tensor(0.5, requires_grad=True)
    delta = torch.tensor(0.1, requires_grad=True)
    B = torch.tensor(0.05, requires_grad=True)
    
    model = TopologicalHamiltonian()
    H = model.build_hamiltonian(3, '3_1', mu, beta, lam, delta, B)
    H4 = model.build_hamiltonian(4, '4_1', mu, beta, lam, delta, B)
    
    # Calculate eigenvalues
    ev_31, _ = torch.linalg.eigh(H)
    ev_41, _ = torch.linalg.eigh(H4)
    
    print("Hermitian Hamiltonian matrix 3_1 successfully built.")
    print(f"Spectrum 3_1 (first 3 levels): {ev_31[:3].detach().real.numpy()}")
    print(f"Electron mass E_0(3_1): {ev_31[0].detach().real.item():.4f}\n")
    
    print("Hermitian Hamiltonian matrix 4_1 successfully built.")
    print(f"Spectrum 4_1 (first 3 levels): {ev_41[:3].detach().real.numpy()}")
    print(f"Muon mass E_0(4_1): {ev_41[0].detach().real.item():.4f}")