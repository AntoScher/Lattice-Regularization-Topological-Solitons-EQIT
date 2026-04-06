import sympy as sp

def verify_invariant(knot_name, poly_expr, t):
    """Строгое алгебраическое вычисление топологических инвариантов узла"""
    print(f"--- Топологический анализ: Узел {knot_name} ---")
    print(f"Полином Александера: Δ(t) = {poly_expr}")
    
    # 1. Вычисление Детерминанта узла (Оценка топологического штрафа C)
    # Математическое определение: C = |Δ(-1)|
    det_expr = poly_expr.subs(t, -1)
    determinant = abs(det_expr)
    
    # 2. Оценка алгебраических корней (Анализ стабильности вакуума)
    roots = sp.solve(poly_expr, t)
    real_roots = [sp.N(r, 3) for r in roots if r.is_real]
    
    print(f"Строгий Детерминант C = |Δ(-1)| : {determinant}")
    print(f"Вещественные корни (t_c)         : {real_roots}\n")
    return determinant

if __name__ == "__main__":
    t = sp.Symbol('t')
    
    print("=== EQIT Phase 2: Строгий расчет инвариантов высших порядков (SymPy) ===\n")
    
    # --- Сектор K=6 (Кандидаты в тяжелые фермионы 4-го поколения) ---
    # 6_1 (Stevedore knot) - Амфихиральный
    poly_6_1 = 2*t - 5 + 2*t**(-1)
    verify_invariant("6_1 (Амфихиральный)", poly_6_1, t)
    
    # 6_3 - Амфихиральный
    poly_6_3 = t**2 - 3*t + 5 - 3*t**(-1) + t**(-2)
    verify_invariant("6_3 (Амфихиральный)", poly_6_3, t)
    
    # --- Сектор K=8 (Кандидат в Темную Материю) ---
    # 8_3 - Амфихиральный
    poly_8_3 = 4*t - 9 + 4*t**(-1)
    verify_invariant("8_3 (Амфихиральный, ТМ)", poly_8_3, t)