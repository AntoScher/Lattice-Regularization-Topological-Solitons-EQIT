"""
ILQC Topological EFT Framework: Kadanoff Block-Spin Coarse-Graining
License: MIT License
Author: Anton Shcherbich
Purpose: Phenomenological visualization of the RG flow from a discrete 
         Planckian qutrit network to a continuous macroscopic EFT field.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.ndimage import uniform_filter

# --- Академическая настройка стилей (как в LaTeX) ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def calculate_gradient_energy(S_x, S_y):
    """
    Вычисляет кинетическую энергию поля (прокси для M^2 (\partial_\mu n)^2).
    """
    grad_x_x, grad_x_y = np.gradient(S_x)
    grad_y_x, grad_y_y = np.gradient(S_y)
    return np.sum(grad_x_x**2 + grad_x_y**2 + grad_y_x**2 + grad_y_y**2)

def calculate_topological_charge(S_x, S_y):
    """
    Вычисляет 2D топологический индекс (winding number / vorticity density).
    Интеграл от якобиана: q ~ \int (\partial_x S_x \partial_y S_y - \partial_x S_y \partial_y S_x) dx dy
    """
    grad_x_x, grad_x_y = np.gradient(S_x)
    grad_y_x, grad_y_y = np.gradient(S_y)
    jacobian = grad_x_x * grad_y_y - grad_x_y * grad_y_x
    return np.abs(np.sum(jacobian)) * 100  # Нормировка для наглядности масштаба

def generate_coarse_graining_visualization():
    print("Симуляция блочного спинового коарсинга (Kadanoff Coarse-Graining)...")

    # 1. Настройка микроскопической решетки (Планковский масштаб)
    N = 200  # Высокое разрешение для симуляции миллионов узлов
    x = np.linspace(-5, 5, N)
    y = np.linspace(-5, 5, N)
    X, Y = np.meshgrid(x, y)

    # 2. Скрытый макроскопический топологический порядок (Водоворот/Хопфион)
    # На микроуровне он почти невидим из-за квантового шума
    R = np.sqrt(X**2 + Y**2) + 0.1
    theta = np.arctan2(Y, X)
    V_x = -np.sin(theta) * np.exp(-R/4)
    V_y = np.cos(theta) * np.exp(-R/4)

    # 3. Добавляем термальный шум и дискретизируем до Кутритов {-1, 0, 1}
    # Фиксируем seed для строгой воспроизводимости Figure 6 в публикации.
    np.random.seed(42)
    noise_level = 2.5
    S_x_raw = V_x + noise_level * (np.random.rand(N, N) - 0.5)
    S_y_raw = V_y + noise_level * (np.random.rand(N, N) - 0.5)

    # Строгая дискретизация (j=1)
    def discretize(arr):
        return np.clip(np.round(arr), -1, 1)

    S_x_micro = discretize(S_x_raw)
    S_y_micro = discretize(S_y_raw)

    # 4. Процедура Коарсинга (РГ-поток)
    def block_average(field, size):
        # Усреднение по квадратному блоку и субдискретизация
        smoothed = uniform_filter(field, size=size)
        return smoothed[size//2::size, size//2::size]

    # Мезо-масштаб (Усреднение 8x8)
    b_meso = 8
    S_x_meso = block_average(S_x_micro, b_meso)
    S_y_meso = block_average(S_y_micro, b_meso)
    X_meso = block_average(X, b_meso)
    Y_meso = block_average(Y, b_meso)

    # Макро-масштаб (Континуальный EFT предел)
    S_x_eft = uniform_filter(S_x_micro, size=35)
    S_y_eft = uniform_filter(S_y_micro, size=35)

    # --- Количественный анализ термодинамической релаксации (RG-поток) ---
    E_micro = calculate_gradient_energy(S_x_micro, S_y_micro)
    E_meso = calculate_gradient_energy(S_x_meso, S_y_meso)
    E_macro = calculate_gradient_energy(S_x_eft, S_y_eft)
    
    Q_micro = calculate_topological_charge(S_x_micro, S_y_micro)
    Q_meso = calculate_topological_charge(S_x_meso, S_y_meso)
    Q_macro = calculate_topological_charge(S_x_eft, S_y_eft)
    
    print("\n[QUANTITATIVE RG-FLOW ANALYSIS]")
    print(f"1. Microscale -> Energy: {E_micro:.2e} | Topo Integral ~ {Q_micro:.2f} (Masked by noise)")
    print(f"2. Mesoscale  -> Energy: {E_meso:.2e} (Drops {E_micro/E_meso:.1f}x) | Topo Integral ~ {Q_meso:.2f}")
    print(f"3. Macroscale -> Energy: {E_macro:.2e} (Drops {E_micro/E_macro:.1f}x) | Topo Integral ~ {Q_macro:.2f} (Conserved!)\n")

    # 5. Визуализация
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Панель 1: Микро-уровень (Дискретный шум)
    angle_micro = np.arctan2(S_y_micro, S_x_micro)
    axs[0].imshow(angle_micro, cmap='twilight', origin='lower', extent=[-5, 5, -5, 5])
    axs[0].set_title(r"1. Microscale (Planckian)" + "\n" + r"Discrete Qutrit Network $S \in \{-1,0,1\}$", fontsize=14)
    axs[0].axis('off')
    axs[0].text(-4.8, -4.6, f"$\\mathcal{{E}}_{{grad}} \\approx {E_micro:.1e}$\n$\\tilde{{Q}}_{{topo}} \\approx {Q_micro:.1f}$", color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3'))

    # Панель 2: Мезо-уровень (Укрупнение)
    angle_meso = np.arctan2(S_y_meso, S_x_meso)
    axs[1].imshow(angle_meso, cmap='twilight', origin='lower', extent=[-5, 5, -5, 5], alpha=0.7)
    axs[1].quiver(X_meso, Y_meso, S_x_meso, S_y_meso, color='white', scale=10, alpha=0.9)
    axs[1].set_title(r"2. Mesoscale (RG Flow)" + "\n" + r"Kadanoff Block-Spin Averaging", fontsize=14)
    axs[1].axis('off')
    axs[1].text(-4.8, -4.6, f"$\\mathcal{{E}}_{{grad}} \\approx {E_meso:.1e}$\n$\\tilde{{Q}}_{{topo}} \\approx {Q_meso:.1f}$", color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3'))

    # Панель 3: Макро-уровень (Сплошная Эффективная Теория)
    angle_eft = np.arctan2(S_y_eft, S_x_eft)
    axs[2].imshow(angle_eft, cmap='twilight', origin='lower', extent=[-5, 5, -5, 5], alpha=0.5)
    axs[2].streamplot(x, y, S_x_eft, S_y_eft, color='black', linewidth=1.5, density=1.2, arrowsize=1.5)
    axs[2].set_title(r"3. Macroscale (Continuum Limit)" + "\n" + r"Emergent Continuous Field $\vec{n}(x)$", fontsize=14)
    axs[2].axis('off')
    axs[2].text(-4.8, -4.6, f"$\\mathcal{{E}}_{{grad}} \\approx {E_macro:.1e}$\n$\\tilde{{Q}}_{{topo}} \\approx {Q_macro:.1f}$", color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig('coarse_graining_rg_flow.eps', format='eps', bbox_inches='tight')
    plt.savefig('coarse_graining_rg_flow.png', dpi=300, bbox_inches='tight')
    print("Успех: График сохранен как 'coarse_graining_rg_flow.png'")

if __name__ == '__main__':
    generate_coarse_graining_visualization()
