import math

class LatticeRegularizationBridge:
    """
    Mathematical bridge (Lattice Regularization) between the continuous O(3) Sigma model
    of Faddeev-Niemi and the discrete topological Hamiltonian.
    
    Continuous parameters (EFT):
    - v: Vacuum Expectation Value (VEV) -> Determines macroscopic tension M^2 = v^2
    - c2: Skyrme constant -> Determines topological rigidity 1/e^2 = 4 * c2 * v^4
    - q: Effective coordination number of the vacuum graph
    
    Discrete parameters (PyTorch):
    - mu: Base geometric tension per crossing
    - lambda_param: Topological coupling strength
    - beta: Entropic RG-flow parameter
    """
    def __init__(self, lattice_spacing=1.0):
        # a - Effective lattice scale (in natural units a = 1)
        self.a = lattice_spacing 
        
    def continuous_to_discrete(self, v, c2, q):
        """ Direct mapping: from continuous EFT to discrete graph """
        # 1. Entropic capacity (Shannon entropy of graph paths)
        beta = math.log(q)
        
        # 2. Base tension (mu) arises from the kinetic term M^2 = v^2
        # integrated over the lattice cell volume.
        mu = (v**2) * self.a
        
        # 3. Topological coupling (lambda) arises from the Skyrme term
        lambda_param = c2 * (v**4) * self.a
        
        return mu, lambda_param, beta
        
    def discrete_to_continuous(self, mu, lambda_param, beta):
        """ Inverse spectral problem: from PyTorch matrices to EFT physics """
        # 1. Effective coordination number of the vacuum
        q = math.exp(beta)
        
        # 2. Vacuum Expectation Value (v)
        v = math.sqrt(mu / self.a)
        
        # 3. Skyrme constant (c2)
        # lambda = c2 * v^4 * a  =>  c2 = lambda / (v^4 * a)
        c2 = lambda_param / ((v**4) * self.a)
        
        return v, c2, q

if __name__ == "__main__":
    print("=== Lattice Regularization: From Discrete Hamiltonian to Continuum Limit ===\n")
    
    # Optimal parameters found in run_calibration.py
    mu_opt = 0.002588
    lambda_opt = 4.108225
    beta_opt = 2.5
    
    bridge = LatticeRegularizationBridge()
    v, c2, q = bridge.discrete_to_continuous(mu_opt, lambda_opt, beta_opt)
    
    print(f"Calculated parameters of the macroscopic vacuum (Faddeev-Niemi Model):")
    print(f"  Effective coordination number of the graph (q) : {q:.2f} (degrees of freedom per node)")
    print(f"  Vacuum expectation value (v)                 : {v:.6f} (in natural units)")
    print(f"  Skyrme constant (c2)                         : {c2:.2f}")
    print(f"  -> Macroscopic tension (M^2 = v^2)           : {v**2:.6f}")
    print(f"  -> Topological rigidity (1/e^2)              : {4.0 * c2 * (v**4):.2f}\n")