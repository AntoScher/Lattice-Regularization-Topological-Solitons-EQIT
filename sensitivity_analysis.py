import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# Настройки для академических графиков
plt.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

class FastTopologicalHamiltonian:
    """Упрощенная версия Гамильтониана для быстрых расчетов Монте-Карло"""
    def __init__(self, mu, beta, lam, delta, B):
        self.mu = mu
        self.beta = beta
        self.lam = lam
        self.delta = delta
        self.B = B
        
    def get_ground_state(self, K, C):
        N = 2**K
        H = torch.zeros((N, N), dtype=torch.complex128)
        
        # Диагональ
        C_tensor = torch.ones(N, dtype=torch.float64)
        C_tensor[0] = C
        C_tensor[-1] = C
        
        tension = self.mu * np.exp(self.beta * K)
        diag_energies = (tension * K - self.lam * C_tensor).to(torch.complex128)
        diag_indices = torch.arange(N)
        H[diag_indices, diag_indices] = diag_energies
        
        # Туннелирование
        i = torch.arange(N).view(N, 1)
        j = torch.arange(N).view(1, N)
        xor_matrix = torch.bitwise_xor(i, j)
        is_power_of_2 = (torch.bitwise_and(xor_matrix, xor_matrix - 1) == 0) & (xor_matrix != 0)
        H[is_power_of_2] = -self.delta / float(K)
                
        # Нарушение четности
        for idx in range(N // 2):
            mirror_idx = (N - 1) - idx
            H[idx, mirror_idx] = 1j * self.B
            H[mirror_idx, idx] = -1j * self.B
            
        eigenvalues = torch.linalg.eigvalsh(H)
        return eigenvalues[0].item()

def run_monte_carlo():
    print("=== EQIT Sensitivity Analysis (Monte Carlo) ===")
    print("Проверка устойчивости предсказания массы Тау-лептона к флуктуациям вакуума...\n")
    
    # Оптимальные параметры (Ground Truth)
    mu_opt = 0.002588
    lam_opt = 4.108225
    beta_opt = 2.5
    delta_opt = 0.020009
    B_opt = 0.715517
    
    m_e_exp = 0.510998
    m_tau_exp = 1776.86
    
    N_samples = 5000
    noise_level = 0.002 # Введение 0.2% структурного шума (типично для эффективных теорий)
    
    np.random.seed(42)
    mu_samples = np.random.normal(mu_opt, mu_opt * noise_level, N_samples)
    lam_samples = np.random.normal(lam_opt, lam_opt * noise_level, N_samples)
    
    predicted_tau_masses = []
    
    print(f"Генерация {N_samples} состояний вакуума с {noise_level*100}% дисперсией параметров mu и lambda...")
    
    for i in range(N_samples):
        model = FastTopologicalHamiltonian(mu=mu_samples[i], beta=beta_opt, lam=lam_samples[i], delta=delta_opt, B=B_opt)
        
        E_e = model.get_ground_state(3, 3.0)   # 3_1
        E_tau = model.get_ground_state(5, 7.0) # 5_2
        
        # Защита от коллапса вакуума (исключаем тахионные состояния)
        if E_e > 0.01:
            m_tau_calc = (E_tau / E_e) * m_e_exp
            predicted_tau_masses.append(m_tau_calc)
        
        if (i+1) % 1000 == 0:
            print(f"  Обраработано {i+1}/{N_samples} итераций...")
            
    predicted_tau_masses = np.array(predicted_tau_masses)
    
    mean_tau = np.mean(predicted_tau_masses)
    std_tau = np.std(predicted_tau_masses)
    
    print(f"\n--- Результаты Монте-Карло ---")
    print(f"Экспериментальная масса Тау : {m_tau_exp} MeV")
    print(f"Среднее предсказание модели : {mean_tau:.2f} MeV")
    print(f"Стандартное отклонение (1σ) : {std_tau:.2f} MeV")
    
    # Построение графика
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(predicted_tau_masses, bins=50, color='royalblue', alpha=0.7, edgecolor='black', density=True)
    ax.axvline(m_tau_exp, color='red', linestyle='dashed', linewidth=2.5, label=f'Experimental Target ({m_tau_exp:.1f} MeV)')
    ax.axvline(mean_tau, color='black', linestyle='solid', linewidth=2, label=f'Model Mean ({mean_tau:.1f} MeV)')
    
    ax.set_title('Monte Carlo Sensitivity Analysis: Topological Tau Mass Prediction\n(0.2% structural noise in vacuum parameters $\mu, \lambda$)', fontsize=14)
    ax.set_xlabel(r'Predicted Tau Mass $m_\tau$ (MeV)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, ls=':', alpha=0.7)
    
    plt.savefig('tau_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    print("График успешно сохранен: tau_sensitivity_analysis.png")

if __name__ == "__main__":
    run_monte_carlo()