import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class DepthMapGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Depth Map Generator")
        self.root.geometry("800x700")
        
        # Variables
        self.width_var = tk.IntVar(value=1920)
        self.height_var = tk.IntVar(value=1080)
        self.wave_qty_var = tk.IntVar(value=5)
        self.wave_size_var = tk.DoubleVar(value=0.3)
        self.ripple_qty_var = tk.IntVar(value=10)
        self.ripple_size_var = tk.DoubleVar(value=0.1)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.bit_depth_var = tk.StringVar(value="16-bit")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Depth Map Generator", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Output Size Section
        size_frame = ttk.LabelFrame(main_frame, text="Output Size", padding="10")
        size_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(size_frame, text="Width (px):").grid(row=0, column=0, padx=5, pady=5)
        width_spin = ttk.Spinbox(size_frame, from_=100, to=10000, textvariable=self.width_var, width=10)
        width_spin.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(size_frame, text="Height (px):").grid(row=0, column=2, padx=5, pady=5)
        height_spin = ttk.Spinbox(size_frame, from_=100, to=10000, textvariable=self.height_var, width=10)
        height_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # Wave Controls Section
        wave_frame = ttk.LabelFrame(main_frame, text="Wave Controls", padding="10")
        wave_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(wave_frame, text="Wave Quantity:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        wave_qty_scale = ttk.Scale(wave_frame, from_=1, to=20, variable=self.wave_qty_var, orient=tk.HORIZONTAL, length=300)
        wave_qty_scale.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.wave_qty_label = ttk.Label(wave_frame, text="5")
        self.wave_qty_label.grid(row=0, column=2, padx=5, pady=5)
        wave_qty_scale.configure(command=lambda v: self.wave_qty_label.config(text=str(int(float(v)))))
        
        ttk.Label(wave_frame, text="Wave Size:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        wave_size_scale = ttk.Scale(wave_frame, from_=0.1, to=2.0, variable=self.wave_size_var, orient=tk.HORIZONTAL, length=300)
        wave_size_scale.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.wave_size_label = ttk.Label(wave_frame, text="0.30")
        self.wave_size_label.grid(row=1, column=2, padx=5, pady=5)
        wave_size_scale.configure(command=lambda v: self.wave_size_label.config(text=f"{float(v):.2f}"))
        
        # Ripple Controls Section
        ripple_frame = ttk.LabelFrame(main_frame, text="Ripple Controls", padding="10")
        ripple_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(ripple_frame, text="Ripple Quantity:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ripple_qty_scale = ttk.Scale(ripple_frame, from_=0, to=50, variable=self.ripple_qty_var, orient=tk.HORIZONTAL, length=300)
        ripple_qty_scale.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.ripple_qty_label = ttk.Label(ripple_frame, text="10")
        self.ripple_qty_label.grid(row=0, column=2, padx=5, pady=5)
        ripple_qty_scale.configure(command=lambda v: self.ripple_qty_label.config(text=str(int(float(v)))))
        
        ttk.Label(ripple_frame, text="Ripple Size:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ripple_size_scale = ttk.Scale(ripple_frame, from_=0.05, to=0.5, variable=self.ripple_size_var, orient=tk.HORIZONTAL, length=300)
        ripple_size_scale.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.ripple_size_label = ttk.Label(ripple_frame, text="0.10")
        self.ripple_size_label.grid(row=1, column=2, padx=5, pady=5)
        ripple_size_scale.configure(command=lambda v: self.ripple_size_label.config(text=f"{float(v):.2f}"))
        
        # Contrast Control
        contrast_frame = ttk.LabelFrame(main_frame, text="Contrast", padding="10")
        contrast_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(contrast_frame, text="Contrast:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        contrast_scale = ttk.Scale(contrast_frame, from_=0.1, to=3.0, variable=self.contrast_var, orient=tk.HORIZONTAL, length=300)
        contrast_scale.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.contrast_label = ttk.Label(contrast_frame, text="1.00")
        self.contrast_label.grid(row=0, column=2, padx=5, pady=5)
        contrast_scale.configure(command=lambda v: self.contrast_label.config(text=f"{float(v):.2f}"))
        
        # Bit Depth Selection
        bit_depth_frame = ttk.LabelFrame(main_frame, text="Bit Depth", padding="10")
        bit_depth_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(bit_depth_frame, text="16-bit", variable=self.bit_depth_var, value="16-bit").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(bit_depth_frame, text="32-bit", variable=self.bit_depth_var, value="32-bit").grid(row=0, column=1, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        generate_btn = ttk.Button(button_frame, text="Generate Preview", command=self.generate_preview)
        generate_btn.grid(row=0, column=0, padx=5)
        
        save_btn = ttk.Button(button_frame, text="Save Image", command=self.save_image)
        save_btn.grid(row=0, column=1, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        wave_frame.columnconfigure(1, weight=1)
        ripple_frame.columnconfigure(1, weight=1)
        contrast_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def generate_depth_map(self):
        """Generate the depth map based on current parameters"""
        width = self.width_var.get()
        height = self.height_var.get()
        wave_qty = self.wave_qty_var.get()
        wave_size = self.wave_size_var.get()
        ripple_qty = self.ripple_qty_var.get()
        ripple_size = self.ripple_size_var.get()
        contrast = self.contrast_var.get()
        
        # Create coordinate grids
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        X, Y = np.meshgrid(x, y)
        
        # Initialize depth map
        depth_map = np.zeros((height, width))
        
        # Generate waves (diagonal flowing patterns)
        for i in range(wave_qty):
            # Random direction and phase for each wave
            angle = np.random.uniform(0, 2 * np.pi)
            phase = np.random.uniform(0, 2 * np.pi)
            frequency = np.random.uniform(0.5, 2.0) * wave_size
            
            # Create wave pattern
            wave = np.sin(2 * np.pi * frequency * (X * np.cos(angle) + Y * np.sin(angle)) + phase)
            
            # Add some variation in amplitude
            amplitude = np.random.uniform(0.3, 1.0)
            depth_map += amplitude * wave
        
        # Normalize waves
        if wave_qty > 0:
            depth_map = depth_map / wave_qty
        
        # Generate ripples (smaller, more localized patterns)
        for i in range(ripple_qty):
            # Random center position
            center_x = np.random.uniform(0, 1)
            center_y = np.random.uniform(0, 1)
            
            # Distance from center
            dx = X - center_x
            dy = Y - center_y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Create ripple pattern
            frequency = np.random.uniform(5, 20) * ripple_size
            ripple = np.sin(2 * np.pi * frequency * distance + np.random.uniform(0, 2 * np.pi))
            
            # Apply falloff to make ripples fade
            falloff = np.exp(-distance * 3)
            ripple *= falloff
            
            # Add to depth map
            amplitude = np.random.uniform(0.1, 0.3)
            depth_map += amplitude * ripple
        
        # Normalize to 0-1 range
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-10)
        
        # Apply contrast
        depth_map = (depth_map - 0.5) * contrast + 0.5
        depth_map = np.clip(depth_map, 0, 1)
        
        return depth_map
    
    def generate_preview(self):
        """Generate and display a preview"""
        try:
            depth_map = self.generate_depth_map()
            
            # Convert to 8-bit for preview
            preview = (depth_map * 255).astype(np.uint8)
            preview_img = Image.fromarray(preview, mode='L')
            
            # Show in a new window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Preview")
            
            # Resize for preview if too large
            max_preview_size = 800
            if preview_img.width > max_preview_size or preview_img.height > max_preview_size:
                ratio = min(max_preview_size / preview_img.width, max_preview_size / preview_img.height)
                preview_img = preview_img.resize((int(preview_img.width * ratio), int(preview_img.height * ratio)), Image.Resampling.LANCZOS)
            
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(preview_img)
            
            label = ttk.Label(preview_window, image=photo)
            label.image = photo  # Keep a reference
            label.pack(padx=10, pady=10)
            
            info_label = ttk.Label(preview_window, text=f"Size: {self.width_var.get()}x{self.height_var.get()}px | Bit Depth: {self.bit_depth_var.get()}")
            info_label.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")
    
    def save_image(self):
        """Generate and save the depth map"""
        try:
            depth_map = self.generate_depth_map()
            
            # Ask for save location
            bit_depth = self.bit_depth_var.get()
            default_ext = ".png" if bit_depth == "16-bit" else ".tiff"
            
            filename = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=[
                    ("PNG files", "*.png"),
                    ("TIFF files", "*.tiff"),
                    ("All files", "*.*")
                ],
                title="Save Depth Map"
            )
            
            if not filename:
                return
            
            # Convert to appropriate bit depth
            if bit_depth == "16-bit":
                # 16-bit: 0-65535
                img_array = (depth_map * 65535).astype(np.uint16)
                img = Image.fromarray(img_array, mode='I;16')
            else:  # 32-bit
                # 32-bit float: 0.0-1.0
                img_array = depth_map.astype(np.float32)
                img = Image.fromarray(img_array, mode='F')
            
            # Save
            img.save(filename)
            messagebox.showinfo("Success", f"Depth map saved successfully!\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")


def main():
    root = tk.Tk()
    app = DepthMapGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

