import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Извлекаем параметры из заголовка
    params = {}
    for line in lines[:20]:  # Читаем только заголовок
        if '#' in line and '=' in line:
            parts = line.split('#')[1].split('=')
            if len(parts) == 2:
                key = parts[0].strip()
                value = float(parts[1].strip().split()[0])
                params[key] = value
    
    # Извлекаем данные из таблицы
    data = []
    for line in lines[20:]:
        if line.strip() and not line.startswith('#'):
            values = list(map(float, line.split()))
            data.append(values)
    
    return params, np.array(data)

# Чтение данных
params, data = read_data('data.txt')

# Извлекаем необходимые параметры
mu_s = params.get('mu_s', 0.34883)  # 1/mm
mu_t = params.get('mu_t', 0.40662)  # 1/mm
density = params.get('density', 0.1)  # particles/um^3

# Расчет концентрации для 3-кратного усиления сигнала
# Для 3-кратного усиления нужно увеличить mu_s в 3 раза
target_mu_s = mu_s * 3
required_density = density * 3  # particles/um^3

# Пересчет в частицы на мм^3
required_density_mm3 = required_density * 1e9  # particles/mm^3

# Расчет сигналов в дБ
signal_original = 10 * np.log10(np.exp(-mu_t))  # дБ
signal_enhanced = 10 * np.log10(np.exp(-mu_t * 3))  # дБ

print(f"Требуемая концентрация частиц: {required_density_mm3:.2e} частиц/мм³")
print(f"Исходный сигнал: {signal_original:.2f} дБ")
print(f"Усиленный сигнал: {signal_enhanced:.2f} дБ")
print(f"Разница в сигнале: {signal_enhanced - signal_original:.2f} дБ")

# Построение графика углового распределения
theta = data[:, 0]
natural = data[:, 1]

plt.figure(figsize=(10, 6))
plt.polar(np.radians(theta), natural)
plt.title('Угловое распределение рассеяния')
plt.grid(True)
plt.show()
