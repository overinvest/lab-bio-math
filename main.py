import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Annulus
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')

def generate_photon_coordinates(N, a1, a2):
    """
    Generate N random photon coordinates in an annular region with inner radius a1 and outer radius a2.
    The distribution is uniform in area (constant probability density).
    
    Args:
        N: Number of photons
        a1: Inner radius
        a2: Outer radius
    
    Returns:
        x, y: Arrays of x and y coordinates
    """
    # Generate random angles uniformly between 0 and 2π
    theta = np.random.uniform(0, 2*np.pi, N)
    
    # Generate random radii with proper weighting for uniform area distribution
    # For uniform distribution in area, we need r ~ sqrt(r1² + u*(r2² - r1²))
    u = np.random.uniform(0, 1, N)
    r = np.sqrt(a1**2 + u*(a2**2 - a1**2))
    
    # Convert to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    return x, y

def plot_photon_distribution(x, y, a1, a2, bins=50):
    """
    Plot the photon distribution and compare with analytical curve.
    
    Args:
        x, y: Arrays of photon coordinates
        a1, a2: Inner and outer radii
        bins: Number of bins for histogram
    """
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Scatter plot of photon positions
    ax1.scatter(x, y, s=1, alpha=0.5, color='blue')
    ax1.add_patch(plt.Circle((0, 0), a1, fill=False, color='red', linestyle='--'))
    ax1.add_patch(plt.Circle((0, 0), a2, fill=False, color='red', linestyle='--'))
    ax1.set_aspect('equal')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Распределение фотонов')
    ax1.grid(True)
    
    # Plot 2: Radial distribution
    r = np.sqrt(x**2 + y**2)
    
    # Calculate histogram of radial distribution
    hist, bin_edges = np.histogram(r, bins=bins, range=(0, a2*1.1))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]
    
    # Normalize histogram by area of each annular bin
    # The area of each bin is approximately 2πr·dr
    hist_normalized = hist / (2 * np.pi * bin_centers * bin_width)
    
    # Plot histogram
    ax2.bar(bin_centers, hist_normalized, width=bin_width, alpha=0.5, label='Численная модель')
    
    # Plot analytical curve (constant in [a1, a2], zero elsewhere)
    r_analytical = np.linspace(0, a2*1.1, 1000)
    analytical = np.zeros_like(r_analytical)
    mask = (r_analytical >= a1) & (r_analytical <= a2)
    
    # Set constant value in the range [a1, a2]
    # Normalize to match histogram height
    if np.any(mask):
        analytical[mask] = np.mean(hist_normalized[(bin_centers >= a1) & (bin_centers <= a2)])
    
    ax2.plot(r_analytical, analytical, 'r-', linewidth=2, label='Аналитическая модель')
    
    ax2.set_xlabel('Радиус r')
    ax2.set_ylabel('Плотность распределения p(r)')
    ax2.set_title('Сечение плотности распределения')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    return fig

class PhotonGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор фотонов в осесимметричном пучке")
        self.root.geometry("1200x800")
        
        # Create frame for inputs
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Create widgets
        ttk.Label(input_frame, text="Количество фотонов (N):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.N_var = tk.StringVar(value="10000")
        ttk.Entry(input_frame, textvariable=self.N_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Внутренний радиус (a₁):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.a1_var = tk.StringVar(value="2.0")
        ttk.Entry(input_frame, textvariable=self.a1_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Внешний радиус (a₂):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.a2_var = tk.StringVar(value="5.0")
        ttk.Entry(input_frame, textvariable=self.a2_var, width=10).grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Сгенерировать", command=self.generate).grid(row=0, column=6, padx=20, pady=5)
        ttk.Button(input_frame, text="Сохранить в файл", command=self.save_to_file).grid(row=0, column=7, padx=5, pady=5)
        
        # Frame for the plots
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize with default values
        self.x = None
        self.y = None
        self.generate()
    
    def generate(self):
        try:
            N = int(self.N_var.get())
            a1 = float(self.a1_var.get())
            a2 = float(self.a2_var.get())
            
            if N <= 0:
                self.status_var.set("Ошибка: Количество фотонов должно быть положительным")
                return
                
            if a1 >= a2:
                self.status_var.set("Ошибка: Внутренний радиус должен быть меньше внешнего")
                return
                
            if a1 < 0:
                self.status_var.set("Ошибка: Радиусы должны быть положительными")
                return
            
            # Generate photon coordinates
            self.x, self.y = generate_photon_coordinates(N, a1, a2)
            
            # Clear previous plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            
            # Create new plot
            fig = plot_photon_distribution(self.x, self.y, a1, a2)
            
            # Embed plot in tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set(f"Сгенерировано {N} фотонов в кольце радиусом от {a1} до {a2}")
            
        except ValueError as e:
            self.status_var.set(f"Ошибка ввода: {str(e)}")
    
    def save_to_file(self):
        if self.x is None or self.y is None:
            self.status_var.set("Ошибка: Сначала сгенерируйте данные")
            return
            
        output_file = 'photon_coordinates.txt'
        np.savetxt(output_file, np.column_stack((self.x, self.y)), header='X Y', comments='')
        self.status_var.set(f"Координаты фотонов сохранены в файл {output_file}")


def main():
    # If run from command line with arguments
    import sys
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description='Генерация распределения фотонов в пучке')
        parser.add_argument('-N', type=int, default=10000, help='Количество фотонов')
        parser.add_argument('-a1', type=float, default=2.0, help='Внутренний радиус')
        parser.add_argument('-a2', type=float, default=5.0, help='Внешний радиус')
        args = parser.parse_args()
        
        print(f"Генерация {args.N} фотонов в кольце радиусом от {args.a1} до {args.a2}")
        
        # Generate photon coordinates
        x, y = generate_photon_coordinates(args.N, args.a1, args.a2)
        
        # Plot results
        fig = plot_photon_distribution(x, y, args.a1, args.a2)
        plt.show()
        
        # Save results to file
        output_file = 'photon_coordinates.txt'
        np.savetxt(output_file, np.column_stack((x, y)), header='X Y', comments='')
        print(f"Координаты фотонов сохранены в файл {output_file}")
    
    # If run without arguments, start GUI
    else:
        root = tk.Tk()
        app = PhotonGeneratorGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
