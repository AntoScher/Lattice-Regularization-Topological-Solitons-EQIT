import sympy as sp

def get_knot_determinant(knot_name, poly_expr, t):
    """Calculates the knot determinant C = |Delta(-1)|"""
    # Substitute fermionic limit t = -1
    det = abs(poly_expr.subs(t, -1))
    print(f"Knot {knot_name}:")
    print(f"  Alexander Polynomial Delta(t) = {poly_expr}")
    print(f"  Determinant C = |Delta(-1)|  = {det}\n")
    return det

if __name__ == "__main__":
    t = sp.Symbol('t')
    
    print("=== Strict algebraic calculation of knot invariants (C_i) ===\n")
    
    # 1st generation (Electron) - Trefoil 3_1
    poly_3_1 = t - 1 + t**-1
    get_knot_determinant("3_1 (Electron)", poly_3_1, t)
    
    # 2nd generation (Muon) - Figure-eight 4_1
    poly_4_1 = t - 3 + t**-1
    get_knot_determinant("4_1 (Muon)", poly_4_1, t)
    
    # 3rd generation (Tau) - Candidate 1: Cinquefoil 5_1
    poly_5_1 = t**2 - t + 1 - t**-1 + t**-2
    get_knot_determinant("5_1 (Degenerate candidate)", poly_5_1, t)
    
    # 3rd generation (Tau) - Candidate 2: Three-twist knot 5_2
    poly_5_2 = 2*t - 3 + 2*t**-1
    get_knot_determinant("5_2 (Tau-lepton)", poly_5_2, t)