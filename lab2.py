import numpy as np
import matplotlib.pyplot as plt
import re

def read_mie_parameters(filename):
    """Чтение параметров из файла результатов Mie Calculator"""
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            # Пропускаем комментарии и пустые строки
            if line.startswith('#') or not line.strip():
                continue
            
            # Ищем строки с параметрами
            match = re.match(r'#\s*(\w+)\s+([-+]?\d*\.\d+)\s+\[(.*?)\]\s+\((.*)\)', line)
            if match:
                param_name = match.group(1)
                param_value = float(match.group(2))
                params[param_name] = param_value
    
    return params

# Чтение параметров из файла
params = read_mie_parameters('data.txt')

# Извлечение необходимых параметров
Qsca = params.get('Qsca', 0.0)
Csca = params.get('Csca', 0.0)
mu_s = params.get('mu_s', 0.0)

# Толщина образца
L = 1.0  # [mm]

# Расчет усиления сигнала для 3-кратного увеличения
signal_enhancement = 3.0  # 3-кратное усиление
enhancement_dB = 10 * np.log10(signal_enhancement)

# Расчет ослабления сигнала из-за рассеяния
attenuation = np.exp(-mu_s * L)
attenuation_dB = 10 * np.log10(attenuation)

# Расчет общего регистрируемого сигнала
total_signal_dB = enhancement_dB + attenuation_dB

# Вывод результатов
print("Результаты расчетов:")
print(f"Qsca (коэффициент рассеяния): {Qsca:.5f}")
print(f"Csca (сечение рассеяния): {Csca:.7f} micron²")
print(f"mu_s (коэффициент рассеяния): {mu_s:.5f} 1/mm")
print(f"Усиление сигнала: {enhancement_dB:.2f} дБ")
print(f"Ослабление из-за рассеяния: {attenuation_dB:.2f} дБ")
print(f"Итоговый регистрируемый сигнал: {total_signal_dB:.2f} дБ")

# Визуализация результатов
plt.figure(figsize=(10, 6))
plt.bar(['Усиление', 'Ослабление', 'Итоговый сигнал'],
        [enhancement_dB, attenuation_dB, total_signal_dB],
        color=['green', 'red', 'blue'])
plt.title('Регистрируемые сигналы в дБ')
plt.ylabel('Уровень сигнала (дБ)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('signal_levels.png')
plt.close()

# Сохранение результатов в файл
with open('results.txt', 'w') as f:
    f.write("Результаты расчетов:\n")
    f.write(f"Qsca (коэффициент рассеяния): {Qsca:.5f}\n")
    f.write(f"Csca (сечение рассеяния): {Csca:.7f} micron²\n")
    f.write(f"mu_s (коэффициент рассеяния): {mu_s:.5f} 1/mm\n")
    f.write(f"Усиление сигнала: {enhancement_dB:.2f} дБ\n")
    f.write(f"Ослабление из-за рассеяния: {attenuation_dB:.2f} дБ\n")
    f.write(f"Итоговый регистрируемый сигнал: {total_signal_dB:.2f} дБ\n")
