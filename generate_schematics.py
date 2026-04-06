import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

# --- Академическая настройка стилей (как в LaTeX) ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 12
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['pdf.fonttype'] = 42

def draw_figure_1_continuum():
    print("Генерация Рисунка 1: Континуальный предел...")
    fig = plt.figure(figsize=(14, 5))
    
    # --- ПАНЕЛЬ 1: Дискретная сеть (Микроуровень) ---
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.set_axis_off()
    ax1.set_title(r"Discrete Spin Network ($j=1$)" + "\nPlanck Scale", fontsize=14, y=0.95)
    
    np.random.seed(42)
    nodes = np.random.rand(15, 3)
    # Рисуем узлы
    ax1.scatter(nodes[:,0], nodes[:,1], nodes[:,2], color='black', s=30)
    # Рисуем ребра и спины
    for i in range(15):
        for j in range(i+1, 15):
            if np.linalg.norm(nodes[i] - nodes[j]) < 0.45:
                # Линия связи
                ax1.plot([nodes[i,0], nodes[j,0]], [nodes[i,1], nodes[j,1]], [nodes[i,2], nodes[j,2]], color='gray', alpha=0.5, lw=1.5)
                # Вектор спина на ребре (случайное направление)
                mid = (nodes[i] + nodes[j]) / 2
                vec = (nodes[j] - nodes[i]) * np.random.choice([-1, 0, 1])
                if np.linalg.norm(vec) > 0:
                    ax1.quiver(mid[0], mid[1], mid[2], vec[0], vec[1], vec[2], length=0.15, color='red', arrow_length_ratio=0.5)

    # --- ПАНЕЛЬ 2: Переход (Усреднение) ---
    ax2 = fig.add_subplot(132)
    ax2.set_axis_off()
    ax2.annotate('', xy=(0.9, 0.5), xytext=(0.1, 0.5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=10))
    ax2.text(0.5, 0.55, r"Coarse-Graining ($\Lambda_{UV}$)", ha='center', va='bottom', fontsize=14)
    ax2.text(0.5, 0.45, r"Continuum Limit", ha='center', va='top', fontsize=14)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)

    # --- ПАНЕЛЬ 3: Непрерывное поле (Макроуровень) ---
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.set_axis_off()
    ax3.set_title(r"Continuous EFT Field $\vec{n}(x)$" + "\nFermi Scale", fontsize=14, y=0.95)
    
    # Рисуем изогнутую гладкую трубку
    t = np.linspace(0, 4, 100)
    x = t
    y = np.sin(t)
    z = np.cos(t/2)
    ax3.plot(x, y, z, lw=18, color='lightblue', alpha=0.6, solid_capstyle='round')
    
    # Рисуем гладкое векторное поле внутри трубки
    tv = np.linspace(0.2, 3.8, 8)
    xv = tv
    yv = np.sin(tv)
    zv = np.cos(tv/2)
    uv = np.ones_like(tv) * 0.5
    vv = np.cos(tv) * 0.5
    wv = -0.5 * np.sin(tv/2) * 0.5
    ax3.quiver(xv, yv, zv, uv, vv, wv, length=0.8, color='darkblue', lw=2, arrow_length_ratio=0.3)

    # Врезка с Target Space (Сфера S^2)
    ax_inset = fig.add_axes([0.85, 0.2, 0.12, 0.25]) # x, y, width, height
    ax_inset.set_axis_off()
    circle = patches.Circle((0.5, 0.5), 0.4, fill=False, color='black', lw=1.5)
    ellipse = patches.Ellipse((0.5, 0.5), 0.8, 0.2, fill=False, color='gray', lw=1, ls='--')
    ax_inset.add_patch(circle)
    ax_inset.add_patch(ellipse)
    ax_inset.annotate('', xy=(0.7, 0.7), xytext=(0.5, 0.5), arrowprops=dict(arrowstyle="->", color='blue', lw=2))
    ax_inset.plot(0.5, 0.5, 'ko', markersize=3)
    ax_inset.text(0.5, 0.0, r"Target Space $S^2$", ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig('continuum_limit.eps', format='eps', bbox_inches='tight')
    plt.savefig('continuum_limit.png', dpi=300, bbox_inches='tight')
    print("  -> Сохранено: continuum_limit.eps")

def draw_figure_2_confinement():
    print("Генерация Рисунка 2: Конфайнмент и Y-вершина...")
    fig = plt.figure(figsize=(12, 6))
    
    # --- ПАНЕЛЬ А: Свободный Лептон (Узел 3_1) ---
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_axis_off()
    ax1.set_title(r"A) Closed Topology ($Q_H \in \mathbb{Z}$)" + "\nAsymptotically Free Lepton", fontsize=14, y=0.95)
    
    # Параметрические уравнения узла 3_1 (Трилистник)
    t = np.linspace(0, 2*np.pi, 200)
    x = np.sin(t) + 2*np.sin(2*t)
    y = np.cos(t) - 2*np.cos(2*t)
    z = -np.sin(3*t)
    ax1.plot(x, y, z, lw=8, color='royalblue')
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_zlim(-3, 3)

    # --- ПАНЕЛЬ B: Адроны и Y-вершина (Конфайнмент) ---
    ax2 = fig.add_subplot(122)
    ax2.set_axis_off()
    ax2.set_title(r"B) Open Boundaries (Fractional $Q_H$)" + "\nAbsolute Linear Confinement", fontsize=14, y=0.95)
    
    # Координаты для Y-вершины (120 градусов)
    center = np.array([0, 0])
    angles = [np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3]
    colors = ['crimson', 'forestgreen', 'mediumblue'] # Намек на QCD
    L = 1.5
    
    for i, angle in enumerate(angles):
        end_pt = np.array([L*np.cos(angle), L*np.sin(angle)])
        # Рисуем "пружинистую" трубку потока
        ax2.plot([center[0], end_pt[0]], [center[1], end_pt[1]], lw=12, color=colors[i], alpha=0.5, solid_capstyle='round')
        # Силовая линия внутри
        ax2.annotate('', xy=center, xytext=end_pt*0.8, arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
        # Сингулярные концы (кварки)
        ax2.plot(end_pt[0], end_pt[1], 'ko', markersize=10, mfc='white', mew=2)
        # Дробные заряды
        ax2.text(end_pt[0]*1.2, end_pt[1]*1.2, r'$Q_H = \pm 1/3$', ha='center', va='center', fontsize=12, weight='bold')

    # Дуга 120 градусов
    arc = patches.Arc(center, 0.8, 0.8, theta1=90, theta2=210, color='black', lw=1.5, ls='--')
    ax2.add_patch(arc)
    ax2.text(-0.5, 0.4, r'$120^\circ$', fontsize=12)

    # Центральный монополь
    ax2.plot(center[0], center[1], 'ko', markersize=14)
    ax2.plot(center[0], center[1], 'wo', markersize=6)
    
    # Выноски и текст
    ax2.text(center[0]+0.2, center[1]+0.2, r"$\pi_2(S^2)$ Monopole" + "\n" + r"$\sum Q_H \in \mathbb{Z}$", 
             fontsize=11, bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))
    
    ax2.text(0.8, -0.2, r"Tension: $V(r) = \sigma \cdot r$", fontsize=13, color='black', rotation=-30)
    
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('confinement_y_junction.eps', format='eps', bbox_inches='tight')
    plt.savefig('confinement_y_junction.png', dpi=300, bbox_inches='tight')
    print("  -> Сохранено: confinement_y_junction.eps")

if __name__ == '__main__':
    draw_figure_1_continuum()
    draw_figure_2_confinement()
    print("Все академические схемы успешно сгенерированы!")