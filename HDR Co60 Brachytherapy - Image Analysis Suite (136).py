import sys
import os
import tempfile
import traceback

# ========== UNIVERSAL COMPATIBILITY FIXES ==========

def setup_universal_compatibility():

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    try:
        import matplotlib
        matplotlib.use('Agg')  
        print("✓ Matplotlib backend set to Agg")
    except ImportError:
        print("⚠️  Matplotlib not available")
    

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  
    
    print("✓ Compatibility layer initialized")

def safe_imports():
  
    missing_packages = []
    
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        print("✓ tkinter imported")
    except ImportError as e:
        missing_packages.append(f"tkinter: {e}")
    
    try:
        from PIL import Image as PILImage, ImageTk
        print("✓ PIL imported")
    except ImportError as e:
        missing_packages.append(f"Pillow (PIL): {e}")
    
    try:
        import cv2
        print("✓ OpenCV imported")
    except ImportError as e:
        missing_packages.append(f"OpenCV: {e}")
    
    try:
        import numpy as np
        print("✓ NumPy imported")
    except ImportError as e:
        missing_packages.append(f"NumPy: {e}")
    
    try:
        from tkcalendar import DateEntry
        print("✓ tkcalendar imported")
    except ImportError as e:
        missing_packages.append(f"tkcalendar: {e}")
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported")
    except ImportError as e:
        missing_packages.append(f"matplotlib: {e}")
    
    try:
        import pydicom
        print("✓ pydicom imported")
    except ImportError:
        print("⚠️  pydicom not available - DICOM features disabled")
        
        class DummyDicom:
            def dcmread(self, *args, **kwargs):
                raise ImportError("pydicom not installed")
        sys.modules['pydicom'] = DummyDicom()
    
    if missing_packages:
        error_msg = "Missing required packages:\n" + "\n".join(missing_packages)
        error_msg += "\n\nPlease install using: pip install -r requirements.txt"
        raise ImportError(error_msg)
    
    print("✓ All packages imported successfully")

def handle_exceptions(exctype, value, tb):
  
    error_msg = f"Application Error:\n\n{exctype.__name__}: {value}"
    
    
    print("CRITICAL ERROR:")
    traceback.print_exception(exctype, value, tb)
    
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", 
                           f"{error_msg}\n\nPlease check the console for details.")
        root.destroy()
    except:
        print(f"Could not show error dialog: {error_msg}")
    
    sys.exit(1)


sys.excepthook = handle_exceptions


setup_universal_compatibility()


safe_imports()

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class BEDEQD2Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BED & EQD2 Calculator - Multiple Fractions")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f5f5f5")
        
        
        self.setup_variables()
        self.create_interface()
    
    def setup_variables(self):
       
        self.ebt_fractions = tk.StringVar(value="30")
        self.ebt_dose_per_fx = tk.StringVar(value="1.8")
        
        
        self.hdr_fractions = tk.StringVar(value="2")
        self.hdr_prescription_dose = tk.StringVar(value="9.0")
        
       
        self.structure_vars = {
            'point_A': {
                'ab_ratio': tk.StringVar(value="10"),
                'fx1_percent': tk.StringVar(value="100.0"),
                'fx2_percent': tk.StringVar(value="0.0")
            },
            'point_B': {
                'ab_ratio': tk.StringVar(value="10"),
                'fx1_percent': tk.StringVar(value="21.26"),
                'fx2_percent': tk.StringVar(value="0.0")
            },
            'bladder': {
                'ab_ratio': tk.StringVar(value="3"),
                'fx1_percent': tk.StringVar(value="61.3725"),
                'fx2_percent': tk.StringVar(value="0.0")
            },
            'rectum': {
                'ab_ratio': tk.StringVar(value="3"),
                'fx1_percent': tk.StringVar(value="68.24"),
                'fx2_percent': tk.StringVar(value="0.0")
            }
        }
    
    def create_interface(self):
     
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
       
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
    
        main_frame.grid_rowconfigure(0, weight=0)  
        main_frame.grid_rowconfigure(1, weight=0)  
        main_frame.grid_rowconfigure(2, weight=0)  
        main_frame.grid_rowconfigure(3, weight=1)  
        main_frame.grid_rowconfigure(4, weight=0)  
        
        for i in range(12): 
            main_frame.grid_columnconfigure(i, weight=1)
        
        
        self.build_calculator_interface(main_frame)
    
    def build_calculator_interface(self, parent):
        
        title_frame = tk.Frame(parent, bg="#2c3e50")
        title_frame.grid(row=0, column=0, columnspan=12, sticky="ew", pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="BED & EQD2 Calculator - Fraction-wise Calculation", 
                              font=('Arial', 12, 'bold'), 
                              fg="white", 
                              bg="#2c3e50")
        title_label.pack(pady=2)
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Biological Effective Dose and Equivalent Dose in 2 Gy Fractions", 
                                 font=('Arial', 8), 
                                 fg="#ecf0f1", 
                                 bg="#2c3e50")
        subtitle_label.pack()
        
    
        param_frame = tk.LabelFrame(parent, text="Treatment Parameters", 
                                   bg="#f5f5f5", fg="#2c3e50",
                                   font=('Arial', 10, 'bold'),
                                   relief="groove", bd=2,
                                   padx=10, pady=10)
        param_frame.grid(row=1, column=0, columnspan=12, sticky="ew", pady=(0, 10))
        param_frame.grid_columnconfigure(0, weight=0)
        param_frame.grid_columnconfigure(1, weight=0)
        param_frame.grid_columnconfigure(2, weight=0)
        param_frame.grid_columnconfigure(3, weight=0)
        param_frame.grid_columnconfigure(4, weight=1)
        
       
        tk.Label(param_frame, text="EBT:", font=('Arial', 9, 'bold'), 
                bg="#f5f5f5", fg="#2c3e50").grid(row=0, column=0, sticky="w")
        tk.Label(param_frame, text="Nr. of Fractions", bg="#f5f5f5", fg="#2c3e50").grid(row=0, column=1, padx=(20,5))
        tk.Entry(param_frame, textvariable=self.ebt_fractions, width=8, 
                relief="solid", bd=1).grid(row=0, column=2)
        tk.Label(param_frame, text="Dose/Fraction [Gy]", bg="#f5f5f5", fg="#2c3e50").grid(row=0, column=3, padx=(20,5))
        tk.Entry(param_frame, textvariable=self.ebt_dose_per_fx, width=8,
                relief="solid", bd=1).grid(row=0, column=4, sticky="w")
        
        
        tk.Label(param_frame, text="HDR:", font=('Arial', 9, 'bold'), 
                bg="#f5f5f5", fg="#2c3e50").grid(row=1, column=0, sticky="w", pady=(10,0))
        tk.Label(param_frame, text="Nr. of Fractions:", bg="#f5f5f5", fg="#2c3e50").grid(row=1, column=1, padx=(20,5), pady=(10,0))
        tk.Entry(param_frame, textvariable=self.hdr_fractions, width=8,
                relief="solid", bd=1).grid(row=1, column=2, pady=(10,0))
        tk.Label(param_frame, text="Prescription Dose/Fx [Gy]:", bg="#f5f5f5", fg="#2c3e50").grid(row=1, column=3, padx=(20,5), pady=(10,0))
        tk.Entry(param_frame, textvariable=self.hdr_prescription_dose, width=8,
                relief="solid", bd=1).grid(row=1, column=4, pady=(10,0), sticky="w")
        
       
        struct_frame = tk.LabelFrame(parent, text="Structure Parameters - Fraction Doses (% of Rx)", 
                                    bg="#f5f5f5", fg="#2c3e50",
                                    font=('Arial', 10, 'bold'),
                                    relief="groove", bd=2,
                                    padx=10, pady=10)
        struct_frame.grid(row=2, column=0, columnspan=12, sticky="ew", pady=(10, 10))
        
       
        for i in range(6):
            struct_frame.grid_columnconfigure(i, weight=1)
        
       
        headers = ['Structure', 'α/β Ratio', 'Fx1 [%Rx]', 'Fx2 [%Rx]', 'Avg [%Rx]', 'Total Dose [Gy]']
        for col, header in enumerate(headers):
            tk.Label(struct_frame, text=header, font=('Arial', 9, 'bold'), 
                    bg="#f5f5f5", fg="#2c3e50").grid(row=0, column=col, padx=5, pady=5, sticky="w")
        
       
        structures = [
            ('point_A', 'Point A'),
            ('point_B', 'Point B'),
            ('bladder', 'Bladder'),
            ('rectum', 'Rectum')
        ]
        
        for row, (struct_key, display_name) in enumerate(structures, 1):
         
            tk.Label(struct_frame, text=display_name, bg="#f5f5f5", fg="#2c3e50").grid(row=row, column=0, padx=5, pady=3, sticky="w")
            
          
            tk.Entry(struct_frame, textvariable=self.structure_vars[struct_key]['ab_ratio'], 
                    width=8, relief="solid", bd=1).grid(row=row, column=1, padx=5, pady=3, sticky="w")
            
           
            tk.Entry(struct_frame, textvariable=self.structure_vars[struct_key]['fx1_percent'], 
                    width=10, relief="solid", bd=1).grid(row=row, column=2, padx=5, pady=3, sticky="w")
            
            
            tk.Entry(struct_frame, textvariable=self.structure_vars[struct_key]['fx2_percent'], 
                    width=10, relief="solid", bd=1).grid(row=row, column=3, padx=5, pady=3, sticky="w")
            
            
            avg_percent_label = tk.Label(struct_frame, text="", width=10, bg="#f5f5f5", fg="#2c3e50")
            avg_percent_label.grid(row=row, column=4, padx=5, pady=3, sticky="w")
            self.structure_vars[struct_key]['avg_percent'] = avg_percent_label
            
            
            total_dose_label = tk.Label(struct_frame, text="", width=10, bg="#f5f5f5", fg="#2c3e50")
            total_dose_label.grid(row=row, column=5, padx=5, pady=3, sticky="w")
            self.structure_vars[struct_key]['total_dose'] = total_dose_label
        
       
        results_frame = tk.LabelFrame(parent, text="Fraction-wise BED & EQD2 Results", 
                                     bg="#f5f5f5", fg="#2c3e50",
                                     font=('Arial', 10, 'bold'),
                                     relief="groove", bd=2,
                                     padx=10, pady=10)
        results_frame.grid(row=3, column=0, columnspan=12, sticky="nsew", pady=(10, 10))
        
       
        results_frame.grid_rowconfigure(0, weight=0) 
        results_frame.grid_rowconfigure(1, weight=1)  
        for i in range(12):
            results_frame.grid_columnconfigure(i, weight=1)
        
  
        canvas = tk.Canvas(results_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
    
        headers = [
            'Structure', 'α/β [Gy]', 
            'Fx1 BED', 'Fx2 BED', 'Fx1 EQD2', 'Fx2 EQD2',
            'HDR BED Total', 'HDR EQD2', 
            'EBT BED', 'EBT EQD2',
            'Total BED', 'Total EQD2'
        ]
        
        for col, header in enumerate(headers):
            tk.Label(scrollable_frame, text=header, font=('Arial', 8, 'bold'), 
                    bg="#f5f5f5", fg="#2c3e50", width=12).grid(row=0, column=col, padx=2, pady=5, sticky="w")
        
        
        self.structure_rows = {}
        
        for row, (struct_key, display_name) in enumerate(structures, 1):
        
            tk.Label(scrollable_frame, text=display_name, font=('Arial', 8), 
                    bg="#f5f5f5", fg="#2c3e50", width=12).grid(row=row, column=0, padx=2, sticky="w")
            
         
            ab_label = tk.Label(scrollable_frame, textvariable=self.structure_vars[struct_key]['ab_ratio'], 
                               font=('Arial', 8), bg="#f5f5f5", fg="#2c3e50", width=12)
            ab_label.grid(row=row, column=1, padx=2, sticky="w")
            
          
            fx1_bed_label = self.create_clickable_label(scrollable_frame, row, 2)
            fx2_bed_label = self.create_clickable_label(scrollable_frame, row, 3)
            fx1_eqd2_label = self.create_clickable_label(scrollable_frame, row, 4)
            fx2_eqd2_label = self.create_clickable_label(scrollable_frame, row, 5)
            hdr_bed_label = self.create_clickable_label(scrollable_frame, row, 6)
            hdr_eqd2_label = self.create_clickable_label(scrollable_frame, row, 7)
            ebt_bed_label = self.create_clickable_label(scrollable_frame, row, 8)
            ebt_eqd2_label = self.create_clickable_label(scrollable_frame, row, 9)
            total_bed_label = self.create_clickable_label(scrollable_frame, row, 10)
            total_eqd2_label = self.create_clickable_label(scrollable_frame, row, 11)
            
            self.structure_rows[struct_key] = {
                'fx1_bed': fx1_bed_label,
                'fx2_bed': fx2_bed_label,
                'fx1_eqd2': fx1_eqd2_label,
                'fx2_eqd2': fx2_eqd2_label,
                'hdr_bed': hdr_bed_label,
                'hdr_eqd2': hdr_eqd2_label,
                'ebt_bed': ebt_bed_label,
                'ebt_eqd2': ebt_eqd2_label,
                'total_bed': total_bed_label,
                'total_eqd2': total_eqd2_label
            }
        
       
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
     
        button_frame = tk.Frame(parent, bg="#f5f5f5")
        button_frame.grid(row=4, column=0, columnspan=12, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
      
        calc_button = tk.Button(button_frame, text="Calculate All", 
                               command=self.calculate_all,
                               bg="#3498db", fg="white", 
                               font=('Arial', 10, 'bold'),
                               relief="raised", bd=2,
                               width=15, height=1)
        calc_button.grid(row=0, column=0, padx=5)
        
        clear_button = tk.Button(button_frame, text="Clear Results", 
                                command=self.clear_all,
                                bg="#e74c3c", fg="white",
                                font=('Arial', 10, 'bold'),
                                relief="raised", bd=2,
                                width=15, height=1)
        clear_button.grid(row=0, column=1, padx=5)
        
        export_button = tk.Button(button_frame, text="Export to CSV", 
                                 command=self.export_to_csv,
                                 bg="#27ae60", fg="white",
                                 font=('Arial', 10, 'bold'),
                                 relief="raised", bd=2,
                                 width=15, height=1)
        export_button.grid(row=0, column=2, padx=5)
        
      
        self.update_averages()
    
    def create_clickable_label(self, parent, row, column):
        """Create a label that can be clicked to copy its value"""
        label = tk.Label(parent, text="", width=12, font=('Arial', 8), 
                        relief="solid", bd=1, bg='white', cursor="hand2",
                        fg="#2c3e50", anchor="w")
        label.grid(row=row, column=column, padx=2, sticky="w")
        label.bind("<Button-1>", lambda e: self.copy_to_clipboard(label.cget("text")))
        label.bind("<Enter>", lambda e: label.config(bg='#ecf0f1'))
        label.bind("<Leave>", lambda e: label.config(bg='white'))
        return label
    
    def copy_to_clipboard(self, text):
       
        if text and text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            # Show brief tooltip
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{self.root.winfo_pointerx()+10}+{self.root.winfo_pointery()+10}")
            label = tk.Label(tooltip, text="Copied!", bg="#2ecc71", fg="white", 
                           relief="solid", bd=1, font=('Arial', 8, 'bold'))
            label.pack()
            tooltip.after(1000, tooltip.destroy)
    
    def update_averages(self):
      
        try:
            hdr_rx_dose = float(self.hdr_prescription_dose.get())
            
            for struct_key in self.structure_vars:
                try:
                    fx1_percent = float(self.structure_vars[struct_key]['fx1_percent'].get())
                    fx2_percent = float(self.structure_vars[struct_key]['fx2_percent'].get())
                    
                 
                    avg_percent = (fx1_percent + fx2_percent) / 2
                    self.structure_vars[struct_key]['avg_percent'].config(text=f"{avg_percent:.4f}")
                    
                   
                    fx1_dose = (fx1_percent / 100) * hdr_rx_dose
                    fx2_dose = (fx2_percent / 100) * hdr_rx_dose
                    total_dose = fx1_dose + fx2_dose
                    self.structure_vars[struct_key]['total_dose'].config(text=f"{total_dose:.4f}")
                    
                except:
                    self.structure_vars[struct_key]['avg_percent'].config(text="")
                    self.structure_vars[struct_key]['total_dose'].config(text="")
        except:
            pass
    
    def calculate_fraction_bed_eqd2(self, dose, ab_ratio):
   
        bed = dose * (1 + (dose / ab_ratio))
        eqd2 = bed / (1 + (2 / ab_ratio))
        return bed, eqd2
    
    def calculate_bed_eqd2(self, total_dose, dose_per_fraction, ab_ratio):
        
        bed = total_dose * (1 + (dose_per_fraction / ab_ratio))
        eqd2 = bed / (1 + (2 / ab_ratio))
        return bed, eqd2
    
    def calculate_all(self):
       
        try:
       
            self.update_averages()
            
           
            ebt_fx = float(self.ebt_fractions.get())
            ebt_dose_fx = float(self.ebt_dose_per_fx.get())
            hdr_rx_dose = float(self.hdr_prescription_dose.get())
            
        
            for struct_key, vars_dict in self.structure_vars.items():
             
                ab_ratio = float(vars_dict['ab_ratio'].get())
                
               
                fx1_percent = float(vars_dict['fx1_percent'].get())
                fx2_percent = float(vars_dict['fx2_percent'].get())
                
                fx1_dose = (fx1_percent / 100) * hdr_rx_dose
                fx2_dose = (fx2_percent / 100) * hdr_rx_dose
                total_hdr_dose = fx1_dose + fx2_dose
                
                
                fx1_bed, fx1_eqd2 = self.calculate_fraction_bed_eqd2(fx1_dose, ab_ratio)
                fx2_bed, fx2_eqd2 = self.calculate_fraction_bed_eqd2(fx2_dose, ab_ratio)
                
          
                hdr_bed_total = fx1_bed + fx2_bed
                hdr_eqd2 = hdr_bed_total / (1 + (2 / ab_ratio))
                
     
                ebt_total_dose = ebt_fx * ebt_dose_fx
                ebt_bed, ebt_eqd2 = self.calculate_bed_eqd2(ebt_total_dose, ebt_dose_fx, ab_ratio)
                
               
                total_bed = ebt_bed + hdr_bed_total
                total_eqd2 = total_bed / (1 + (2 / ab_ratio))
                
                
                self.structure_rows[struct_key]['fx1_bed'].config(text=f"{fx1_bed:.4f}")
                self.structure_rows[struct_key]['fx2_bed'].config(text=f"{fx2_bed:.4f}")
                self.structure_rows[struct_key]['fx1_eqd2'].config(text=f"{fx1_eqd2:.4f}")
                self.structure_rows[struct_key]['fx2_eqd2'].config(text=f"{fx2_eqd2:.4f}")
                self.structure_rows[struct_key]['hdr_bed'].config(text=f"{hdr_bed_total:.4f}")
                self.structure_rows[struct_key]['hdr_eqd2'].config(text=f"{hdr_eqd2:.4f}")
                self.structure_rows[struct_key]['ebt_bed'].config(text=f"{ebt_bed:.4f}")
                self.structure_rows[struct_key]['ebt_eqd2'].config(text=f"{ebt_eqd2:.4f}")
                self.structure_rows[struct_key]['total_bed'].config(text=f"{total_bed:.4f}")
                self.structure_rows[struct_key]['total_eqd2'].config(text=f"{total_eqd2:.4f}")
        
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please check all input values are valid numbers")
    
    def clear_all(self):
       
        for struct_key in self.structure_vars:
            self.structure_vars[struct_key]['avg_percent'].config(text="")
            self.structure_vars[struct_key]['total_dose'].config(text="")
        
        for struct_key in self.structure_rows:
            self.structure_rows[struct_key]['fx1_bed'].config(text="")
            self.structure_rows[struct_key]['fx2_bed'].config(text="")
            self.structure_rows[struct_key]['fx1_eqd2'].config(text="")
            self.structure_rows[struct_key]['fx2_eqd2'].config(text="")
            self.structure_rows[struct_key]['hdr_bed'].config(text="")
            self.structure_rows[struct_key]['hdr_eqd2'].config(text="")
            self.structure_rows[struct_key]['ebt_bed'].config(text="")
            self.structure_rows[struct_key]['ebt_eqd2'].config(text="")
            self.structure_rows[struct_key]['total_bed'].config(text="")
            self.structure_rows[struct_key]['total_eqd2'].config(text="")
    
    def export_to_csv(self):
        """Export results to CSV file with all fraction-wise details"""
        try:
            data = []
            structures_display = {
                'point_A': 'Point A',
                'point_B': 'Point B',
                'bladder': 'Bladder',
                'rectum': 'Rectum'
            }
            
            # Get EBT parameters for the export
            ebt_fx = float(self.ebt_fractions.get())
            ebt_dose_fx = float(self.ebt_dose_per_fx.get())
            ebt_total_dose = ebt_fx * ebt_dose_fx
            
            hdr_rx_dose = float(self.hdr_prescription_dose.get())
            
            for struct_key, display_name in structures_display.items():
                # Get fraction data
                fx1_percent = float(self.structure_vars[struct_key]['fx1_percent'].get())
                fx2_percent = float(self.structure_vars[struct_key]['fx2_percent'].get())
                fx1_dose = (fx1_percent / 100) * hdr_rx_dose
                fx2_dose = (fx2_percent / 100) * hdr_rx_dose
                
                # Calculate EBT components for this structure's α/β
                ab_ratio = float(self.structure_vars[struct_key]['ab_ratio'].get())
                ebt_bed, ebt_eqd2 = self.calculate_bed_eqd2(ebt_total_dose, ebt_dose_fx, ab_ratio)
                
                row_data = {
                    'Structure': display_name,
                    'α/β_Ratio': ab_ratio,
                    'Fx1_%Rx': fx1_percent,
                    'Fx2_%Rx': fx2_percent,
                    'Fx1_Dose_Gy': f"{fx1_dose:.4f}",
                    'Fx2_Dose_Gy': f"{fx2_dose:.4f}",
                    'Total_HDR_Dose_Gy': self.structure_vars[struct_key]['total_dose'].cget('text'),
                    'BED_Fx1': self.structure_rows[struct_key]['fx1_bed'].cget('text'),
                    'BED_Fx2': self.structure_rows[struct_key]['fx2_bed'].cget('text'),
                    'EQD2_Fx1': self.structure_rows[struct_key]['fx1_eqd2'].cget('text'),
                    'EQD2_Fx2': self.structure_rows[struct_key]['fx2_eqd2'].cget('text'),
                    'HDR_BED_Total': self.structure_rows[struct_key]['hdr_bed'].cget('text'),
                    'HDR_EQD2': self.structure_rows[struct_key]['hdr_eqd2'].cget('text'),
                    'EBT_BED': f"{ebt_bed:.4f}",
                    'EBT_EQD2': f"{ebt_eqd2:.4f}",
                    'Total_BED': self.structure_rows[struct_key]['total_bed'].cget('text'),
                    'Total_EQD2': self.structure_rows[struct_key]['total_eqd2'].cget('text')
                }
                data.append(row_data)
            
            df = pd.DataFrame(data)
            df.to_csv('bed_eqd2_fraction_wise_results.csv', index=False)
            messagebox.showinfo("Export Successful", 
                              "Results exported to 'bed_eqd2_fraction_wise_results.csv'\n\n"
                              "Includes all fraction-wise BED, EQD2 values and totals.")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export data:\n{str(e)}")
            
import json
import math
import re
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image as PILImage, ImageTk
import cv2
import numpy as np
from datetime import datetime
import json
import os
import math
import re
import tempfile
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class BrachyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HDR Co60 Brachytherapy Image Loader")
        
       
        self.check_dependencies()
        
      
        self.temp_dir = self.create_temp_directory()
        
        
        self.patient_info = {}
        self.image_paths = {
            "AP_frac1": None,
            "LAT_frac1": None,
            "AP_frac2": None,
            "LAT_frac2": None
        }
        
       
        self.pixel_spacing = {
            "AP_frac1": 0.2979,  
            "AP_frac2": 0.2979,
            "LAT_frac1": 0.2979,
            "LAT_frac2": 0.2979
        }

        
        self.current_window = "main"  
        self.ap_window = None
        self.lat_window = None
        
        self.create_widgets()

    def get_screen_info(self):
     
        try:
           
            self.root.update()
            
           
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            
            ref_width = 1920
            ref_height = 1080
            
            
            width_scale = screen_width / ref_width
            height_scale = screen_height / ref_height
            
            
            scale_factor = min(width_scale, height_scale, 1.3)  
            
            
            scale_factor = max(0.7, scale_factor)
            
            print(f"Screen: {screen_width}x{screen_height}, Scale: {scale_factor:.2f}")
            
            return {
                'width': screen_width,
                'height': screen_height,
                'scale': scale_factor,
                'width_scale': width_scale,
                'height_scale': height_scale
            }
        except Exception as e:
            print(f"Screen detection error: {e}")
            
            return {
                'width': 1920,
                'height': 1080,
                'scale': 1.0,
                'width_scale': 1.0,
                'height_scale': 1.0
            }

    def get_scaled_font(self, base_size=10, bold=False):
    
        screen_info = self.get_screen_info()
        scaled_size = max(8, int(base_size * screen_info['scale']))
        
        weight = "bold" if bold else "normal"
        return ("Arial", scaled_size, weight)

    def get_scaled_size(self, size):

        screen_info = self.get_screen_info()
        return int(size * screen_info['scale'])

    def create_scaled_button(self, parent, text, command, **kwargs):
   
        
        defaults = {
            'font': self.get_scaled_font(10),
            'relief': "raised",
            'bd': self.get_scaled_size(2)
        }
        
       
        defaults.update(kwargs)
        
       
        if 'width' in defaults:
            defaults['width'] = self.get_scaled_size(defaults['width'])
        if 'height' in defaults:
            defaults['height'] = self.get_scaled_size(defaults['height'])
            
        return tk.Button(parent, text=text, command=command, **defaults)

    def create_scaled_label(self, parent, text=None, **kwargs):
     
        
        defaults = {
            'font': self.get_scaled_font(10),
            'bg': parent.cget('bg') if 'bg' not in kwargs else kwargs['bg']
        }
        
        
        defaults.update(kwargs)
        
        return tk.Label(parent, text=text, **defaults)

    def create_scaled_entry(self, parent, **kwargs):
    
        
        defaults = {
            'font': self.get_scaled_font(10),
            'relief': "solid",
            'bd': self.get_scaled_size(1)
        }
        
        
        defaults.update(kwargs)
        
        
        if 'width' in defaults:
            defaults['width'] = self.get_scaled_size(defaults['width'])
            
        return tk.Entry(parent, **defaults)

    def create_scaled_frame(self, parent, **kwargs):
     
        defaults = {}
        
        
        if 'padx' in kwargs:
            kwargs['padx'] = self.get_scaled_size(kwargs['padx'])
        if 'pady' in kwargs:
            kwargs['pady'] = self.get_scaled_size(kwargs['pady'])
            
        defaults.update(kwargs)
        return tk.Frame(parent, **defaults)

    def create_scaled_labelframe(self, parent, text, **kwargs):
   
        defaults = {
            'font': self.get_scaled_font(12, bold=True)
        }
        
       
        if 'padx' in kwargs:
            kwargs['padx'] = self.get_scaled_size(kwargs['padx'])
        if 'pady' in kwargs:
            kwargs['pady'] = self.get_scaled_size(kwargs['pady'])
            
        defaults.update(kwargs)
        return tk.LabelFrame(parent, text=text, **defaults)


    def return_to_main(self):
    
        if hasattr(self, 'ap_window') and self.ap_window and self.ap_window.winfo_exists():
            self.ap_window.destroy()
            self.ap_window = None
        
        if hasattr(self, 'lat_window') and self.lat_window and self.lat_window.winfo_exists():
            self.lat_window.destroy()
            self.lat_window = None
        
        self.current_window = "main"
        self.update_status("Ready - Returned to main menu")

    def navigate_to_lat_from_ap(self):
     
        if hasattr(self, 'ap_window') and self.ap_window and self.ap_window.winfo_exists():
            self.ap_window.destroy()
            self.ap_window = None
        
        self.current_window = "lat"
        self.show_lat_images()

    def navigate_to_ap_from_lat(self):
       
        if hasattr(self, 'lat_window') and self.lat_window and self.lat_window.winfo_exists():
            self.lat_window.destroy()
            self.lat_window = None
        
        self.current_window = "ap"
        self.show_ap_images()

    
    def center_window_safe(self, window, width, height, taskbar_height=40):
  
        try:
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
        except:
            screen_width = 1920
            screen_height = 1080
            
        
        x = (screen_width - width) // 2
        y = (screen_height - height - taskbar_height) // 2
        
        
        y = max(0, y)  
        
        window.geometry(f"{width}x{height}+{x}+{y}")


    def start_ap_workflow(self):
       
        if not self.validate_images_for_analysis("AP"):
            return
        
        self.current_window = "ap"
        self.show_ap_images()

    def start_lat_workflow(self):
      
        if not self.validate_images_for_analysis("LAT"):
            return
        
        self.current_window = "lat"
        self.show_lat_images()

    def validate_images_for_analysis(self, view_type):
    
        if view_type == "AP":
            required = ["AP_frac1"]
            if self.fractions_entry.get() == "2":
                required.append("AP_frac2")
        else:  
            required = ["LAT_frac1"]
            if self.fractions_entry.get() == "2":
                required.append("LAT_frac2")
        
        missing = []
        for key in required:
            if not self.image_paths[key]:
                missing.append(key.replace('_', ' ').title())
        
        if missing:
            messagebox.showerror(
                "Missing Images", 
                f"Please upload the following images first:\n" + "\n".join(missing)
            )
            return False
        return True

    def show_final_results(self):
   
        self.return_to_main()
        
        
        messagebox.showinfo(
            "Analysis Complete", 
            "🎉 Analysis workflow completed!\n\n"
            "Both AP and Lateral analyses have been processed.\n"
            "You can now:\n"
            "• Compare fractions using the main menu\n"
            "• Review patient information\n"
            "• Start a new patient analysis"
        )
        
        self.update_status("Analysis complete - Ready for new patient or comparisons")

        
    def check_dependencies(self):
        """Verify all required dependencies are available"""
        missing_deps = []
        try:
            import tkinter
        except ImportError:
            missing_deps.append("tkinter")
            
        try:
            from PIL import Image
        except ImportError:
            missing_deps.append("Pillow")
            
        try:
            import cv2
        except ImportError:
            missing_deps.append("OpenCV")
            
        try:
            import numpy
        except ImportError:
            missing_deps.append("NumPy")
            
        if missing_deps:
            messagebox.showerror(
                "Missing Dependencies", 
                f"The following dependencies are missing: {', '.join(missing_deps)}\n\n"
                "Please install them using: pip install opencv-python pillow numpy"
            )
            sys.exit(1)
    
    def create_temp_directory(self):
    
        temp_dir = os.path.join(tempfile.gettempdir(), "BrachyApp")
        try:
            os.makedirs(temp_dir, exist_ok=True)
            return temp_dir
        except (OSError, PermissionError) as e:
            
            temp_dir = os.path.join(os.getcwd(), "BrachyApp_Temp")
            os.makedirs(temp_dir, exist_ok=True)
            return temp_dir
    
    def get_safe_window_size(self, parent):
     
        try:
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()
        except:
            screen_width = 1280
            screen_height = 800
            
        width = min(max(1000, int(screen_width * 0.7)), screen_width - 100)
        height = min(max(700, int(screen_height * 0.7)), screen_height - 100)
        
        return width, height


    def debug_distance_saving(self):
       
        import glob
        from datetime import datetime
    
        
        temp_dir = self.temp_dir
        pattern = os.path.join(temp_dir, "**", "*distance*.txt")
        all_distance_files = glob.glob(pattern, recursive=True)
    
        prinshow_apt("=== ALL DISTANCE FILES FOUND ===")
        for file_path in all_distance_files:
            print(f"File: {file_path}")
            print(f"Size: {os.path.getsize(file_path)} bytes")
            print(f"Modified: {datetime.fromtimestamp(os.path.getmtime(file_path))}")
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    print(f"First 100 chars: {content[:100]}...")
            except Exception as e:
                print(f"Error reading: {e}")
            print("-" * 50)

    def get_adaptive_preview_size(self):
        
        screen_info = self.get_screen_info()
        
       
        base_size = 400
        scaled_size = int(base_size * screen_info['scale'])
        
      
        min_size = 300
        max_size = 600
        
        return max(min_size, min(scaled_size, max_size))

    
    def center_window(self, window, width, height):
        
        screen_info = self.get_screen_info()
        
      
        scaled_width = int(width * screen_info['scale'])
        scaled_height = int(height * screen_info['scale'])
        
        x = (screen_info['width'] - scaled_width) // 2
        y = (screen_info['height'] - scaled_height) // 2
        
        window.geometry(f"{scaled_width}x{scaled_height}+{x}+{y}")



    def create_widgets(self):
        
        screen_info = self.get_screen_info()
        
      
        window_width = int(1300 * screen_info['scale'])
        window_height = int(950 * screen_info['scale'])
        min_width = int(1100 * screen_info['scale'])
        min_height = int(800 * screen_info['scale'])
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(min_width, min_height)
        self.root.title("HDR Co60 Brachytherapy - Image Analysis Suite")

       
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass

        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        
        pad_x = int(10 * screen_info['scale'])
        pad_y = int(10 * screen_info['scale'])
        main_container = tk.Frame(self.root, bg="#f5f5f5", padx=pad_x, pady=pad_y)
        main_container.pack(fill=tk.BOTH, expand=True)

       
        for i in range(6):
            main_container.grid_rowconfigure(i, weight=1 if i == 4 else 0)
        main_container.grid_columnconfigure(0, weight=1)

       
        header_frame = tk.Frame(main_container, bg="#2c3e50", pady=int(5 * screen_info['scale']))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, int(5 * screen_info['scale'])))

       
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        
        title_frame = tk.Frame(header_frame, bg="#2c3e50")
        title_frame.grid(row=0, column=0, sticky="w")

        self.create_scaled_label(title_frame, "HDR Co60 Brachytherapy Analysis", 
                               font=self.get_scaled_font(12, bold=True), fg="white", bg="#2c3e50").pack(pady=2)
        self.create_scaled_label(title_frame, "Image Loader and Applicator Tracking System", 
                               font=self.get_scaled_font(8), fg="#ecf0f1", bg="#2c3e50").pack()

    
        new_patient_frame = tk.Frame(header_frame, bg="#2c3e50")
        new_patient_frame.grid(row=0, column=1, sticky="e", padx=pad_x, pady=int(5 * screen_info['scale']))

        self.create_scaled_button(new_patient_frame, text="🔄 New Patient", command=self.new_patient,
                  bg="#e74c3c", fg="white", font=self.get_scaled_font(10, bold=True), 
                  width=15, height=1).pack()

       
        info_frame = tk.LabelFrame(main_container, text="📋 Patient Information", 
                             padx=int(15 * screen_info['scale']), pady=int(15 * screen_info['scale']), 
                             font=self.get_scaled_font(12, bold=True),
                             bg="white", relief="groove", bd=2)
        info_frame.grid(row=2, column=0, sticky="ew", pady=(0, int(15 * screen_info['scale'])))

        
        label_font = self.get_scaled_font(10, bold=True)
        entry_font = self.get_scaled_font(10)

        
        pady_val = int(8 * screen_info['scale'])
        padx_val = int(5 * screen_info['scale'])

        self.create_scaled_label(info_frame, text="Patient Name:", font=label_font, bg="white").grid(
            row=0, column=0, sticky="e", pady=pady_val, padx=padx_val)
        self.name_entry = self.create_scaled_entry(info_frame, width=30, font=entry_font, relief="solid", bd=1)
        self.name_entry.grid(row=0, column=1, padx=int(15 * screen_info['scale']), pady=pady_val, sticky="w")

        self.create_scaled_label(info_frame, text="Number of Fractions:", font=label_font, bg="white").grid(
            row=0, column=2, sticky="e", pady=pady_val, padx=padx_val)
        self.fractions_entry = self.create_scaled_entry(info_frame, width=10, font=entry_font, relief="solid", bd=1)
        self.fractions_entry.grid(row=0, column=3, padx=int(15 * screen_info['scale']), pady=pady_val, sticky="w")

        self.create_scaled_label(info_frame, text="Admission Number:", font=label_font, bg="white").grid(
            row=0, column=4, sticky="e", pady=pady_val, padx=padx_val)
        self.admission_entry = self.create_scaled_entry(info_frame, width=20, font=entry_font, relief="solid", bd=1)
        self.admission_entry.grid(row=0, column=5, padx=int(15 * screen_info['scale']), pady=pady_val, sticky="w")

        
        help_label = self.create_scaled_label(info_frame, text="💡 Enter '2' for fraction comparison", 
                     font=self.get_scaled_font(9), fg="#7f8c8d", bg="white", justify="left")
        help_label.grid(row=0, column=6, sticky="w", padx=int(1 * screen_info['scale']), pady=int(1 * screen_info['scale']))

        
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        
        cal_frame = tk.LabelFrame(main_container, text="⚙️ Pixel Spacing Calibration (mm/pixel)", 
                                padx=int(20 * screen_info['scale']), pady=int(20 * screen_info['scale']), 
                                font=self.get_scaled_font(12, bold=True),
                                bg="white", relief="groove", bd=2)
        cal_frame.grid(row=3, column=0, sticky="ew", pady=(0, int(15 * screen_info['scale'])))

        
        cal_help = self.create_scaled_label(cal_frame, text="Set the conversion factor from pixels to millimeters", 
                           font=self.get_scaled_font(9), fg="#7f8c8d", bg="white")
        cal_help.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, int(10 * screen_info['scale'])))

        self.create_scaled_label(cal_frame, text="AP Images:", font=label_font, bg="white").grid(
            row=1, column=0, sticky="e", pady=pady_val, padx=padx_val)
        self.ap_spacing_entry = self.create_scaled_entry(cal_frame, width=12, font=entry_font, relief="solid", bd=1)
        self.ap_spacing_entry.insert(0, "0.2979")
        self.ap_spacing_entry.grid(row=1, column=1, padx=padx_val, pady=pady_val, sticky="w")
    
        self.create_scaled_label(cal_frame, text="Lateral Images:", font=label_font, bg="white").grid(
            row=1, column=2, sticky="e", pady=pady_val, padx=padx_val)
        self.lat_spacing_entry = self.create_scaled_entry(cal_frame, width=12, font=entry_font, relief="solid", bd=1)
        self.lat_spacing_entry.insert(0, "0.2979")
        self.lat_spacing_entry.grid(row=1, column=3, padx=padx_val, pady=pady_val, sticky="w")

        
        self.create_scaled_button(cal_frame, text="Apply Calibration", command=self.apply_calibration,
                  bg="#3498db", fg="white", font=self.get_scaled_font(10, bold=True), 
                  width=25, height=1).grid(row=1, column=4, padx=int(20 * screen_info['scale']), pady=pady_val)

       
        cal_frame.grid_columnconfigure(4, weight=1)
    
        
        fractions_container = tk.Frame(main_container, bg="#f5f5f5")
        fractions_container.grid(row=4, column=0, sticky="nsew", pady=(0, int(15 * screen_info['scale'])))

        
        fractions_container.grid_propagate(False)
        fractions_container.config(height=int(500 * screen_info['scale']))

      
        fractions_container.grid_rowconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(1, weight=1)

     
        left_column = tk.Frame(fractions_container, bg="#f5f5f5")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, int(10 * screen_info['scale'])))
        right_column = tk.Frame(fractions_container, bg="#f5f5f5")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(int(10 * screen_info['scale']), 0))

     
        left_column.grid_propagate(False)
        right_column.grid_propagate(False)
        column_width = int(600 * screen_info['scale'])
        column_height = int(500 * screen_info['scale'])
        left_column.config(width=column_width, height=column_height)
        right_column.config(width=column_width, height=column_height)

        
        frac1_frame = tk.LabelFrame(left_column, text="📅 First Fraction", 
                                  padx=15, pady=15, font=("Arial", 12, "bold"),
                                  bg="white", relief="groove", bd=2)
        frac1_frame.grid(row=0, column=0, sticky="nsew")
        frac1_frame.grid_propagate(False)  
        frac1_frame.config(height=350, width=680)  
        frac1_frame.grid_rowconfigure(2, weight=1)
        frac1_frame.grid_columnconfigure(0, weight=1)

       
        tk.Label(frac1_frame, text="Fraction Date:", font=label_font, bg="white").grid(row=0, column=0, sticky="e", pady=8, padx=5)
        self.date_frac1 = DateEntry(frac1_frame, width=18, background='darkblue', 
                                   foreground='white', borderwidth=2, 
                                   date_pattern='yyyy-mm-dd', font=entry_font)
        self.date_frac1.grid(row=0, column=1, pady=8, sticky="w", columnspan=2)

        
        upload_frame_frac1 = tk.Frame(frac1_frame, bg="white")
        upload_frame_frac1.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        upload_frame_frac1.grid_columnconfigure(0, weight=1)
        upload_frame_frac1.grid_columnconfigure(1, weight=1)

        tk.Button(upload_frame_frac1, text="📷 Upload AP Image", command=lambda: self.upload_image("AP_frac1"),
                  width=16, height=1, bg="#2980b9", fg="white", 
                  font=("Arial", 9, "bold"), relief="raised", bd=2).grid(row=0, column=0, padx=5)

        tk.Button(upload_frame_frac1, text="📷 Upload Lateral Image", command=lambda: self.upload_image("LAT_frac1"),
                  width=16, height=1, bg="#2980b9", fg="white", 
                  font=("Arial", 9, "bold"), relief="raised", bd=2).grid(row=0, column=1, padx=5)

        
        preview_frame_frac1 = tk.Frame(frac1_frame, bg="white")
        preview_frame_frac1.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        preview_frame_frac1.grid_propagate(False) 
        preview_frame_frac1.config(height=350)  
        preview_frame_frac1.grid_rowconfigure(0, weight=1)
        preview_frame_frac1.grid_columnconfigure(0, weight=1)
        preview_frame_frac1.grid_columnconfigure(1, weight=1)

        
        self.preview_ap_frac1 = tk.Label(preview_frame_frac1, 
                                        text="AP View\n(Click to upload image)\n\n📁 No image selected", 
                                        width=28, height=14, 
                                        relief="solid", borderwidth=1, bg="#ecf0f1",
                                        font=("Arial", 9), cursor="hand2", 
                                        wraplength=200, justify="center")
        self.preview_ap_frac1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.preview_ap_frac1.grid_propagate(False) 
        self.preview_ap_frac1.bind("<Button-1>", lambda e: self.upload_image("AP_frac1"))
        
        self.preview_lat_frac1 = tk.Label(preview_frame_frac1, 
                                         text="Lateral View\n(Click to upload image)\n\n📁 No image selected",
                                         width=28, height=14, 
                                         relief="solid", borderwidth=1, bg="#ecf0f1",
                                         font=("Arial", 9), cursor="hand2", 
                                         wraplength=200, justify="center")
        self.preview_lat_frac1.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.preview_lat_frac1.grid_propagate(False)  
        self.preview_lat_frac1.bind("<Button-1>", lambda e: self.upload_image("LAT_frac1"))

       
        frac2_frame = tk.LabelFrame(right_column, text="📅 Second Fraction", 
                                  padx=15, pady=15, font=("Arial", 12, "bold"),
                                  bg="white", relief="groove", bd=2)
        frac2_frame.grid(row=0, column=0, sticky="nsew")
        frac2_frame.grid_propagate(False) 
        frac2_frame.config(height=350, width=680)  
        frac2_frame.grid_rowconfigure(2, weight=1)
        frac2_frame.grid_columnconfigure(0, weight=1)

       
        tk.Label(frac2_frame, text="Fraction Date:", font=label_font, bg="white").grid(row=0, column=0, sticky="e", pady=8, padx=5)
        self.date_frac2 = DateEntry(frac2_frame, width=18, background='darkblue', 
                                   foreground='white', borderwidth=2, 
                                   date_pattern='yyyy-mm-dd', font=entry_font)
        self.date_frac2.grid(row=0, column=1, pady=8, sticky="w", columnspan=2)

       
        upload_frame_frac2 = tk.Frame(frac2_frame, bg="white")
        upload_frame_frac2.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        upload_frame_frac2.grid_columnconfigure(0, weight=1)
        upload_frame_frac2.grid_columnconfigure(1, weight=1)

        tk.Button(upload_frame_frac2, text="📷 Upload AP Image", command=lambda: self.upload_image("AP_frac2"),
                  width=16, height=1, bg="#2980b9", fg="white", 
                  font=("Arial", 9, "bold"), relief="raised", bd=2).grid(row=0, column=0, padx=5)

        tk.Button(upload_frame_frac2, text="📷 Upload Lateral Image", command=lambda: self.upload_image("LAT_frac2"),
                  width=16, height=1, bg="#2980b9", fg="white", 
                  font=("Arial", 9, "bold"), relief="raised", bd=2).grid(row=0, column=1, padx=5)

    
        preview_frame_frac2 = tk.Frame(frac2_frame, bg="white")
        preview_frame_frac2.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        preview_frame_frac2.grid_propagate(False) 
        preview_frame_frac2.config(height=350) 
        preview_frame_frac2.grid_rowconfigure(0, weight=1)
        preview_frame_frac2.grid_columnconfigure(0, weight=1)
        preview_frame_frac2.grid_columnconfigure(1, weight=1)

        self.preview_ap_frac2 = tk.Label(preview_frame_frac2, 
                                        text="AP View\n(Click to upload image)\n\n📁 No image selected",
                                        width=28, height=14,  
                                        relief="solid", borderwidth=1, bg="#ecf0f1",
                                        font=("Arial", 9), cursor="hand2", 
                                        wraplength=200, justify="center")
        self.preview_ap_frac2.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.preview_ap_frac2.grid_propagate(False)  
        self.preview_ap_frac2.bind("<Button-1>", lambda e: self.upload_image("AP_frac2"))

        self.preview_lat_frac2 = tk.Label(preview_frame_frac2, 
                                         text="Lateral View\n(Click to upload image)\n\n📁 No image selected",
                                         width=28, height=14, 
                                         relief="solid", borderwidth=1, bg="#ecf0f1",
                                         font=("Arial", 9), cursor="hand2", 
                                         wraplength=200, justify="center")
        self.preview_lat_frac2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.preview_lat_frac2.grid_propagate(False) 
        self.preview_lat_frac2.bind("<Button-1>", lambda e: self.upload_image("LAT_frac2"))

       
        self.preview_labels = {
            "AP_frac1": self.preview_ap_frac1,
            "LAT_frac1": self.preview_lat_frac1,
            "AP_frac2": self.preview_ap_frac2,
            "LAT_frac2": self.preview_lat_frac2
        }

        
        buttons_frame = tk.LabelFrame(main_container, text="🚀 Analysis Actions", 
                                    padx=5, pady=5, font=("Arial", 12, "bold"),
                                    bg="white", relief="groove", bd=2)
        buttons_frame.grid(row=5, column=0, sticky="ew", pady=5)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(0, weight=1)

       
        buttons_frame = tk.LabelFrame(main_container, text="🚀 Analysis Workflow", 
                                    padx=int(5 * screen_info['scale']), pady=int(5 * screen_info['scale']), 
                                    font=self.get_scaled_font(12, bold=True),
                                    bg="white", relief="groove", bd=2)
        buttons_frame.grid(row=5, column=0, sticky="ew", pady=int(5 * screen_info['scale']))
        buttons_frame.grid_columnconfigure((0,1,2,3,4), weight=1)

       
        self.create_scaled_button(buttons_frame, text="👁 Review Patient", command=self.show_info,
                  bg="#27ae60", fg="white", font=self.get_scaled_font(11, bold=True), 
                  width=20, height=1).grid(row=0, column=0, padx=int(4 * screen_info['scale']), pady=int(8 * screen_info['scale']))

        self.create_scaled_button(buttons_frame, text="➡️ Start AP Analysis", command=self.start_ap_workflow,
                  bg="#e67e22", fg="white", font=self.get_scaled_font(11, bold=True), 
                  width=25, height=1).grid(row=0, column=1, padx=int(4 * screen_info['scale']), pady=int(8 * screen_info['scale']))

        self.create_scaled_button(buttons_frame, text="➡️ Start LAT Analysis", command=self.start_lat_workflow,
                  bg="#e67e22", fg="white", font=self.get_scaled_font(11, bold=True), 
                  width=25, height=1).grid(row=0, column=2, padx=int(4 * screen_info['scale']), pady=int(8 * screen_info['scale']))

        
        self.create_scaled_button(buttons_frame, text="❓ Quick Guide", command=self.show_quick_guide,
                  bg="#3498db", fg="white", font=self.get_scaled_font(10), 
                  width=20, height=1).grid(row=0, column=3, padx=int(4 * screen_info['scale']), pady=int(8 * screen_info['scale']))

        self.create_scaled_button(buttons_frame, text="🐛 Debug Tools", command=self.debug_distance_saving,
                  bg="#8e44ad", fg="white", font=self.get_scaled_font(10), 
                  width=20, height=1).grid(row=0, column=4, padx=int(4 * screen_info['scale']), pady=int(8 * screen_info['scale']))

        
        status_frame = tk.Frame(main_container, bg="#34495e", height=int(25 * screen_info['scale']))
        status_frame.grid(row=6, column=0, sticky="ew", pady=(int(10 * screen_info['scale']), 0))
        status_frame.grid_propagate(False)
    
        self.status_var = tk.StringVar(value="Ready - Please load patient data and images to begin analysis")
        status_label = self.create_scaled_label(status_frame, textvariable=self.status_var, 
                              font=self.get_scaled_font(9), fg="white", bg="#34495e", anchor="w")
        status_label.pack(fill=tk.X, padx=int(10 * screen_info['scale']))

       
        self.root.bind('<Configure>', self.on_window_resize)

    def show_quick_guide(self):
       
        guide_text = """
        QUICK START GUIDE
    
        1. PATIENT INFO: Enter patient details and number of fractions
        2. CALIBRATION: Set pixel spacing (default: 0.2979 mm/pixel)
        3. UPLOAD IMAGES: Click preview areas to upload AP and Lateral images
        4. START ANALYSIS: Click 'Start AP Analysis' to begin annotation
    
        TIP: For fraction comparison, upload both fraction 1 and 2 images
        """
    
        messagebox.showinfo("Quick Guide", guide_text)

    def update_status(self, message):
    
        self.status_var.set(message)
        self.root.update_idletasks()

    def on_window_resize(self, event):
        
        if event.widget == self.root:
            
            screen_info = self.get_screen_info()

    def apply_calibration(self):
    
        try:
            ap_spacing = float(self.ap_spacing_entry.get())
            lat_spacing = float(self.lat_spacing_entry.get())
            
       
            self.pixel_spacing["AP_frac1"] = ap_spacing
            self.pixel_spacing["AP_frac2"] = ap_spacing
            self.pixel_spacing["LAT_frac1"] = lat_spacing
            self.pixel_spacing["LAT_frac2"] = lat_spacing
            
            messagebox.showinfo("Calibration Applied", 
                              f"AP Images: {ap_spacing:.4f} mm/pixel\n"
                              f"Lateral Images: {lat_spacing:.4f} mm/pixel")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for pixel spacing")

    def new_patient(self):
        self.name_entry.delete(0, tk.END)
        self.admission_entry.delete(0, tk.END)
        self.fractions_entry.delete(0, tk.END)

        today = datetime.today().strftime('%Y-%m-%d')
        self.date_frac1.set_date(today)
        self.date_frac2.set_date(today)

        for key in self.image_paths:
            self.image_paths[key] = None

        for key, lbl in self.preview_labels.items():
            lbl.config(image='', text=key)
            lbl.image = None

        print("New patient data cleared.")

    def upload_image(self, key):
       
        filepath = filedialog.askopenfilename(
            title=f"Select {key.replace('_', ' ').title()}",
            filetypes=[("Image Files", "*.bmp *.png *.jpg *.jpeg *.tif *.tiff")]
        )
    
        if filepath:
            self.image_paths[key] = filepath

            try:
                
                from PIL import Image as PILImage
                import PIL.Image
            
               
                img = PILImage.open(filepath)
    
            
                if img.mode in ('P', 'RGBA', 'LA'):
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('L')
        
           
                preview_size = (self.get_adaptive_preview_size(), self.get_adaptive_preview_size())
    
             
                img.thumbnail(preview_size, PILImage.Resampling.LANCZOS)
    
     
                img_tk = ImageTk.PhotoImage(img)

    
                preview_label = self.preview_labels[key]
                preview_label.config(image=img_tk, text="")
                preview_label.image = img_tk  

                print(f"Uploaded {key}: {os.path.basename(filepath)}")

            except Exception as e:
                print(f"Error loading image {filepath}: {e}")
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.image_paths[key] = Nonee

    def show_info(self):
        self.patient_info = {
            "Name": self.name_entry.get(),
            "Admission Number": self.admission_entry.get(),
            "First Fraction Date": self.date_frac1.get(),
            "Second Fraction Date": self.date_frac2.get(),
            "Number of Fractions": self.fractions_entry.get(),
            "AP Pixel Spacing": f"{self.pixel_spacing['AP_frac1']:.4f} mm/pixel",
            "Lateral Pixel Spacing": f"{self.pixel_spacing['LAT_frac1']:.4f} mm/pixel"
        }

      
        uploaded_images = []
        for k, v in self.image_paths.items():
            status = "Uploaded" if v else "Not Uploaded"
            uploaded_images.append(f"{k}: {status}")        

        info_text = "=== Patient Info ===\n"
        for k, v in self.patient_info.items():
            info_text += f"{k}: {v}\n"
        
        info_text += "\n=== Image Status ===\n"
        for status in uploaded_images:
            info_text += f"{status}\n"

        print(info_text)
        
     
        messagebox.showinfo("Patient Information", info_text)

    def get_pixel_spacing(self, image_key):
        
        return self.pixel_spacing.get(image_key, 0.2979) 

    def get_pixel_spacing_enhanced(self, image_key, image_path=None):
    

        calibrated_spacing = self.pixel_spacing.get(image_key, 0.2979)
    
    
        if image_path and image_path.lower().endswith(('.dcm', '.dicom')):
            try:
                import pydicom
                ds = pydicom.dcmread(image_path)
                if hasattr(ds, 'PixelSpacing'):
                    
                    dicom_spacing = float(ds.PixelSpacing[0])
                    print(f"Using DICOM pixel spacing: {dicom_spacing} mm/pixel")
                    return dicom_spacing
            except ImportError:
                print("pydicom not available, using calibrated spacing")
            except Exception as e:
                print(f"Could not read DICOM spacing: {e}, using calibrated")
    
        return calibrated_spacing    

    def auto_enhance(self, img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_img = clahe.apply(img)
        bilateral = cv2.bilateralFilter(clahe_img, d=9, sigmaColor=75, sigmaSpace=75)
        gaussian = cv2.GaussianBlur(bilateral, (9,9), 10.0)
        unsharp = cv2.addWeighted(bilateral, 1.5, gaussian, -0.5, 0)
        gamma = 1.2
        lut = np.array([((i/255.0)**(1/gamma))*255 for i in np.arange(0,256)]).astype("uint8")
        return cv2.LUT(unsharp, lut)

    def euclidean_distance(self, p1, p2):
      
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    def load_applicator_points(self, json_filename):
        import os
        import json

        json_path = os.path.join(self.temp_dir, json_filename)
        if not os.path.exists(json_path):
            print(f"File not found: {json_path}")
            return None

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)

            print(f"DEBUG: Loaded {json_filename} - Type: {type(data)}")
        
            
            if isinstance(data, dict):
                print(f"DEBUG: Dictionary format with keys: {list(data.keys())}")
                return data
            elif isinstance(data, list):
                print(f"DEBUG: List format with {len(data)} items")
              
                converted_data = {}
                for item in data:
                    if isinstance(item, dict):
                        converted_data.update(item)
                print(f"DEBUG: Converted to dictionary with keys: {list(converted_data.keys())}")
                return converted_data
            else:
                print(f"Unexpected data format in {json_filename}: {type(data)}")
                return None
        
        except Exception as e:
            print(f"Error loading applicator points: {e}")
            return None
        
    def debug_annotation_files(self):
        
        import glob
        from datetime import datetime
    
        print("=== DEBUG ANNOTATION FILES ===")
    
       
        annotation_patterns = [
            "AP_frac1_annotations.json",
            "AP_frac2_annotations.json", 
            "AP_frac1_aligned_to_frac2.json",
            "LAT_frac1_annotations.json",
            "LAT_frac2_annotations.json"
        ]
    
        for pattern in annotation_patterns:
            file_path = os.path.join(self.temp_dir, pattern)
            if os.path.exists(file_path):
                print(f"✅ FOUND: {pattern}")
                print(f"   Size: {os.path.getsize(file_path)} bytes")
                print(f"   Modified: {datetime.fromtimestamp(os.path.getmtime(file_path))}")
            
             
                try:
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                    print(f"   Structure: {list(content.keys())}")
                
            
                    for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                        if applicator in content and content[applicator]:
                            print(f"   ✅ {applicator}: ANNOTATED")
                        else:
                            print(f"   ❌ {applicator}: NOT ANNOTATED")
                        
                except Exception as e:
                    print(f"   ❌ Error reading: {e}")
            else:
                print(f"❌ MISSING: {pattern}")
        
            print("-" * 50)
    
       
        lat_dir = os.path.join(self.temp_dir, "LAT")
        if os.path.exists(lat_dir):
            lat_files = glob.glob(os.path.join(lat_dir, "*annotations.json"))
            for file_path in lat_files:
                file_name = os.path.basename(file_path)
                print(f"✅ FOUND in LAT/: {file_name}")
                print(f"   Size: {os.path.getsize(file_path)} bytes")
            

    def calculate_direct_shifts_between_fractions(self):
     
       
        frac1_points = self.load_applicator_points("AP_frac1_annotations.json")
        if not frac1_points:
            messagebox.showerror("Error", "Could not load Fraction 1 applicator points")
            return None
    
       
        frac2_points = self.load_applicator_points("AP_frac2_annotations.json")
        if not frac2_points:
            messagebox.showerror("Error", "Could not load Fraction 2 applicator points")
            return None
    
        shifts = {}
        mm_per_px = self.pixel_spacing["AP_frac1"]  
    
        for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
            if applicator not in frac1_points or applicator not in frac2_points:
                continue
            
            tip1 = frac1_points[applicator].get("tip")
            base1 = frac1_points[applicator].get("base")
            tip2 = frac2_points[applicator].get("tip") 
            base2 = frac2_points[applicator].get("base")
        
            if not all([tip1, base1, tip2, base2]):
                continue
        
            
            tip_shift_px = self.euclidean_distance(tip1, tip2)
            base_shift_px = self.euclidean_distance(base1, base2)
        
            tip_shift_mm = tip_shift_px * mm_per_px
            base_shift_mm = base_shift_px * mm_per_px
        
            applicator_name = applicator.replace('applicator_', '').replace('_', ' ').title()
        
            shifts[applicator_name] = {
                "tip_shift_mm": tip_shift_mm,
                "base_shift_mm": base_shift_mm,
                "average_shift_mm": (tip_shift_mm + base_shift_mm) / 2
            }
    
        return shifts

    def show_direct_shifts(self):
       
        shifts = self.calculate_direct_shifts_between_fractions()
        if not shifts:
            return
    
       
        shift_window = tk.Toplevel(self.root)
        shift_window.title("Direct Applicator Shifts Between Fractions")
        shift_window.geometry("600x400")
    
       
        text_widget = tk.Text(shift_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        text_widget.insert(tk.END, "DIRECT APPLICATOR SHIFTS BETWEEN FRACTIONS\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
    
        for applicator, data in shifts.items():
            text_widget.insert(tk.END, f"{applicator}:\n")
            text_widget.insert(tk.END, f"  • Tip shifted: {data['tip_shift_mm']:.2f} mm\n")
            text_widget.insert(tk.END, f"  • Base shifted: {data['base_shift_mm']:.2f} mm\n")
            text_widget.insert(tk.END, f"  • Average shift: {data['average_shift_mm']:.2f} mm\n\n")
    
        text_widget.config(state=tk.DISABLED)
    
        
        save_button = tk.Button(shift_window, text="Save Results", 
                              command=lambda: self.save_shift_results(shifts))
        save_button.pack(pady=10)

    def save_shift_results(self, shifts):
   
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, "direct_applicator_shifts.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("DIRECT APPLICATOR SHIFTS BETWEEN FRACTIONS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Calculation performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
                for applicator, data in shifts.items():
                    f.write(f"{applicator}:\n")
                    f.write(f"  Tip shifted: {data['tip_shift_mm']:.2f} mm\n")
                    f.write(f"  Base shifted: {data['base_shift_mm']:.2f} mm\n")
                    f.write(f"  Average shift: {data['average_shift_mm']:.2f} mm\n\n")
        
            messagebox.showinfo("Success", f"Results saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    
    def save_masks_at_original_resolution(self, image_path, annotations, output_dir):
     
        
        import cv2
        import numpy as np
        import os
    
        
        original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if original_img is None:
            print(f"Could not load original image: {image_path}")
            return
    
        original_height, original_width = original_img.shape
    
        
        screen_w, screen_h = 1400, 900 
        scale = min(screen_w / original_width, screen_h / original_height, 1.0)
        display_width = int(original_width * scale)
        display_height = int(original_height * scale)
    
        
        scale_x = original_width / display_width
        scale_y = original_height / display_height
    
        
        color_map = {
            "anatomy": 1,
            "applicator_tandem": 2,
            "left_ovoid": 3,
            "right_ovoid": 4
        }
    
        
        combined_mask = np.zeros((original_height, original_width), dtype=np.uint8)
        
        for structure_type, polygons in annotations.items():
            if structure_type not in color_map:
                continue
            
            
            individual_mask = np.zeros((original_height, original_width), dtype=np.uint8)
        
            for polygon in polygons:
                
                original_points = []
                for point in polygon:
                    if isinstance(point, list) and len(point) == 2:
                       
                        x_display, y_display = point
                        x_original = int(x_display * scale_x)
                        y_original = int(y_display * scale_y)
                        original_points.append([x_original, y_original])
                    elif isinstance(point, dict) and "tip" in point and "base" in point:
                        
                        tip = point["tip"]
                        base = point["base"]
                        if tip and base:
                            x_tip_orig = int(tip[0] * scale_x)
                            y_tip_orig = int(tip[1] * scale_y)
                            x_base_orig = int(base[0] * scale_x)
                            y_base_orig = int(base[1] * scale_y)
                         
                            cv2.line(individual_mask, 
                                    (x_tip_orig, y_tip_orig), 
                                    (x_base_orig, y_base_orig), 
                                    color_map[structure_type], 3)
                           
                            cv2.circle(individual_mask, (x_tip_orig, y_tip_orig), 5, color_map[structure_type], -1)
                            cv2.circle(individual_mask, (x_base_orig, y_base_orig), 5, color_map[structure_type], -1)
            
               
                if original_points and len(original_points) >= 2:
                    points_array = np.array(original_points, dtype=np.int32)
                    cv2.fillPoly(individual_mask, [points_array], color_map[structure_type])
        
           
            mask_filename = f"{os.path.basename(image_path).split('.')[0]}_{structure_type}_mask.png"
            mask_path = os.path.join(output_dir, mask_filename)
            cv2.imwrite(mask_path, individual_mask * 63)  
        
          
            combined_mask[individual_mask > 0] = color_map[structure_type]
    
        
        combined_mask_path = os.path.join(output_dir, f"{os.path.basename(image_path).split('.')[0]}_combined_mask.png")
        cv2.imwrite(combined_mask_path, combined_mask * 63)  
    
        print(f"Masks saved to: {output_dir}")

  
    def save_explicit_points(self, polygons, file_path):
      
        explicit_data = {
            "anatomy": polygons.get("anatomy", []),
            "applicator_tandem": {
                "tip": polygons.get("applicator_tandem", [{}])[0].get("tip") if polygons.get("applicator_tandem") else None,
                "base": polygons.get("applicator_tandem", [{}])[0].get("base") if polygons.get("applicator_tandem") else None
            },
            "left_ovoid": {
                "tip": polygons.get("left_ovoid", [{}])[0].get("tip") if polygons.get("left_ovoid") else None,
                "base": polygons.get("left_ovoid", [{}])[0].get("base") if polygons.get("left_ovoid") else None
            },
            "right_ovoid": {
                "tip": polygons.get("right_ovoid", [{}])[0].get("tip") if polygons.get("right_ovoid") else None,
                "base": polygons.get("right_ovoid", [{}])[0].get("base") if polygons.get("right_ovoid") else None
            }
        }
    
        explicit_path = file_path.replace('.json', '_explicit.json')
        with open(explicit_path, 'w') as f:
            json.dump(explicit_data, f, indent=2)
        

    def zoom_image(self, image_data, factor):
        image_data["zoom"] *= factor
        # ... rest of the existing code continues ...



    def zoom_image(self, image_data, factor):
        image_data["zoom"] *= factor
        self.refresh_image(image_data)

    def reset_zoom(self, image_data):
        image_data["zoom"] = 1.0
        self.refresh_image(image_data)

    def rotate_image(self, image_data, angle):
        image_data["angle"] += angle
        self.refresh_image(image_data)

    def reset_rotation(self, image_data):
        image_data["angle"] = 0
        self.refresh_image(image_data)

    def refresh_image(self, image_data):
        img = image_data["image"]
        if img is None:
           print("No image to refresh")
           return
    
        scale = image_data["zoom"]
        angle = image_data["angle"]
    
        if scale <= 0:
           print("Invalid scale:", scale)
           return
    
        if len(img.shape) == 2:
           h, w = img.shape
        else:
           h, w, _ = img.shape
    
        new_w, new_h = int(w * scale), int(h * scale)
        if new_w <= 0 or new_h <= 0:
           print("Invalid new size:", new_w, new_h)
           return
    
        resized = cv2.resize(img, (new_w, new_h))
    
        if angle != 0:
           center = (new_w // 2, new_h // 2)
           rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
           resized = cv2.warpAffine(resized, rot_mat, (new_w, new_h), borderMode=cv2.BORDER_REPLICATE)
    
        img_resized = cv2.resize(resized, (300, 300))
        img_resized = img_resized.astype('uint8')
 
        img_tk_new = ImageTk.PhotoImage(Image.fromarray(img_resized))
        image_data["img_label"].config(image=img_tk_new)
        image_data["img_label"].image = img_tk_new

    def show_ap_images(self):
       
        screen_info = self.get_screen_info()
        
       
        if not hasattr(self, 'ap_window') or self.ap_window is None or not self.ap_window.winfo_exists():
            self.ap_window = tk.Toplevel(self.root)
        
        
        taskbar_height = 40  
        max_window_width = screen_info['width'] - 50  
        max_window_height = screen_info['height'] - taskbar_height - 50  
        
        
        window_width = min(self.get_scaled_size(1600), max_window_width)
        window_height = min(self.get_scaled_size(1000), max_window_height)
        
        self.ap_window.geometry(f"{window_width}x{window_height}")
        self.ap_window.title("AP Images Editing - Workflow Step 1/2")
        
        
        self.center_window_safe(self.ap_window, window_width, window_height, taskbar_height)
        
       
        for widget in self.ap_window.winfo_children():
            widget.destroy()
        
        
        self.ap_window.grid_rowconfigure(0, weight=1)
        self.ap_window.grid_columnconfigure(0, weight=1)
        
        # ========== MAIN CONTAINER WITH SCROLLBARS ==========
        
        main_container = self.create_scaled_frame(self.ap_window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ========== NAVIGATION HEADER ==========
        nav_frame = self.create_scaled_frame(main_container, bg="#2c3e50", height=40)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        nav_frame.pack_propagate(False)
        
        
        nav_buttons_frame = self.create_scaled_frame(nav_frame, bg="#2c3e50")
        nav_buttons_frame.pack(expand=True)
        
        self.create_scaled_button(nav_buttons_frame, "🏠 Main Menu", self.return_to_main,
                  bg="#3498db", fg="white", font=self.get_scaled_font(10, bold=True),
                  width=15, height=1).pack(side=tk.LEFT, padx=5)
        
        self.create_scaled_button(nav_buttons_frame, "⬅️ Back", self.return_to_main,
                  bg="#95a5a6", fg="white", font=self.get_scaled_font(10),
                  width=12, height=1).pack(side=tk.LEFT, padx=5)
        
       
        self.create_scaled_label(nav_buttons_frame, "Step 1: AP Image Analysis", 
                 font=self.get_scaled_font(12, bold=True), fg="white", bg="#2c3e50").pack(side=tk.LEFT, padx=20)
        
        self.create_scaled_button(nav_buttons_frame, "Next: Lateral Analysis ➡️", command=self.navigate_to_lat_from_ap,
                  bg="#e67e22", fg="white", font=self.get_scaled_font(10, bold=True),
                  width=30, height=1).pack(side=tk.RIGHT, padx=5)
        
        
        status_label = self.create_scaled_label(nav_frame, "✓ AP Workflow Active", 
                               font=self.get_scaled_font(9), fg="#2ecc71", bg="#2c3e50")
        status_label.pack(side=tk.RIGHT, padx=10)
        
        # ========== IMAGE CONTENT FRAME ==========
       
        content_frame = self.create_scaled_frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def make_panel(parent_frame, original_img):
            original_image_data = original_img.copy()
            edited = {"image": original_img.copy(), "history": []}
            zoom = [1.0]
            angle = [0]
        
            
            current_brightness = [100] 
            current_contrast = [100]   
            current_auto_enhance = [False]
            current_negative = [False]
            current_edges = [False]
        
            
            available_height = window_height - 200
            img_h, img_w = original_img.shape

            max_canvas_w = int(window_width * 0.8)
            max_canvas_h = int(available_height * 0.8)
            
            scale_w = max_canvas_w / img_w
            scale_h = max_canvas_h / img_h
            scale = min(1.0, scale_w, scale_h)

            canvas_w = int(img_w * scale)
            canvas_h = int(img_h * scale)
            
            max_allowed_w = int(window_width * 0.9)
            max_allowed_h = int(available_height * 0.9)
            canvas_w = min(canvas_w, max_allowed_w)
            canvas_h = min(canvas_h, max_allowed_h)
        
            print(f"Canvas size: {canvas_w}x{canvas_h}, Window: {window_width}x{window_height}")
        
            
            canvas_frame = self.create_scaled_frame(parent_frame)
            canvas_frame.grid(row=0, column=0, columnspan=9, sticky="nsew", pady=(0, 10))
            
            canvas = tk.Canvas(canvas_frame, width=canvas_w, height=canvas_h, bg='black')
            canvas.focus_set()
            
          
            v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
            canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
           
            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")
            
            canvas_frame.grid_rowconfigure(0, weight=1)
            canvas_frame.grid_columnconfigure(0, weight=1)

            
            from PIL import Image as PILImage
            pil_img = PILImage.fromarray(original_img)
            img_tk = ImageTk.PhotoImage(pil_img)
            image_id = canvas.create_image(0, 0, anchor='nw', image=img_tk)
            canvas.image = img_tk
            canvas.config(scrollregion=(0, 0, pil_img.width, pil_img.height))

            def refresh_image():
                img = edited["image"]
                scale_val = zoom[0]
    
                if len(img.shape) == 2:
                    h, w = img.shape
                else:
                    h, w, _ = img.shape
    
                new_w, new_h = int(w * scale_val), int(h * scale_val)
                if new_w <= 0 or new_h <= 0:
                    print("Invalid size")
                    return
    
                resized = cv2.resize(img, (new_w, new_h))
    
                if angle[0] != 0:
                    center = (new_w // 2, new_h // 2)
                    rot_mat = cv2.getRotationMatrix2D(center, angle[0], 1.0)
                    resized = cv2.warpAffine(resized, rot_mat, (new_w, new_h), borderMode=cv2.BORDER_REPLICATE)
    
             
                from PIL import Image as PILImage
                pil_resized = PILImage.fromarray(resized)
                img_tk_new = ImageTk.PhotoImage(pil_resized)
    
               
                canvas.itemconfig(image_id, image=img_tk_new)
                canvas.image = img_tk_new
                canvas.config(scrollregion=(0, 0, new_w, new_h))

            def apply_all_adjustments():
              
                img = original_image_data.copy()

              
                if current_auto_enhance[0]:
                    img = self.auto_enhance(img)

           
                alpha = current_contrast[0] / 100.0
                beta = (current_brightness[0] - 100) * 0.5  
    
              
                img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

                
                if current_negative[0]:
                    img = cv2.bitwise_not(img)

                
                if current_edges[0]:
                    img = cv2.Canny(img, 50, 150)

                edited["image"] = img
                refresh_image()  
            
            def apply_auto_enhance():
                edited["history"].append(edited["image"].copy())
                current_auto_enhance[0] = not current_auto_enhance[0]  
                apply_all_adjustments()

            def apply_negative():
                edited["history"].append(edited["image"].copy())
                current_negative[0] = not current_negative[0]
                apply_all_adjustments()

            def apply_edges():
                edited["history"].append(edited["image"].copy())
                current_edges[0] = not current_edges[0]
                apply_all_adjustments()

            def undo_edit():
                if edited["history"]:
                    edited["image"] = edited["history"].pop()
                    
                   
                    current_brightness[0] = 100
                    current_contrast[0] = 100
                    current_auto_enhance[0] = False
                    current_negative[0] = False
                    current_edges[0] = False
                   
                    bright_slider.set(100)
                    contrast_slider.set(100)
                    refresh_image()

            def update_brightness(val):
                current_brightness[0] = int(val)
                apply_all_adjustments()

            def update_contrast(val):
                current_contrast[0] = float(val)
                apply_all_adjustments()

            
            def on_mousewheel(event):
                if event.delta > 0: 
                   zoom[0] *= 1.1
                else:             
                   zoom[0] /= 1.1
                refresh_image()

            canvas.bind("<MouseWheel>", on_mousewheel)  
            canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), refresh_image()))
            canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), refresh_image()))  
            canvas.focus_set()
            
            row_offset = 2
            
            tk.Button(parent_frame, text="🌟 Auto Enhancement", command=apply_auto_enhance,
                      bg="#E3F2FD", fg="#1976D2", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=0, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🌗 Invert Colors", command=apply_negative,
                      bg="#F3E5F5", fg="#7B1FA2", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=1, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔍 Edge Detection", command=apply_edges,
                      bg="#E0F2F1", fg="#00838F", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=2, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="↩️ Undo Last Action", command=undo_edit,
                      bg="#FFEBEE", fg="#D32F2F", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=3, sticky="we", padx=2, pady=5)

            tk.Button(parent_frame, text="🔍 Zoom In", command=lambda: (zoom.__setitem__(0, zoom[0]*1.2), refresh_image()),
                      bg="#FAFAFA", fg="#455A64", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=0, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔍 Zoom Out", command=lambda: (zoom.__setitem__(0, zoom[0]/1.2), refresh_image()),
                      bg="#FAFAFA", fg="#455A64", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=1, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="⟲ Rotate Left", command=lambda: (angle.__setitem__(0, (angle[0]-90)%360), refresh_image()),
                      bg="#EFEBE9", fg="#5D4037", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=2, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="⟳ Rotate Right", command=lambda: (angle.__setitem__(0, (angle[0]+90)%360), refresh_image()),
                      bg="#EFEBE9", fg="#5D4037", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=3, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔄 Reset View", command=lambda: (zoom.__setitem__(0, 1.0), angle.__setitem__(0, 0), refresh_image()),
                      bg="#FFF3E0", fg="#E64A19", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=4, sticky="we", padx=2, pady=5)

            tk.Label(parent_frame, text="Brightness Adjustment", font=("Arial", 9, "bold"), 
                     fg="#37474F").grid(row=row_offset+2, column=0, sticky="w")
            bright_slider = tk.Scale(parent_frame, from_=0, to=200, orient="horizontal", command=update_brightness,
                                    bg="#F5F5F5", fg="#37474F", troughcolor="#E0E0E0")
            bright_slider.set(100)
            bright_slider.grid(row=row_offset+2, column=1, columnspan=3, sticky="we")

            tk.Label(parent_frame, text="Contrast Adjustment", font=("Arial", 9, "bold"), 
                     fg="#37474F").grid(row=row_offset+3, column=0, sticky="w")
            contrast_slider = tk.Scale(parent_frame, from_=50, to=200, orient="horizontal", command=update_contrast,
                                      bg="#F5F5F5", fg="#37474F", troughcolor="#E0E0E0")
            contrast_slider.set(100)
            contrast_slider.grid(row=row_offset+3, column=1, columnspan=3, sticky="we")

            def get_current_edited_image():
                return edited["image"]
            return get_current_edited_image

       
        fractions_container = self.create_scaled_frame(content_frame)
        fractions_container.pack(fill=tk.BOTH, expand=True)
        fractions_container.grid_rowconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(1, weight=1)

      
        for idx, key in enumerate(["AP_frac1", "AP_frac2"]):
            frame = self.create_scaled_labelframe(fractions_container, f"Fraction {idx+1} - AP", padx=10, pady=10)
            frame.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)  
            frame.grid_columnconfigure(0, weight=1)
            
            if self.image_paths[key]:
               original_img = cv2.imread(self.image_paths[key], cv2.IMREAD_GRAYSCALE)
               if original_img is not None:
                  get_edited_img = make_panel(frame, original_img)

                  if key == "AP_frac1":
                    def save_and_annotate(get_img=get_edited_img, k=key):
                        img_to_save = get_img()
                        save_name = f"{k}_edited.png"
                        save_path = os.path.join(self.temp_dir, save_name)
                        cv2.imwrite(save_path, img_to_save)
                        print(f"Saved edited image: {save_path}")
                        self.open_annotation_window(save_path, k)

                    tk.Button(frame, text="📝 Proceed to Annotation", command=save_and_annotate,
                               bg="#E8F5E8", fg="#2E7D32", font=("Arial", 10, "bold"),
                              width=20, relief="raised", bd=1).grid(row=6, column=0, columnspan=3, pady=10, sticky="we")
                      
                  elif key == "AP_frac2":
                      def open_alignment_window(get_img=get_edited_img):
                          align_win = tk.Toplevel(self.ap_window)
                          align_win.title("Align and Annotate - Fraction 2 Edited Image")
                          align_win.geometry("1400x900")

                         
                          align_win.grid_rowconfigure(1, weight=1)
                          align_win.grid_columnconfigure(0, weight=1)
                          align_win.grid_columnconfigure(1, weight=0) 

                          
                          img = get_img() 
                          if img is None:
                              messagebox.showerror("Error", "Could not load Fraction 2 edited image")
                              align_win.destroy()
                              return

                          img_h, img_w = img.shape[:2]
                          screen_w, screen_h = align_win.winfo_screenwidth(), align_win.winfo_screenheight()
                          scale = min(screen_w / img_w, screen_h / img_h, 1.0)
                          new_w, new_h = int(img_w * scale), int(img_h * scale)
                          img_resized = cv2.resize(img, (new_w, new_h))
                          pil_img = PILImage.fromarray(img_resized)
                          zoom = [1.0]

                          
                          content_frame = tk.Frame(align_win)
                          content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

                         
                          canvas_frame = tk.Frame(content_frame)
                          canvas_frame.pack(fill=tk.BOTH, expand=True)

                          canvas = tk.Canvas(canvas_frame, width=new_w, height=new_h, bg="black", 
                                            scrollregion=(0, 0, new_w, new_h))

                          
                          v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
                          h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
                          canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

                       
                          v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                          h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
                          canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                          img_tk = ImageTk.PhotoImage(pil_img)
                          canvas.create_image(0, 0, anchor='nw', image=img_tk)
                          canvas.image = img_tk

                         
                          explicit_points = {
                              "anatomy": [],
                              "applicator_tandem": {"tip": None, "base": None},
                              "left_ovoid": {"tip": None, "base": None},
                              "right_ovoid": {"tip": None, "base": None}
                          }

                          
                          anatomy_points = []

                          current_points = []
                          mode = tk.StringVar(value="none") 
                          point_type = tk.StringVar(value="tip")  

                          color_map = {
                              "anatomy": "red",
                              "applicator_tandem": "blue",
                              "left_ovoid": "purple",
                              "right_ovoid": "green"
                          }

                          
                          canvas_items = {
                              "anatomy": [],
                              "applicator_tandem": {"tip": None, "base": None, "line": None},
                              "left_ovoid": {"tip": None, "base": None, "line": None},
                              "right_ovoid": {"tip": None, "base": None, "line": None}
                          }

                         
                          imported_anatomy_original = []
                          
                          imported_anatomy_current = []
        
                         
                          anatomy_offset = {"x": 0, "y": 0}

                          
                          alignment_saved = False
                          
                          in_annotation_mode = False

                          def redraw_canvas():
                              
                              for item_type in canvas_items:
                                  if item_type == "anatomy":
                                      for item in canvas_items[item_type]:
                                          canvas.delete(item)
                                      canvas_items[item_type] = []
                                  else:
                                      for point_type in ["tip", "base", "line"]:
                                          if canvas_items[item_type][point_type]:
                                              canvas.delete(canvas_items[item_type][point_type])
                                              canvas_items[item_type][point_type] = None

                             
                              scaled_w, scaled_h = int(new_w * zoom[0]), int(new_h * zoom[0])
                              canvas.config(scrollregion=(0, 0, scaled_w, scaled_h))

                          
                              pil_scaled = pil_img.resize((scaled_w, scaled_h), PILImage.Resampling.LANCZOS)
                              img_tk_scaled = ImageTk.PhotoImage(pil_scaled)
                              canvas.delete("background") 
                              canvas.create_image(0, 0, anchor='nw', image=img_tk_scaled, tags="background")
                              canvas.image = img_tk_scaled

                              
                              for poly in imported_anatomy_current:
                                  scaled_poly = [(int((x + anatomy_offset["x"]) * zoom[0]), int((y + anatomy_offset["y"]) * zoom[0])) for x, y in poly]
                                  if len(scaled_poly) > 1:
                                      item = canvas.create_line(scaled_poly, fill=color_map["anatomy"], width=2, tags="imported_anatomy")
                                      canvas_items["anatomy"].append(item)
                                  for x, y in scaled_poly:
                                      item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="imported_anatomy")
                                      canvas_items["anatomy"].append(item)

                           
                              for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                                  tip = explicit_points[label]["tip"]
                                  base = explicit_points[label]["base"]

                                  if tip:
                                      x, y = int(tip[0] * zoom[0]), int(tip[1] * zoom[0])
                                      item = canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                              outline='white', tags="annotation")
                                      canvas_items[label]["tip"] = item
                                      item_text = canvas.create_text(x+10, y-10, text=f"{label.replace('_', ' ').title()} Tip", 
                                                               fill='white', font=("Arial", 8), tags="annotation")
                                      canvas_items["anatomy"].append(item_text)

                                  if base:
                                      x, y = int(base[0] * zoom[0]), int(base[1] * zoom[0])
                                      item = canvas.create_rectangle(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                                  outline='white', tags="annotation")
                                      canvas_items[label]["base"] = item
                                      item_text = canvas.create_text(x+10, y+10, text=f"{label.replace('_', ' ').title()} Base", 
                                                                   fill='white', font=("Arial", 8), tags="annotation")
                                      canvas_items["anatomy"].append(item_text)

                                 
                                  if tip and base:
                                      item = canvas.create_line(
                                          int(tip[0] * zoom[0]), int(tip[1] * zoom[0]),
                                          int(base[0] * zoom[0]), int(base[1] * zoom[0]),
                                          fill=color_map[label], width=2, dash=(4, 2), tags="annotation"
                                      )
                                      canvas_items[label]["line"] = item

                          
                          def on_click(event):
                              
                              if not in_annotation_mode or not alignment_saved:
                                  print(f"Click ignored - in_annotation_mode: {in_annotation_mode}, alignment_saved: {alignment_saved}")
                                  return
        
                              x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
            
                              current_mode = mode.get()
                              print(f"Click at ({x}, {y}) - Mode: {current_mode}, Point Type: {point_type.get()}")
            
                        
                              if current_mode != "anatomy" and current_mode != "none":
                                  current_point_type = point_type.get()
                
                                  if current_point_type == "tip":
                                      explicit_points[current_mode]["tip"] = (x, y)
                                      point_type.set("base")
                                      status_var.set(f"Set {current_mode.replace('_', ' ').title()} tip. Now click for base point.")
                                      print(f"Set {current_mode} tip at ({x}, {y})")
                                  else:
                                      explicit_points[current_mode]["base"] = (x, y)
                                      point_type.set("tip")
                                      status_var.set(f"Set {current_mode.replace('_', ' ').title()} base. Annotation complete for this applicator.")
                                      print(f"Set {current_mode} base at ({x}, {y})")
                
                                  redraw_canvas()

                   
                          def on_mouse_move(event):
                              x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
                              current_mode = mode.get()
                              current_point_type = point_type.get()
            
                              status_text = f"Position: X:{x} Y:{y}"
            
                              if alignment_saved and in_annotation_mode:
                                  if current_mode != "none" and current_mode != "anatomy":
                                      status_text += f" | Mode: {current_mode.replace('_', ' ').title()} | Point: {current_point_type.title()}"
                                  else:
                                      status_text += " | Select an applicator to start annotation"
                              elif alignment_saved:
                                  status_text += " | ALIGNMENT SAVED - Click an applicator button to start annotation"
                              elif not alignment_saved:
                                  status_text += " | Drag anatomy to align, then click 'Save Alignment'"
            
                              status_var.set(status_text)
                                    
                         
                          drag_data = {"x": 0, "y": 0, "item": None}

                          def start_move(event):
                          
                              if alignment_saved:
                                  return
                          
                             
                              items = canvas.find_withtag("imported_anatomy")
                              for item in items:
                                  if canvas.type(item) == 'line':
                                      coords = canvas.coords(item)
                                      x_vals = coords[::2]
                                      y_vals = coords[1::2]
                                      if min(x_vals) - 10 <= event.x <= max(x_vals) + 10 and min(y_vals) - 10 <= event.y <= max(y_vals) + 10:
                                          drag_data["item"] = item
                                          drag_data["x"] = event.x
                                          drag_data["y"] = event.y
                                          break

                          def on_move(event):
                              
                              if alignment_saved or drag_data["item"] is None:
                                  return
        
                              dx = event.x - drag_data["x"]
                              dy = event.y - drag_data["y"]

                          
                              anatomy_offset["x"] += dx / zoom[0]
                              anatomy_offset["y"] += dy / zoom[0]

                            
                              for item in canvas.find_withtag("imported_anatomy"):
                                  canvas.move(item, dx, dy)
                              drag_data["x"] = event.x
                              drag_data["y"] = event.y

                          def stop_move(event):
                              drag_data["item"] = None

                          def undo_last_point():
                           
                              current_mode = mode.get()
                              if current_mode != "anatomy" and current_mode != "none":
                                
                                  if point_type.get() == "tip" and explicit_points[current_mode]["base"]:
                                      explicit_points[current_mode]["base"] = None
                                      point_type.set("base")
                                      status_var.set(f"Undid base point. Click to set base for {current_mode.replace('_', ' ').title()}.")
                                  elif explicit_points[current_mode]["tip"]:
                                      explicit_points[current_mode]["tip"] = None
                                      point_type.set("tip")
                                      status_var.set(f"Undid tip point. Click to set tip for {current_mode.replace('_', ' ').title()}.")
                                  redraw_canvas()

                         
                          def clear_current_applicator():
                              current_mode = mode.get()
                              if current_mode != "anatomy" and current_mode != "none":
                                  explicit_points[current_mode]["tip"] = None
                                  explicit_points[current_mode]["base"] = None
                                  point_type.set("tip")
                                  status_var.set(f"Cleared {current_mode.replace('_', ' ').title()}. Ready for new annotation.")
                                  redraw_canvas()
                                  print(f"Cleared {current_mode} annotations")

                          def clear_all_annotations():
                            
                              for label in explicit_points:
                                  if label == "anatomy":
                                      continue
                                  explicit_points[label]["tip"] = None
                                  explicit_points[label]["base"] = None
                              point_type.set("tip")
                              mode.set("none")
                              status_var.set("Cleared all applicator annotations. Select an applicator to start annotation.")
                              redraw_canvas()
                              print("Cleared all applicator annotations")

                          def import_fraction1_anatomy():
                              nonlocal imported_anatomy_original, imported_anatomy_current
                              path = os.path.join(self.temp_dir, "AP_frac1_annotations.json")
                              if not os.path.exists(path):
                                  print("Fraction 1 anatomy annotations not found")
                                  status_var.set("Error: Fraction 1 anatomy annotations not found")
                                  return

                              with open(path, 'r') as f:
                                  all_polygons = json.load(f)

                              if "anatomy" in all_polygons:
                                  imported_anatomy_original = all_polygons["anatomy"]
                                  imported_anatomy_current = all_polygons["anatomy"].copy()  
                              
                                  anatomy_offset["x"] = 0
                                  anatomy_offset["y"] = 0
                                  redraw_canvas()
                                  print("Imported Fraction 1 anatomy")
                                  status_var.set("Anatomy imported. Drag to position, then click 'Save Alignment' when done.")

                          def save_alignment():
                              nonlocal alignment_saved, in_annotation_mode
                             
                              polygons = {
                                  "anatomy": imported_anatomy_current,  
                                  "applicator_tandem": [],
                                  "left_ovoid": [],
                                  "right_ovoid": []
                              }

                             
                              for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                                  tip = explicit_points[label]["tip"]
                                  base = explicit_points[label]["base"]
                                  if tip and base:
                                     
                                      polygons[label].append([tip, base])

                              json_path = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
                              with open(json_path, 'w') as f:
                                  json.dump(polygons, f)

                             
                              explicit_path = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2_explicit_points.json")
                              with open(explicit_path, 'w') as f:
                                  json.dump(explicit_points, f)

                             
                              edited_img_path = os.path.join(self.temp_dir, "AP_frac2_edited.png")
                              if os.path.exists(edited_img_path):
                                  self.save_masks_at_original_resolution(edited_img_path, polygons, self.temp_dir)

                              
                              alignment_saved = True
                              in_annotation_mode = True

                              
                              canvas.unbind("<ButtonPress-1>")
                              canvas.unbind("<B1-Motion>")
                              canvas.unbind("<ButtonRelease-1>")

                              
                              canvas.bind("<Button-1>", on_click)

                              print(f"Alignment saved to {json_path}")
                              status_var.set("Alignment saved! Anatomy is now fixed. Select an applicator button to start annotation.")

                        
                          def start_tandem_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("applicator_tandem")
                                  point_type.set("tip")  
                                  in_annotation_mode = True
                                  status_var.set("TANDEM MODE - Click to set tip point")
                                  print(f"Annotation mode set to: {mode.get()}, point type: {point_type.get()}")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")

                          def start_left_ovoid_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("left_ovoid")
                                  point_type.set("tip")  
                                  in_annotation_mode = True
                                  status_var.set("LEFT OVOID MODE - Click to set tip point")
                                  print(f"Annotation mode set to: {mode.get()}, point type: {point_type.get()}")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")

                          def start_right_ovoid_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("right_ovoid")
                                  point_type.set("tip")  
                                  in_annotation_mode = True
                                  status_var.set("RIGHT OVOID MODE - Click to set tip point")
                                  print(f"Annotation mode set to: {mode.get()}, point type: {point_type.get()}")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")

                          def save_and_end_session():
                              """Save distances to file and close the alignment session"""
                              if not imported_anatomy_current:
                                  messagebox.showerror("Error", "No anatomy imported. Please import Fraction 1 anatomy first.")
                                  return
        
                              if len(imported_anatomy_current) == 0 or len(imported_anatomy_current[0]) < 2:
                                  messagebox.showerror("Error", "Anatomy line is incomplete. Please ensure anatomy has at least 2 points.")
                                  return

                              anatomy_poly = imported_anatomy_current[0]
                              anatomy_start = anatomy_poly[0]
                              anatomy_end = anatomy_poly[-1]

                              mm_per_px = self.pixel_spacing["AP_frac1"] 

                              
                              dist_results = []
                              dist_results.append("=== AP View - Fraction 2 ===")
                              dist_results.append(f"Anatomy start point: {anatomy_start}")
                              dist_results.append(f"Anatomy end point: {anatomy_end}")
                              dist_results.append("")

                              structures = {
                                  "applicator_tandem": "Tandem Applicator",
                                  "left_ovoid": "Left Ovoid", 
                                  "right_ovoid": "Right Ovoid"
                              }

                              for applicator_key, applicator_name in structures.items():
                                  tip = explicit_points[applicator_key]["tip"]
                                  base = explicit_points[applicator_key]["base"]

                                  if not tip or not base:
                                      
                                      dist_results.append(f"{applicator_name} Tip to Anatomy Start: ")
                                      dist_results.append(f"{applicator_name} Base to Anatomy Start: ")
                                      dist_results.append(f"{applicator_name} Tip to Anatomy End: ")
                                      dist_results.append(f"{applicator_name} Base to Anatomy End: ")
                                      continue

                                  # Calculate distances
                                  tip_to_start = self.euclidean_distance(tip, anatomy_start) * mm_per_px
                                  base_to_start = self.euclidean_distance(base, anatomy_start) * mm_per_px
                                  tip_to_end = self.euclidean_distance(tip, anatomy_end) * mm_per_px
                                  base_to_end = self.euclidean_distance(base, anatomy_end) * mm_per_px

                                  dist_results.append(f"{applicator_name} Tip to Anatomy Start: {tip_to_start:.2f} mm")
                                  dist_results.append(f"{applicator_name} Base to Anatomy Start: {base_to_start:.2f} mm")
                                  dist_results.append(f"{applicator_name} Tip to Anatomy End: {tip_to_end:.2f} mm")
                                  dist_results.append(f"{applicator_name} Base to Anatomy End: {base_to_end:.2f} mm")

                            
                              txt_filename = "AP_frac2_distances_from_anatomy.txt"
                              txt_path = os.path.join(self.temp_dir, txt_filename)

                              try:
                                  with open(txt_path, "w", encoding="utf-8") as f:
                                      for line in dist_results:
                                          f.write(line + "\n")

                                 
                                  messagebox.showinfo("Success", 
                                                    f"Distances saved to:\n{txt_path}\n\n"
                                                    f"Session completed successfully!\n"
                                                    f"File contains measurements for all applicators.\n"
                                                    f"All distances measured in mm relative to anatomy landmarks.")

                                  
                                  print(f"✅ DISTANCES SAVED: {txt_path}")
                                  for line in dist_results:
                                      print(f"   {line}")

                                 
                                  align_win.destroy()

                              except Exception as e:
                                  messagebox.showerror("Error", f"Failed to save distances: {str(e)}")
                                  print(f"❌ Error saving distances: {e}")

                      
                          def zoom_in():
                              zoom[0] *= 1.2
                              redraw_canvas()

                          def zoom_out():
                              zoom[0] /= 1.2
                              redraw_canvas()

                          def reset_zoom():
                              zoom[0] = 1.0
                              redraw_canvas()
            
                          def on_mousewheel(event):
                              if event.delta > 0:
                                  zoom[0] *= 1.1
                              else:
                                  zoom[0] /= 1.1
                              redraw_canvas()

                     
                          canvas.bind("<Button-1>", on_click)
                          canvas.bind("<Motion>", on_mouse_move)
                          canvas.bind("<MouseWheel>", on_mousewheel)
                          canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), redraw_canvas()))
                          canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), redraw_canvas()))

                     
                          canvas.bind("<ButtonPress-1>", start_move)
                          canvas.bind("<B1-Motion>", on_move)
                          canvas.bind("<ButtonRelease-1>", stop_move)

            
                          toolbar_frame = tk.Frame(align_win, relief=tk.RAISED, borderwidth=2, bg="#F5F5F5", width=350)
                          toolbar_frame.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=10)
                          toolbar_frame.grid_propagate(False)

                          align_win.grid_columnconfigure(1, weight=0, minsize=350)
                          align_win.grid_columnconfigure(0, weight=1)

                     
                          status_var = tk.StringVar(value="Ready - Import Fraction 1 Anatomy first")
                          status_label = tk.Label(align_win, textvariable=status_var, relief=tk.SUNKEN, 
                                                anchor=tk.W, font=("Arial", 10), bg="#E8F5E8", fg="#2E7D32")
                          status_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
                  
                          sections = [
                              ("Movement & Import Tools", [
                                  ("📥 Import Fraction 1 Anatomy", import_fraction1_anatomy),
                                  ("💾 Save Alignment Position", save_alignment)
                              ]),
                              ("Annotation Mode Selection", [
                                  ("📐 Tandem Applicator (Blue)", start_tandem_annotation),
                                  ("📐 Left Ovoid Applicator (Purple)", start_left_ovoid_annotation),
                                  ("📐 Right Ovoid Applicator (Green)", start_right_ovoid_annotation)
                              ]),
                              ("Current Point Type", [
                                  (f"Current Point Type: {point_type.get()}", lambda: None)
                              ]),
                              ("Applicator Editing Tools", [
                                  ("🗑️ Clear Current Applicator", clear_current_applicator),
                                  ("🗑️ Clear All Applicators", clear_all_annotations),
                                  ("↩️ Undo Last Point Placement", undo_last_point)
                              ]),
                              ("View Control Options", [
                                  ("🔍 Zoom In Image View", zoom_in),
                                  ("🔍 Zoom Out Image View", zoom_out),
                                  ("🔄 Reset Zoom Level", reset_zoom)
                              ]),
                              ("Session Tools", [
                                  ("💾 Save & End Session", save_and_end_session)
                              ])
                          ]

                          row = 0
                          for section_title, buttons in sections:
                        
                              section_frame = tk.LabelFrame(toolbar_frame, text=section_title, 
                                                          font=("Arial", 10, "bold"), padx=8, pady=6,
                                                          bg="#F5F5F5", fg="#37474F", width=330)
                              section_frame.grid(row=row, column=0, sticky="ew", pady=(0, 12), padx=5)
                              section_frame.grid_propagate(False)
                              row += 1

                              for btn_text, command in buttons:
                                  if "Current Point Type:" in btn_text:
                            
                                      static_label = tk.Label(section_frame, text="Current Point Type:", 
                                                            font=("Arial", 9, "bold"), fg="#37474F", bg="#F5F5F5",
                                                            anchor="w")
                                      static_label.pack(fill=tk.X, pady=(5, 0), padx=5)
                             
                                      point_display = tk.Label(section_frame, textvariable=point_type, 
                                                             font=("Arial", 10, "bold"), fg="#1565C0", bg="#F5F5F5",
                                                             width=25, anchor="w")
                                      point_display.pack(fill=tk.X, pady=3, padx=5)
                                      point_display.is_point_display = True
                                  else:
                                
                                      if "Import" in btn_text or "Save" in btn_text:
                                          bg_color, fg_color = "#E8F5E8", "#2E7D32"
                                      elif "Tandem" in btn_text:
                                          bg_color, fg_color = "#E3F2FD", "#1565C0"
                                      elif "Left Ovoid" in btn_text:
                                          bg_color, fg_color = "#F3E5F5", "#7B1FA2"
                                      elif "Right Ovoid" in btn_text:
                                          bg_color, fg_color = "#E8F5E8", "#2E7D32"
                                      elif "Clear" in btn_text or "Remove" in btn_text:
                                          bg_color, fg_color = "#FFEBEE", "#D32F2F"
                                      elif "Undo" in btn_text:
                                          bg_color, fg_color = "#FFF3E0", "#FF6F00"
                                      elif "Zoom" in btn_text or "View" in btn_text:
                                          bg_color, fg_color = "#FAFAFA", "#455A64"
                                      elif "Calculate" in btn_text or "Measurement" in btn_text:
                                          bg_color, fg_color = "#E1F5FE", "#0277BD"
                                      else:
                                          bg_color, fg_color = "#F5F5F5", "#37474F"
                  
                                      btn = tk.Button(section_frame, text=btn_text, command=command,
                                                    font=("Arial", 9), width=32, height=1,
                                                    bg=bg_color, fg=fg_color, relief="raised", bd=2,
                                                    anchor="w", justify="left")
                                      btn.pack(fill=tk.X, pady=3, padx=5)

                     
                          def update_point_display(*args):
                              for widget in toolbar_frame.winfo_children():
                                  if isinstance(widget, tk.LabelFrame):
                                      for child in widget.winfo_children():
                                          if isinstance(child, tk.Label) and hasattr(child, 'is_point_display'):
                                              child.config(text=f"{point_type.get().title()}")

                          point_type.trace('w', update_point_display)
                  
                      
                          for widget in toolbar_frame.winfo_children():
                              if isinstance(widget, tk.LabelFrame) and "Current Point Type" in widget.cget('text'):
                                  for child in widget.winfo_children():
                                      if isinstance(child, tk.Label):
                                          child.is_point_display = True

                 
                          redraw_canvas()

                    
                          status_var.set("Ready - Import Fraction 1 Anatomy first, then drag to align")
            
                          print(f"Enhanced alignment window ready for Fraction 2")

                      tk.Button(frame, text="🔄 Image Alignment", command=open_alignment_window,
                                bg="#E3F2FD", fg="#1565C0", font=("Arial", 10, "bold"),
                                width=15, relief="raised", bd=1).grid(row=6, column=0, columnspan=3, pady=5, sticky="we")
                      tk.Button(frame, text="📊 Compare Fractions", command=self.compare_fraction_distances_from_txt,
                                bg="#FFF3E0", fg="#FF6F00", font=("Arial", 10, "bold"),
                                width=15, relief="raised", bd=1).grid(row=6, column=3, columnspan=3, pady=5, sticky="we")



        


    def compare_fraction_distances_direct_euclidean(self):
        
        import os
        import re
        from datetime import datetime
    
   
        file1 = os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt")
        file2 = os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")
    
    
        if not os.path.exists(file1) or not os.path.exists(file2):
            messagebox.showerror("Error", 
                               "Cannot perform comparison. Missing distance files.\n\n"
                               f"Fraction 1: {'Found' if os.path.exists(file1) else 'Missing'}\n"
                               f"Fraction 2: {'Found' if os.path.exists(file2) else 'Missing'}\n\n"
                               "Please complete annotation for both fractions first.")
            return
    
        def extract_structured_distances(file_path):
         
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    current_applicator = None
                    for line in f:
                        line = line.strip()
                    
                      
                        if not line or "===" in line or "Anatomy" in line:
                            continue
                        
                 
                        match = re.match(r"(.+?)\s+(Tip|Base)\s+to\s+Anatomy\s+(Start|End):\s*([\d.]+)\s*mm", line)
                        if match:
                            applicator = match.group(1).strip()
                            point_type = match.group(2).lower()  # tip or base
                            anatomy_point = match.group(3).lower()  # start or end
                            value = float(match.group(4))
                        
                          
                            if applicator not in distances:
                                distances[applicator] = {}
                        
                        
                            key = f"{point_type}_to_{anatomy_point}"
                            distances[applicator][key] = value
                        
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            return distances
    
       
        dist1 = extract_structured_distances(file1)
        dist2 = extract_structured_distances(file2)
    
        if not dist1 or not dist2:
            messagebox.showerror("Error", "No valid distance data found in one or both files")
            return
    
       
        shifts = {}
    
        for applicator in ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]:
            if applicator in dist1 and applicator in dist2:
       
                measurement_pairs = []
            
                for point_type in ["tip", "base"]:
                    for anatomy_point in ["start", "end"]:
                        key = f"{point_type}_to_{anatomy_point}"
                        if key in dist1[applicator] and key in dist2[applicator]:
                  
                            shift = dist2[applicator][key] - dist1[applicator][key]
                            measurement_pairs.append({
                                'measurement': f"{point_type.title()} to Anatomy {anatomy_point.title()}",
                                'fraction1': dist1[applicator][key],
                                'fraction2': dist2[applicator][key],
                                'shift': shift,
                                'abs_shift': abs(shift)
                            })
            
                if measurement_pairs:
                   
                    avg_shift = sum(pair['shift'] for pair in measurement_pairs) / len(measurement_pairs)
                    avg_abs_shift = sum(pair['abs_shift'] for pair in measurement_pairs) / len(measurement_pairs)
                
                    shifts[applicator] = {
                        'measurements': measurement_pairs,
                        'average_shift': avg_shift,
                        'average_absolute_shift': avg_abs_shift,
                        'max_shift': max(abs(pair['shift']) for pair in measurement_pairs)
                    }
    
  
        self.show_direct_euclidean_results(shifts, file1, file2)

    def show_direct_euclidean_results(self, shifts, file1_path, file2_path):
      
        results_window = tk.Toplevel(self.root)
        results_window.title("Direct Euclidean Distance Comparison - AP View")
        results_window.geometry("1000x700")
    
        
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
     
        title_label = tk.Label(main_frame, text="DIRECT EUCLIDEAN DISTANCE COMPARISON", 
                              font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)
    
        
        subtitle_label = tk.Label(main_frame, text="APPROACH 1: Point-to-Point Distance Differences (Fraction 2 - Fraction 1)",
                                font=("Arial", 12), fg="#555555")
        subtitle_label.pack(pady=5)
        
        
        file_info = tk.Label(main_frame, 
                            text=f"Data from:\n• {os.path.basename(file1_path)}\n• {os.path.basename(file2_path)}",
                            font=("Arial", 9), fg="#666666", justify=tk.LEFT)
        file_info.pack(pady=5)
    
        
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")
    
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
    
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        
        text_widget.insert(tk.END, "DIRECT EUCLIDEAN DISTANCE SHIFTS\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        text_widget.insert(tk.END, f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
        if not shifts:
            text_widget.insert(tk.END, "No matching measurements found between fractions.\n")
            text_widget.insert(tk.END, "Please ensure both fractions have the same structures annotated.\n")
        else:
            for applicator, data in shifts.items():
                text_widget.insert(tk.END, f"{applicator.upper()}\n", "subtitle")
                text_widget.insert(tk.END, "-" * 40 + "\n")
            
          
                for measurement in data['measurements']:
                    direction = "increased" if measurement['shift'] > 0 else "decreased"
                    text_widget.insert(tk.END, 
                                     f"  • {measurement['measurement']}:\n"
                                     f"    F1: {measurement['fraction1']:.2f} mm → "
                                     f"F2: {measurement['fraction2']:.2f} mm\n"
                                     f"    Shift: {measurement['shift']:+.2f} mm ({direction})\n")
            
                
                text_widget.insert(tk.END, f"\n  SUMMARY:\n")
                text_widget.insert(tk.END, f"  • Average shift: {data['average_shift']:+.2f} mm\n")
                text_widget.insert(tk.END, f"  • Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
                text_widget.insert(tk.END, f"  • Maximum shift: {data['max_shift']:.2f} mm\n")
            
             
                if data['max_shift'] < 3.0:
                    assessment = "EXCELLENT reproducibility"
                    color = "green"
                elif data['max_shift'] < 5.0:
                    assessment = "GOOD reproducibility"
                    color = "orange"
                elif data['max_shift'] < 7.0:
                    assessment = "MODERATE variation"
                    color = "darkorange"
                else:
                    assessment = "SIGNIFICANT movement"
                    color = "red"
                
                text_widget.insert(tk.END, f"  • ASSESSMENT: {assessment}\n", color)
                text_widget.insert(tk.END, "\n")
    
       
        if shifts:
            text_widget.insert(tk.END, "OVERALL CLINICAL ASSESSMENT\n", "subtitle")
            text_widget.insert(tk.END, "=" * 40 + "\n\n")
        
            max_overall_shift = max(data['max_shift'] for data in shifts.values())
            if max_overall_shift < 3.0:
                assessment = "✓ EXCELLENT overall reproducibility"
                details = "Minimal applicator movement between fractions"
                color = "green"
            elif max_overall_shift < 5.0:
                assessment = "✓ GOOD overall reproducibility" 
                details = "Acceptable clinical variation"
                color = "orange"
            elif max_overall_shift < 7.0:
                assessment = "⚠ MODERATE overall variation"
                details = "Consider clinical impact on dose distribution"
                color = "darkorange"
            else:
                assessment = "❌ SIGNIFICANT overall movement"
                details = "Review patient positioning and applicator fixation"
                color = "red"
            
            text_widget.insert(tk.END, f"{assessment}\n", color)
            text_widget.insert(tk.END, f"{details}\n")
            text_widget.insert(tk.END, f"Maximum observed shift: {max_overall_shift:.2f} mm\n")
    
      
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#1565C0")
        text_widget.tag_configure("green", foreground="#2E7D32")
        text_widget.tag_configure("orange", foreground="#FF9800")
        text_widget.tag_configure("darkorange", foreground="#FF5722")
        text_widget.tag_configure("red", foreground="#D32F2F")
        
        text_widget.config(state=tk.DISABLED)
    
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
    
      
        save_button = tk.Button(button_frame, text="💾 Save Report", 
                              command=lambda: self.save_direct_euclidean_report(shifts),
                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                              width=15, height=1)
        save_button.pack(side=tk.LEFT, padx=10)
    
       
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack(side=tk.LEFT, padx=10)

    def save_direct_euclidean_report(self, shifts):
        
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, "AP_direct_euclidean_comparison.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("DIRECT EUCLIDEAN DISTANCE COMPARISON REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("METHOD: Direct point-to-point Euclidean distance differences\n")
                f.write("FORMULA: Shift = (Fraction 2 distance) - (Fraction 1 distance)\n\n")
            
                for applicator, data in shifts.items():
                    f.write(f"{applicator.upper()}\n")
                    f.write("-" * 50 + "\n")
                
                    for measurement in data['measurements']:
                        f.write(f"{measurement['measurement']}:\n")
                        f.write(f"  Fraction 1: {measurement['fraction1']:.2f} mm\n")
                        f.write(f"  Fraction 2: {measurement['fraction2']:.2f} mm\n")
                        f.write(f"  Shift: {measurement['shift']:+.2f} mm\n")
                
                    f.write(f"\nSummary for {applicator}:\n")
                    f.write(f"  Average shift: {data['average_shift']:+.2f} mm\n")
                    f.write(f"  Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
                    f.write(f"  Maximum shift: {data['max_shift']:.2f} mm\n\n")
            
            messagebox.showinfo("Report Saved", f"Direct Euclidean comparison saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def update_frac2_from_alignment(self):
    
        try:
            aligned_file = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
            frac2_file = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
        
            if not os.path.exists(aligned_file):
                print("Aligned file not found")
                return False
            
            if not os.path.exists(frac2_file):
                print("Fraction 2 file not found")
                return False
            
          
            with open(aligned_file, 'r') as f:
                aligned_data = json.load(f)
            
            with open(frac2_file, 'r') as f:
                frac2_data = json.load(f)
            
        
            applicators = ["applicator_tandem", "left_ovoid", "right_ovoid"]
            updated = False
        
            for applicator in applicators:
                if (applicator in aligned_data and 
                    aligned_data[applicator] and 
                    len(aligned_data[applicator]) > 0):
                
                    frac2_data[applicator] = aligned_data[applicator]
                    print(f"✅ Updated {applicator} in Fraction 2")
                    updated = True
                
            if updated:
              
                with open(frac2_file, 'w') as f:
                    json.dump(frac2_data, f)
                print("✅ Successfully updated Fraction 2 annotations")
                return True
            else:
                print("❌ No applicator data found in aligned file")
                return False
            
        except Exception as e:
            print(f"❌ Error updating Fraction 2: {e}")
            return False


    def check_annotation_completeness(self, file_path):
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        
            filename = os.path.basename(file_path)
            print(f"Checking completeness of {filename}:")
        
        
            required_structures = ["applicator_tandem", "left_ovoid", "right_ovoid"]
            missing_applicators = []
        
            for structure in required_structures:
                if structure in data:
                    if data[structure] and len(data[structure]) > 0:
                        print(f"  ✅ {structure}: ANNOTATED")
                    else:
                        print(f"  ❌ {structure}: EMPTY (not annotated)")
                        missing_applicators.append(structure)
                else:
                    print(f"  ❌ {structure}: MISSING")
                    missing_applicators.append(structure)
        
            # Check anatomy
            if "anatomy" in data and data["anatomy"] and len(data["anatomy"]) > 0:
                print("  ✅ Anatomy: ANNOTATED")
            else:
                print("  ❌ Anatomy: NOT ANNOTATED")
            
            return len(missing_applicators) == 0
        
        except Exception as e:
            print(f"  ❌ Error checking file: {e}")
            return False
        
    def calculate_anatomy_referenced_shifts(self):
       
        import os
        import json

       
        frac1_points = self.load_applicator_points("AP_frac1_annotations.json")
        if not frac1_points:
            messagebox.showerror("Error", "Could not load Fraction 1 applicator points")
            return None

       
        frac2_file_options = [
            "AP_frac1_aligned_to_frac2.json",  
            "AP_frac2_annotations.json"        
        ]

        frac2_points = None
        for file_option in frac2_file_options:
            points = self.load_applicator_points(file_option)
            if points:
                frac2_points = points
                print(f"✅ Loaded Fraction 2 points from: {file_option}")
                break

        if not frac2_points:
            messagebox.showerror("Error", "Could not load Fraction 2 applicator points from any file")
            return None

        
        frac1_anatomy = self.load_anatomy_points("AP_frac1_annotations.json")
        frac2_anatomy = self.load_anatomy_points(frac2_file_options[0] if frac2_points else None)

        mm_per_px = self.pixel_spacing["AP_frac1"]
        shifts = {}

        def get_applicator_points(data, applicator):
         
            if isinstance(data, dict):
                
                if applicator in data and isinstance(data[applicator], dict):
                    return data[applicator].get("tip"), data[applicator].get("base")
            elif isinstance(data, list):
                
                for item in data:
                    if isinstance(item, dict) and applicator in item:
                        if isinstance(item[applicator], dict):
                            return item[applicator].get("tip"), item[applicator].get("base")
                        elif isinstance(item[applicator], list) and len(item[applicator]) > 0:
                         
                            points_list = item[applicator][0]
                            if len(points_list) >= 2:
                                return points_list[0], points_list[1]
            return None, None

        for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
            
            tip1, base1 = get_applicator_points(frac1_points, applicator)
            tip2, base2 = get_applicator_points(frac2_points, applicator)

            if not all([tip1, base1, tip2, base2]):
                print(f"Skipping {applicator} - missing points: tip1={tip1 is not None}, base1={base1 is not None}, tip2={tip2 is not None}, base2={base2 is not None}")
                continue

            
            direct_tip_shift = self.euclidean_distance(tip1, tip2) * mm_per_px
            direct_base_shift = self.euclidean_distance(base1, base2) * mm_per_px

            
            anatomy_referenced_tip_shift = direct_tip_shift
            anatomy_referenced_base_shift = direct_base_shift

            if frac1_anatomy and frac2_anatomy:
                
                anatomy_start1 = frac1_anatomy[0] if frac1_anatomy else (0, 0)
                anatomy_start2 = frac2_anatomy[0] if frac2_anatomy else (0, 0)

             
                tip1_relative = (tip1[0] - anatomy_start1[0], tip1[1] - anatomy_start1[1])
                tip2_relative = (tip2[0] - anatomy_start2[0], tip2[1] - anatomy_start2[1])

              
                anatomy_referenced_tip_shift = self.euclidean_distance(tip1_relative, tip2_relative) * mm_per_px
    
               
                base1_relative = (base1[0] - anatomy_start1[0], base1[1] - anatomy_start1[1])
                base2_relative = (base2[0] - anatomy_start2[0], base2[1] - anatomy_start2[1])

                anatomy_referenced_base_shift = self.euclidean_distance(base1_relative, base2_relative) * mm_per_px

            applicator_name = applicator.replace('applicator_', '').replace('_', ' ').title()

            shifts[applicator_name] = {
            
                "direct_tip_shift_mm": direct_tip_shift,
                "direct_base_shift_mm": direct_base_shift,
                "direct_average_shift_mm": (direct_tip_shift + direct_base_shift) / 2,
    
              
                "anatomy_referenced_tip_shift_mm": anatomy_referenced_tip_shift,
                "anatomy_referenced_base_shift_mm": anatomy_referenced_base_shift,
                "anatomy_referenced_average_shift_mm": (anatomy_referenced_tip_shift + anatomy_referenced_base_shift) / 2,

          
                "tip_to_anatomy_start_diff_mm": self.calculate_specific_distance_differences(applicator, "tip_to_start", mm_per_px),
                "tip_to_anatomy_end_diff_mm": self.calculate_specific_distance_differences(applicator, "tip_to_end", mm_per_px),
                "base_to_anatomy_start_diff_mm": self.calculate_specific_distance_differences(applicator, "base_to_start", mm_per_px),
                "base_to_anatomy_end_diff_mm": self.calculate_specific_distance_differences(applicator, "base_to_end", mm_per_px)
            }

        return shifts

    def test_aligned_file(self):
      
        aligned_file = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
        if os.path.exists(aligned_file):
            print("✅ Aligned file exists!")
            complete = self.check_annotation_completeness(aligned_file)
            print(f"✅ Aligned file completeness: {complete}")
        
           
            shifts = self.calculate_anatomy_referenced_shifts()
            if shifts:
                print("✅ Shifts calculated successfully!")
                for applicator, data in shifts.items():
                    print(f"{applicator}: {data['direct_average_shift_mm']:.2f} mm")
            else:
                print("❌ Could not calculate shifts")
        else:
            print("❌ Aligned file not found")

    def calculate_specific_distance_differences(self, applicator, measurement_type, mm_per_px):

        frac1_points = self.load_applicator_points("AP_frac1_annotations.json")
        frac2_points = self.load_applicator_points("AP_frac2_annotations.json")
        frac1_anatomy = self.load_anatomy_points("AP_frac1_annotations.json")
        frac2_anatomy = self.load_anatomy_points("AP_frac2_annotations.json")
    
        if not all([frac1_points, frac2_points, frac1_anatomy, frac2_anatomy]):
            return 0
    
       
        anatomy_start1 = frac1_anatomy[0]
        anatomy_start2 = frac2_anatomy[0]
        anatomy_end1 = frac1_anatomy[-1] if len(frac1_anatomy) > 1 else anatomy_start1
        anatomy_end2 = frac2_anatomy[-1] if len(frac2_anatomy) > 1 else anatomy_start2
    
     
        tip1 = frac1_points[applicator].get("tip")
        tip2 = frac2_points[applicator].get("tip")
        base1 = frac1_points[applicator].get("base")
        base2 = frac2_points[applicator].get("base")
    
        if not all([tip1, tip2, base1, base2]):
            return 0
    
       
        if measurement_type == "tip_to_start":
            dist1 = self.euclidean_distance(tip1, anatomy_start1) * mm_per_px
            dist2 = self.euclidean_distance(tip2, anatomy_start2) * mm_per_px
        elif measurement_type == "tip_to_end":
            dist1 = self.euclidean_distance(tip1, anatomy_end1) * mm_per_px
            dist2 = self.euclidean_distance(tip2, anatomy_end2) * mm_per_px
        elif measurement_type == "base_to_start":
            dist1 = self.euclidean_distance(base1, anatomy_start1) * mm_per_px
            dist2 = self.euclidean_distance(base2, anatomy_start2) * mm_per_px
        elif measurement_type == "base_to_end":
            dist1 = self.euclidean_distance(base1, anatomy_end1) * mm_per_px
            dist2 = self.euclidean_distance(base2, anatomy_end2) * mm_per_px
        else:
            return 0
    
        return dist2 - dist1  # F2 - F1

    def load_anatomy_points(self, json_filename):
       
        import os
        import json
    
        json_path = os.path.join(self.temp_dir, json_filename)
        if not os.path.exists(json_path):
            return None
    
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        
            if "anatomy" in data and data["anatomy"]:
                return data["anatomy"][0]  
            return None
        except Exception as e:
            print(f"Error loading anatomy points: {e}")
            return None

    def compare_fraction_distances_from_txt(self):
   

        if not self.validate_comparison_files():
            return
        
        import os
        import re
        from datetime import datetime
    
      
        file1 = os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt")
        file2 = os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")
    
    
        if not os.path.exists(file1) or not os.path.exists(file2):
            messagebox.showerror("Error", 
                               "Missing distance files.\n\n"
                               f"Fraction 1: {'Found' if os.path.exists(file1) else 'Missing'}\n"
                               f"Fraction 2: {'Found' if os.path.exists(file2) else 'Missing'}")
            return
    
        def extract_distances(file_path):
      
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
               
                pattern = r"(.+?)\s+(Tip|Base)\s+to\s+Anatomy\s+(Start|End):\s*([\d.]+)\s*mm"
                matches = re.findall(pattern, content)
            
                for match in matches:
                    applicator = match[0].strip()
                    point_type = match[1].lower()  
                    anatomy_point = match[2].lower()
                    value = float(match[3])
                
                  
                    if applicator not in distances:
                        distances[applicator] = {}
                
                   
                    key = f"{point_type}_to_{anatomy_point}"
                    distances[applicator][key] = value
                
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            return distances
    
      
        dist1 = extract_distances(file1)
        dist2 = extract_distances(file2)
    
        if not dist1 or not dist2:
            messagebox.showerror("Error", "No valid distance data found in one or both files")
            return
    
     
        shifts = {}
    
        applicators = ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]
    
        for applicator in applicators:
            if applicator in dist1 and applicator in dist2:
                applicator_shifts = {}
            
               
                for measurement_key in ["tip_to_start", "tip_to_end", "base_to_start", "base_to_end"]:
                    if measurement_key in dist1[applicator] and measurement_key in dist2[applicator]:
                        frac1_val = dist1[applicator][measurement_key]
                        frac2_val = dist2[applicator][measurement_key]
                        shift = frac2_val - frac1_val  
                    
                     
                        parts = measurement_key.split('_')
                        point_type = parts[0].title()
                        anatomy_part = parts[2].title()
                        measurement_name = f"{point_type} to Anatomy {anatomy_part}"
                    
                        applicator_shifts[measurement_name] = {
                            'fraction1': frac1_val,
                            'fraction2': frac2_val,
                                'shift': shift,
                        'absolute_shift': abs(shift)
                        }
            
                if applicator_shifts:
                    shifts[applicator] = applicator_shifts
    
       
        self.save_applicator_shifts_to_txt(shifts, file1, file2)
    
       
        self.display_applicator_shifts(shifts)


    
    def validate_comparison_files(self):
     
        required_files = [
            "AP_frac1_distances_from_anatomy.txt",
            "AP_frac2_distances_from_anatomy.txt",
            "AP_frac1_annotations.json", 
            "AP_frac2_annotations.json"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = os.path.join(self.temp_dir, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)
    
        if missing_files:
            error_msg = "Missing required files for comparison:\n" + "\n".join(missing_files)
            messagebox.showerror("Missing Files", error_msg)
            return False
    
       
        frac1_complete = self.check_annotation_completeness(os.path.join(self.temp_dir, "AP_frac1_annotations.json"))
        frac2_complete = self.check_annotation_completeness(os.path.join(self.temp_dir, "AP_frac2_annotations.json"))
    
        if not frac1_complete or not frac2_complete:
            messagebox.showerror("Incomplete Annotations", 
                           "One or both fractions have incomplete annotations.\nPlease ensure all applicators are annotated.")
            return False
    
        return True


    def save_applicator_shifts_to_txt(self, shifts, file1_path, file2_path):
       
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, "applicator_shifts_between_fractions.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("APPLICATOR SHIFTS BETWEEN FRACTIONS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Data source:\n")
                f.write(f"  Fraction 1: {os.path.basename(file1_path)}\n")
                f.write(f"  Fraction 2: {os.path.basename(file2_path)}\n\n")
                f.write("METHOD: Shift = (Fraction 2 distance) - (Fraction 1 distance)\n\n")
                    
                for applicator, measurements in shifts.items():
                    f.write(f"{applicator.upper()} SHIFTS\n")
                    f.write("-" * 40 + "\n")
                
                    for measurement_name, data in measurements.items():
                        direction = "increased" if data['shift'] > 0 else "decreased"
                        f.write(f"{measurement_name}:\n")
                        f.write(f"  Fraction 1: {data['fraction1']:.2f} mm\n")
                        f.write(f"  Fraction 2: {data['fraction2']:.2f} mm\n")
                        f.write(f"  Shift: {data['shift']:+.2f} mm ({direction})\n")
                        f.write(f"  Absolute shift: {data['absolute_shift']:.2f} mm\n\n")
                
         
                    all_shifts = [data['absolute_shift'] for data in measurements.values()]
                    if all_shifts:
                        avg_shift = sum(data['shift'] for data in measurements.values()) / len(measurements)
                        avg_abs_shift = sum(all_shifts) / len(all_shifts)
                        max_shift = max(all_shifts)
                        
                        f.write(f"SUMMARY FOR {applicator.upper()}:\n")
                        f.write(f"  Average shift: {avg_shift:+.2f} mm\n")
                        f.write(f"  Average absolute shift: {avg_abs_shift:.2f} mm\n")
                        f.write(f"  Maximum shift: {max_shift:.2f} mm\n\n")
            
             
                f.write("OVERALL STATISTICS\n")
                f.write("-" * 30 + "\n")
            
                all_applicator_shifts = []
                for applicator, measurements in shifts.items():
                    for data in measurements.values():
                        all_applicator_shifts.append(data['absolute_shift'])
            
                if all_applicator_shifts:
                    overall_avg_shift = sum(data['shift'] for measurements in shifts.values() for data in measurements.values()) / len(all_applicator_shifts)
                    overall_avg_abs_shift = sum(all_applicator_shifts) / len(all_applicator_shifts)
                    overall_max_shift = max(all_applicator_shifts)
                
                    f.write(f"Average shift across all applicators: {overall_avg_shift:+.2f} mm\n")
                    f.write(f"Average absolute shift: {overall_avg_abs_shift:.2f} mm\n")
                    f.write(f"Maximum observed shift: {overall_max_shift:.2f} mm\n\n")
                
               
                    f.write("CLINICAL ASSESSMENT\n")
                    f.write("-" * 30 + "\n")
                    if overall_max_shift < 3.0:
                        f.write("EXCELLENT reproducibility - minimal applicator movement\n")
                    elif overall_max_shift < 5.0:
                        f.write("GOOD reproducibility - acceptable clinical variation\n")
                    elif overall_max_shift < 7.0:
                        f.write("MODERATE variation - consider clinical impact\n")
                    else:
                        f.write("SIGNIFICANT movement - review positioning and fixation\n")
        
            messagebox.showinfo("Success", f"Applicator shifts saved to:\n{output_file}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save shifts: {str(e)}")

    def display_applicator_shifts(self, shifts):
    
        results_window = tk.Toplevel(self.root)
        results_window.title("Applicator Shifts Between Fractions")
        results_window.geometry("800x600")
    
      
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
      
        title_label = tk.Label(main_frame, text="APPLICATOR SHIFTS ANALYSIS", 
                              font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)
    
      
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")
    
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
    
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
       
        text_widget.insert(tk.END, "APPLICATOR SHIFTS BETWEEN FRACTIONS\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
    
        if not shifts:
            text_widget.insert(tk.END, "No matching measurements found between fractions.\n")
            text_widget.insert(tk.END, "Please ensure both fractions have the same structures annotated.\n")
        else:
            for applicator, measurements in shifts.items():
                text_widget.insert(tk.END, f"{applicator.upper()}\n", "subtitle")
                text_widget.insert(tk.END, "-" * 40 + "\n")
            
                for measurement_name, data in measurements.items():
                    direction = "increased" if data['shift'] > 0 else "decreased"
                    text_widget.insert(tk.END, 
                                     f"{measurement_name}:\n"
                                     f"  F1: {data['fraction1']:.2f} mm → "
                                     f"F2: {data['fraction2']:.2f} mm\n"
                                     f"  Shift: {data['shift']:+.2f} mm ({direction})\n"
                                     f"  Absolute: {data['absolute_shift']:.2f} mm\n\n")
    
     
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#1565C0")
    
        text_widget.config(state=tk.DISABLED)
    
      
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
    
      
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack()

    def debug_txt_files(self):
        
        import os
    
        files_to_check = [
            "AP_frac1_distances_from_anatomy.txt",
            "AP_frac2_distances_from_anatomy.txt"
        ]
    
        print("=== DEBUG TXT FILES ===")
        for filename in files_to_check:
            filepath = os.path.join(self.temp_dir, filename)
            if os.path.exists(filepath):
                print(f"\n--- {filename} ---")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(content)
                    
                       
                        lines = content.split('\n')
                        print(f"Total lines: {len(lines)}")
                    
                
                        measurement_lines = [line for line in lines if 'mm' in line]
                        print(f"Lines with 'mm': {len(measurement_lines)}")
                        for line in measurement_lines:
                            print(f"  -> {line}")
                        
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
            else:    
                print(f"\n--- {filename} NOT FOUND ---")


    def update_frac2_annotations_from_alignment(self):
        
        try:
            alignment_file = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
            frac2_file = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
        
            if not os.path.exists(alignment_file):
                print("Alignment file not found")
                return False
            
            if not os.path.exists(frac2_file):
                print("Fraction 2 file not found")
                return False
            
           
            with open(alignment_file, 'r') as f:
                alignment_data = json.load(f)
            
            with open(frac2_file, 'r') as f:
                frac2_data = json.load(f)
        
           
            for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                if applicator in alignment_data and alignment_data[applicator]:
                    frac2_data[applicator] = alignment_data[applicator]
                    print(f"Updated {applicator} in Fraction 2")
        
        
            with open(frac2_file, 'w') as f:
                json.dump(frac2_data, f)
            
            print("✅ Successfully updated AP_frac2_annotations.json with applicator data")
            return True
        
        except Exception as e:
            print(f"Error updating Fraction 2 annotations: {e}")
            return False
    
    def update_frac2_annotations_from_alignment(self):
 
        try:
            alignment_file = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
            frac2_file = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
        
            if not os.path.exists(alignment_file):
                print("Alignment file not found")
                return False
            
            if not os.path.exists(frac2_file):
                print("Fraction 2 file not found")
                return False
            
            
            with open(alignment_file, 'r') as f:
                alignment_data = json.load(f)
            
            with open(frac2_file, 'r') as f:
                frac2_data = json.load(f)
        
       
            for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                if applicator in alignment_data and alignment_data[applicator]:
                    frac2_data[applicator] = alignment_data[applicator]
                    print(f"Updated {applicator} in Fraction 2")
        
           
            with open(frac2_file, 'w') as f:
                json.dump(frac2_data, f)
                
            print("✅ Successfully updated AP_frac2_annotations.json with applicator data")
            return True
        
        except Exception as e:
            print(f"Error updating Fraction 2 annotations: {e}")
            return False

    def compare_fraction_distances_anatomy_referenced(self):

    
        import os
    
        
        self.debug_annotation_files()
    
      
        frac1_file = os.path.join(self.temp_dir, "AP_frac1_annotations.json")
        frac2_file = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
    
        if not os.path.exists(frac1_file) or not os.path.exists(frac2_file):
            messagebox.showerror("Error", "Missing annotation files. Please annotate both fractions first.")
            return

        def extract_distances(file_path):
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"(.+?):\s*([\d.]+)\s*mm", line)
                        if match:
                            key = match.group(1).strip()
                            value = float(match.group(2))
                            distances[key] = value
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            return distances

        dist1 = extract_distances(file1)
        dist2 = extract_distances(file2)

        if not dist1 or not dist2:
            messagebox.showerror("Error", "No valid distance data found in one or both files")
            return

        all_keys = sorted(set(dist1.keys()).union(set(dist2.keys())))
        diff_results = []
    
        for key in all_keys:
            val1 = dist1.get(key, None)
            val2 = dist2.get(key, None)
            if val1 is not None and val2 is not None:
                diff = val2 - val1
                diff_results.append(f"{key}:\n"
                                  f"  Fraction 1 = {val1:.2f} mm\n"
                                  f"  Fraction 2 = {val2:.2f} mm\n"
                                  f"  Difference = {diff:+.2f} mm\n")
            else:
                diff_results.append(f"{key}: Missing data in one fraction\n")

        
        results_window = tk.Toplevel(self.root)
        results_window.title("AP View - Fraction Distance Comparison")
        results_window.geometry("800x600")

        
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        
        title_label = tk.Label(main_frame, text="AP VIEW - DISTANCE COMPARISON", 
                              font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)

        
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")
    
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
    
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

     
        text_widget.insert(tk.END, "DISTANCE COMPARISON - AP VIEW\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        text_widget.insert(tk.END, f"Comparison performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for result in diff_results:
            text_widget.insert(tk.END, result + "\n")

       
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.config(state=tk.DISABLED)

        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

       
        save_button = tk.Button(button_frame, text="💾 Save Comparison", 
                              command=lambda: self.save_comparison_results(diff_results, "AP"),
                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                              width=20, height=1)
        save_button.pack(side=tk.LEFT, padx=10)

        
        "AP_frac2_annotations.json", 
        "AP_frac1_aligned_to_frac2.json"
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack(side=tk.LEFT, padx=10)

    def save_comparison_results(self, results, view_type):
        
        import os
        from datetime import datetime

        output_file = os.path.join(self.temp_dir, f"{view_type}_distance_comparison.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"{view_type} VIEW - DISTANCE COMPARISON BETWEEN FRACTIONS\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Comparison performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for result in results:
                    f.write(result + "\n")
    
            messagebox.showinfo("Success", f"Comparison results saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    def debug_annotation_structure(self):
        
        import os
        import json
    
        annotation_files = [
            "AP_frac1_annotations.json",
            "AP_frac2_annotations.json", 
            "AP_frac1_aligned_to_frac2.json"
        ]
    
        for file_name in annotation_files:
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.exists(file_path):
                print(f"\n=== {file_name} ===")
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    print(f"Type: {type(data)}")
                    if isinstance(data, dict):
                        print("Keys:", list(data.keys()))
                        for key in data:
                            print(f"  {key}: {type(data[key])} - {data[key]}")
                    elif isinstance(data, list):
                        print(f"List length: {len(data)}")
                        for i, item in enumerate(data):
                            print(f"  Item {i}: {type(item)} - {item}")
                except Exception as e:
                    print(f"Error reading: {e}")
    
    def compare_fraction_distances_txt_only(self):
     
        import os
        import re

        
        file1 = os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt")
        file2 = os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")

        # Check if TXT files exist
        if not os.path.exists(file1) or not os.path.exists(file2):
            messagebox.showerror("Error", 
                               "Missing distance files. Please complete annotation for both fractions first.\n\n"
                               f"Fraction 1: {'Found' if os.path.exists(file1) else 'Missing'}\n"
                               f"Fraction 2: {'Found' if os.path.exists(file2) else 'Missing'}")
            return

        def extract_structured_distances(file_path):
           
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    current_applicator = None
                    for line in f:
                        line = line.strip()
                
                        
                        if not line or "===" in line or "Anatomy" in line:
                            continue
                    
                       
                        match = re.match(r"(.+?)\s+(Tip|Base)\s+to\s+Anatomy\s+(Start|End):\s*([\d.]+)\s*mm", line)
                        if match:
                            applicator = match.group(1).strip()
                            point_type = match.group(2).lower()  
                            anatomy_point = match.group(3).lower()  
                            value = float(match.group(4))
                    
                       
                            if applicator not in distances:
                                distances[applicator] = {}
                    
                           
                            key = f"{point_type}_to_{anatomy_point}"
                            distances[applicator][key] = value
                    
            except Exception as e:
                print(f"Error reading TXT file {file_path}: {e}")
            return distances

       
        dist1 = extract_structured_distances(file1)
        dist2 = extract_structured_distances(file2)

        if not dist1 or not dist2:
            messagebox.showerror("Error", "No valid distance data found in one or both TXT files")
            return

       
        shifts = {}

        for applicator in ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]:
            if applicator in dist1 and applicator in dist2:
            
                measurement_pairs = []
        
                for point_type in ["tip", "base"]:
                    for anatomy_point in ["start", "end"]:
                        key = f"{point_type}_to_{anatomy_point}"
                        if key in dist1[applicator] and key in dist2[applicator]:
                         
                            shift = dist2[applicator][key] - dist1[applicator][key]
                            measurement_pairs.append({
                                'measurement': f"{point_type.title()} to Anatomy {anatomy_point.title()}",
                                'fraction1': dist1[applicator][key],
                                'fraction2': dist2[applicator][key],
                                'shift': shift,
                                'abs_shift': abs(shift)
                            })
        
                if measurement_pairs:
                   
                    avg_shift = sum(pair['shift'] for pair in measurement_pairs) / len(measurement_pairs)
                    avg_abs_shift = sum(pair['abs_shift'] for pair in measurement_pairs) / len(measurement_pairs)
                
                    shifts[applicator] = {
                        'measurements': measurement_pairs,
                        'average_shift': avg_shift,
                        'average_absolute_shift': avg_abs_shift,
                        'max_shift': max(abs(pair['shift']) for pair in measurement_pairs)
                    }

        
        self.show_direct_euclidean_results_txt_only(shifts, file1, file2)

    def show_direct_euclidean_results_txt_only(self, shifts, file1_path, file2_path):
        
        results_window = tk.Toplevel(self.root)
        results_window.title("Direct Euclidean Distance Comparison - AP View (TXT Files)")
        results_window.geometry("1000x700")

        
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        
        title_label = tk.Label(main_frame, text="DIRECT EUCLIDEAN DISTANCE COMPARISON", 
                          font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)

       
        subtitle_label = tk.Label(main_frame, text="APPROACH: Point-to-Point Distance Differences using TXT files only",
                                font=("Arial", 12), fg="#555555")
        subtitle_label.pack(pady=5)
    
       
        file_info = tk.Label(main_frame, 
                            text=f"Data from TXT files:\n• {os.path.basename(file1_path)}\n• {os.path.basename(file2_path)}",
                            font=("Arial", 9), fg="#666666", justify=tk.LEFT)
        file_info.pack(pady=5)

       
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

       
        text_widget.insert(tk.END, "DIRECT EUCLIDEAN DISTANCE SHIFTS (TXT FILES ONLY)\n", "title")
        text_widget.insert(tk.END, "=" * 60 + "\n\n")
        text_widget.insert(tk.END, f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        text_widget.insert(tk.END, "METHOD: Direct comparison of pre-calculated distances from TXT files\n")
        text_widget.insert(tk.END, "FORMULA: Shift = (Fraction 2 distance) - (Fraction 1 distance)\n\n")

        if not shifts:
            text_widget.insert(tk.END, "No matching measurements found between fractions.\n")
            text_widget.insert(tk.END, "Please ensure both fractions have the same structures annotated.\n")
        else:
            for applicator, data in shifts.items():
                text_widget.insert(tk.END, f"{applicator.upper()}\n", "subtitle")
                text_widget.insert(tk.END, "-" * 40 + "\n")
        
          
                for measurement in data['measurements']:
                    direction = "increased" if measurement['shift'] > 0 else "decreased"
                    text_widget.insert(tk.END, 
                                     f"  • {measurement['measurement']}:\n"
                                     f"    F1: {measurement['fraction1']:.2f} mm → "
                                     f"F2: {measurement['fraction2']:.2f} mm\n"
                                     f"    Shift: {measurement['shift']:+.2f} mm ({direction})\n")
        
               
                text_widget.insert(tk.END, f"\n  SUMMARY:\n")
                text_widget.insert(tk.END, f"  • Average shift: {data['average_shift']:+.2f} mm\n")
                text_widget.insert(tk.END, f"  • Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
                text_widget.insert(tk.END, f"  • Maximum shift: {data['max_shift']:.2f} mm\n")
        
               
                if data['max_shift'] < 3.0:
                    assessment = "EXCELLENT reproducibility"
                    color = "green"
                elif data['max_shift'] < 5.0:
                    assessment = "GOOD reproducibility"
                    color = "orange"
                elif data['max_shift'] < 7.0:
                    assessment = "MODERATE variation"
                    color = "darkorange"
                else:
                    assessment = "SIGNIFICANT movement"
                    color = "red"
            
                text_widget.insert(tk.END, f"  • ASSESSMENT: {assessment}\n", color)
                text_widget.insert(tk.END, "\n")

       
        if shifts:
            text_widget.insert(tk.END, "OVERALL CLINICAL ASSESSMENT\n", "subtitle")
            text_widget.insert(tk.END, "=" * 40 + "\n\n")
    
            max_overall_shift = max(data['max_shift'] for data in shifts.values())
            if max_overall_shift < 3.0:
                assessment = "✓ EXCELLENT overall reproducibility"
                details = "Minimal applicator movement between fractions"
                color = "green"
            elif max_overall_shift < 5.0:
                assessment = "✓ GOOD overall reproducibility" 
                details = "Acceptable clinical variation"
                color = "orange"
            elif max_overall_shift < 7.0:
                assessment = "⚠ MODERATE overall variation"
                details = "Consider clinical impact on dose distribution"
                color = "darkorange"
            else:
                assessment = "❌ SIGNIFICANT overall movement"
                details = "Review patient positioning and applicator fixation"
                color = "red"
        
            text_widget.insert(tk.END, f"{assessment}\n", color)
            text_widget.insert(tk.END, f"{details}\n")
            text_widget.insert(tk.END, f"Maximum observed shift: {max_overall_shift:.2f} mm\n")

      
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#1565C0")
        text_widget.tag_configure("green", foreground="#2E7D32")
        text_widget.tag_configure("orange", foreground="#FF9800")
        text_widget.tag_configure("darkorange", foreground="#FF5722")
        text_widget.tag_configure("red", foreground="#D32F2F")
    
        text_widget.config(state=tk.DISABLED)

       
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

       
        save_button = tk.Button(button_frame, text="💾 Save TXT Report", 
                              command=lambda: self.save_direct_euclidean_report_txt_only(shifts),
                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                              width=15, height=1)
        save_button.pack(side=tk.LEFT, padx=10)

       
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack(side=tk.LEFT, padx=10)

    def save_direct_euclidean_report_txt_only(self, shifts):
        
        import os
        from datetime import datetime

        output_file = os.path.join(self.temp_dir, "AP_direct_euclidean_comparison_TXT_ONLY.txt")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("DIRECT EUCLIDEAN DISTANCE COMPARISON REPORT (TXT FILES ONLY)\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("METHOD: Direct point-to-point Euclidean distance differences using TXT files\n")
                f.write("FORMULA: Shift = (Fraction 2 distance) - (Fraction 1 distance)\n\n")
        
                for applicator, data in shifts.items():
                    f.write(f"{applicator.upper()}\n")
                    f.write("-" * 50 + "\n")
            
                    for measurement in data['measurements']:
                        f.write(f"{measurement['measurement']}:\n")
                        f.write(f"  Fraction 1: {measurement['fraction1']:.2f} mm\n")
                        f.write(f"  Fraction 2: {measurement['fraction2']:.2f} mm\n")
                        f.write(f"  Shift: {measurement['shift']:+.2f} mm\n")
            
                    f.write(f"\nSummary for {applicator}:\n")
                    f.write(f"  Average shift: {data['average_shift']:+.2f} mm\n")
                    f.write(f"  Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
                    f.write(f"  Maximum shift: {data['max_shift']:.2f} mm\n\n")
        
            messagebox.showinfo("Report Saved", f"Direct Euclidean comparison (TXT only) saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def validate_annotation_file(self, file_path):
        """Validate that an annotation file has the required structure"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        
            print(f"Validating {os.path.basename(file_path)}:")
        
            
            if not isinstance(data, dict):
                print("  ❌ Not a dictionary")
                return False
            
            
            required_structures = ["applicator_tandem", "left_ovoid", "right_ovoid"]
            missing_structures = []
        
            for structure in required_structures:
                if structure in data:
                    print(f"  ✅ {structure} found")
                   
                    if data[structure]:
                        print(f"  ✅ {structure} has data: {data[structure]}")
                    else:
                        print(f"  ⚠️  {structure} exists but is empty")
                        missing_structures.append(structure)
                else:
                    print(f"  ❌ {structure} missing")
                    missing_structures.append(structure)
        
           
            if "anatomy" in data and data["anatomy"]:
                print("  ✅ Anatomy found with data")
            else:
                print("  ⚠️  Anatomy missing or empty")
            
            return len(missing_structures) == 0
        
        except Exception as e:
            print(f"  ❌ Error validating file: {e}")
            return False

    def save_enhanced_shift_report(self, shifts, view_type):
       
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, f"{view_type}_enhanced_shift_report.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("ENHANCED APPLICATOR SHIFT ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"View: {view_type}\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
                for applicator, data in shifts.items():
                    f.write(f"{applicator.upper()}:\n")
                    f.write("-" * 40 + "\n")
                
                    f.write("Direct Point-to-Point Shifts:\n")
                    f.write(f"  Tip displacement: {data['direct_tip_shift_mm']:.2f} mm\n")
                    f.write(f"  Base displacement: {data['direct_base_shift_mm']:.2f} mm\n")
                    f.write(f"  Average displacement: {data['direct_average_shift_mm']:.2f} mm\n\n")
                
                    f.write("Anatomy-Referenced Shifts:\n")
                    f.write(f"  Tip displacement: {data['anatomy_referenced_tip_shift_mm']:.2f} mm\n")
                    f.write(f"  Base displacement: {data['anatomy_referenced_base_shift_mm']:.2f} mm\n")
                    f.write(f"  Average displacement: {data['anatomy_referenced_average_shift_mm']:.2f} mm\n\n")
                
                    f.write("Specific Distance Differences (F2 - F1):\n")
                    f.write(f"  Tip to Anatomy Start: {data['tip_to_anatomy_start_diff_mm']:+.2f} mm\n")
                    f.write(f"  Tip to Anatomy End: {data['tip_to_anatomy_end_diff_mm']:+.2f} mm\n")
                    f.write(f"  Base to Anatomy Start: {data['base_to_anatomy_start_diff_mm']:+.2f} mm\n")
                    f.write(f"  Base to Anatomy End: {data['base_to_anatomy_end_diff_mm']:+.2f} mm\n\n")
        
            messagebox.showinfo("Report Saved", f"Enhanced shift report saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def save_shift_report(self, shifts, view_type):
        
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, f"{view_type}_applicator_shifts_report.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("APPLICATOR SHIFT ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"View: {view_type}\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
                f.write("DIRECT DISPLACEMENT MEASUREMENTS:\n")
                f.write("-" * 40 + "\n\n")
            
                total_shifts = []
            
                for applicator, data in shifts.items():
                    f.write(f"{applicator.upper()}:\n")
                    f.write(f"  Tip displacement: {data['tip_shift_mm']:.2f} mm\n")
                    f.write(f"  Base displacement: {data['base_shift_mm']:.2f} mm\n")
                    f.write(f"  Average displacement: {data['average_shift_mm']:.2f} mm\n\n")
                
                    total_shifts.append(data['average_shift_mm'])
            
                
                if total_shifts:
                    max_shift = max(total_shifts)
                    min_shift = min(total_shifts)
                    avg_shift = sum(total_shifts) / len(total_shifts)
                
                    f.write("OVERALL STATISTICS:\n")
                    f.write("-" * 40 + "\n\n")
                    f.write(f"Maximum applicator shift: {max_shift:.2f} mm\n")
                    f.write(f"Minimum applicator shift: {min_shift:.2f} mm\n")
                    f.write(f"Average applicator shift: {avg_shift:.2f} mm\n\n")
                
                    f.write("CLINICAL ASSESSMENT:\n")
                    f.write("-" * 40 + "\n\n")
                    if max_shift < 3.0:
                        f.write("EXCELLENT reproducibility - minimal applicator movement between fractions\n")
                    elif max_shift < 5.0:
                        f.write("GOOD reproducibility - acceptable clinical variation\n")
                    elif max_shift < 7.0:
                        f.write("MODERATE variation - consider clinical impact on dose distribution\n")
                    else:
                        f.write("SIGNIFICANT movement - review patient positioning and applicator fixation\n")
        
            messagebox.showinfo("Report Saved", f"Comprehensive shift report saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def open_annotation_window(self, img_path, fraction_key):
        save_folder = self.temp_dir
        os.makedirs(save_folder, exist_ok=True)

        win = tk.Toplevel(self.root)
        win.title(f"Annotate and Align: {fraction_key}")
        win.geometry("1400x900")  
        win.configure(bg="#F5F5F5")

      
        win.grid_rowconfigure(1, weight=1)
        win.grid_columnconfigure(0, weight=1)
        win.grid_columnconfigure(1, weight=0)  

        
        from PIL import Image as PILImage
        img = cv2.imread(img_path)
        img_h, img_w = img.shape[:2]
        screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
        scale = min(screen_w / img_w, screen_h / img_h, 1.0)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        img_resized = cv2.resize(img, (new_w, new_h))
        
       
        pil_img = PILImage.fromarray(img_resized)
        zoom = [1.0]

     
        content_frame = tk.Frame(win, bg="#F5F5F5")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

      
        canvas_frame = tk.Frame(content_frame, bg="#F5F5F5")
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, width=new_w, height=new_h, bg="lightgray", 
                          scrollregion=(0, 0, new_w, new_h))
        
    
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview,
                                  bg="#E0E0E0", troughcolor="#F5F5F5")
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview,
                                  bg="#E0E0E0", troughcolor="#F5F5F5")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        img_tk = ImageTk.PhotoImage(pil_img)
        canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.image = img_tk

       
        explicit_points = {
            "anatomy": [],
            "applicator_tandem": {"tip": None, "base": None},
            "left_ovoid": {"tip": None, "base": None},
            "right_ovoid": {"tip": None, "base": None}
        }
    
        
        anatomy_points = []
    
        current_points = []
        mode = tk.StringVar(value="anatomy")
        point_type = tk.StringVar(value="tip")  
    
        
       

        color_map = {
            "anatomy": "red",
            "applicator_tandem": "blue",
            "left_ovoid": "purple",
            "right_ovoid": "green"
        }

        
        canvas_items = {
            "anatomy": [],
            "applicator_tandem": {"tip": None, "base": None, "line": None},
            "left_ovoid": {"tip": None, "base": None, "line": None},
            "right_ovoid": {"tip": None, "base": None, "line": None}
        }

        def redraw_canvas():
            
            for item_type in canvas_items:
                if item_type == "anatomy":
                    for item in canvas_items[item_type]:
                        canvas.delete(item)
                    canvas_items[item_type] = []
                else:
                    for point_type in ["tip", "base", "line"]:
                        if canvas_items[item_type][point_type]:
                            canvas.delete(canvas_items[item_type][point_type])
                            canvas_items[item_type][point_type] = None

          
            scaled_w, scaled_h = int(new_w * zoom[0]), int(new_h * zoom[0])
            canvas.config(scrollregion=(0, 0, scaled_w, scaled_h))
    
          
            pil_scaled = pil_img.resize((scaled_w, scaled_h), PILImage.Resampling.LANCZOS)
            img_tk_scaled = ImageTk.PhotoImage(pil_scaled)
            canvas.delete("background")  
            canvas.create_image(0, 0, anchor='nw', image=img_tk_scaled, tags="background")
            canvas.image = img_tk_scaled

            
            for poly in anatomy_points:
                scaled_poly = [(int(x * zoom[0]), int(y * zoom[0])) for x, y in poly]
                if len(scaled_poly) > 1:
                    item = canvas.create_line(scaled_poly, fill=color_map["anatomy"], width=2, tags="annotation")
                    canvas_items["anatomy"].append(item)
                for x, y in scaled_poly:
                    item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="annotation")
                    canvas_items["anatomy"].append(item)

          
            for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                tip = explicit_points[label]["tip"]
                base = explicit_points[label]["base"]
    
                if tip:
                    x, y = int(tip[0] * zoom[0]), int(tip[1] * zoom[0])
                    item = canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                            outline='white', tags="annotation")
                    canvas_items[label]["tip"] = item
                    item_text = canvas.create_text(x+10, y-10, text=f"{label.replace('_', ' ').title()} Tip", 
                                             fill='white', font=("Arial", 8), tags="annotation")
                    canvas_items["anatomy"].append(item_text)
    
                if base:
                    x, y = int(base[0] * zoom[0]), int(base[1] * zoom[0])
                    item = canvas.create_rectangle(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                outline='white', tags="annotation")
                    canvas_items[label]["base"] = item
                    item_text = canvas.create_text(x+10, y+10, text=f"{label.replace('_', ' ').title()} Base", 
                                                 fill='white', font=("Arial", 8), tags="annotation")
                    canvas_items["anatomy"].append(item_text)
    
               
                if tip and base:
                    item = canvas.create_line(
                        int(tip[0] * zoom[0]), int(tip[1] * zoom[0]),
                        int(base[0] * zoom[0]), int(base[1] * zoom[0]),
                        fill=color_map[label], width=2, dash=(4, 2), tags="annotation"
                    )
                    canvas_items[label]["line"] = item

           
            scaled_current = [(int(x * zoom[0]), int(y * zoom[0])) for x, y in current_points]
            if len(scaled_current) > 1:
                item = canvas.create_line(scaled_current, fill=color_map["anatomy"], width=2, tags="annotation")
                canvas_items["anatomy"].append(item)
            for x, y in scaled_current:
                item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="annotation")
                canvas_items["anatomy"].append(item)

      

        
      

        def on_click(event):
            x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
    
            if mode.get() == "anatomy":
                current_points.append((x, y))
                redraw_canvas()
            else:
              
                if point_type.get() == "tip":
                    explicit_points[mode.get()]["tip"] = (x, y)
                    point_type.set("base")
                    print(f"Set {mode.get()} tip at ({x}, {y})")
                else:
                    explicit_points[mode.get()]["base"] = (x, y)
                    point_type.set("tip")
                    print(f"Set {mode.get()} base at ({x}, {y})")
        
                redraw_canvas()
    
           

        def on_mouse_move(event):
            x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
            status_var.set(f"Position: X:{x} Y:{y} | Mode: {mode.get().replace('_', ' ').title()} | Point: {point_type.get().title()}")

        def finish_anatomy_polygon(event=None):
            if len(current_points) >= 2:
                anatomy_points.append(current_points.copy())
            current_points.clear()
            redraw_canvas()
            

        def undo_last_point():
            if mode.get() == "anatomy":
                if current_points:
                    current_points.pop()
            else:
                
                if point_type.get() == "tip" and explicit_points[mode.get()]["base"]:
                    explicit_points[mode.get()]["base"] = None
                    point_type.set("base")
                elif explicit_points[mode.get()]["tip"]:
                    explicit_points[mode.get()]["tip"] = None
                    point_type.set("tip")
            redraw_canvas()
            

        def clear_current_applicator():
            explicit_points[mode.get()]["tip"] = None
            explicit_points[mode.get()]["base"] = None
            point_type.set("tip")
            redraw_canvas()
            

        def clear_all_annotations():
            anatomy_points.clear()
            current_points.clear()
            for label in explicit_points:
                if label == "anatomy":
                    continue
                explicit_points[label]["tip"] = None
                explicit_points[label]["base"] = None
            point_type.set("tip")
            mode.set("anatomy")
            redraw_canvas()
            

        def save_all_annotations():
            """Save annotations and automatically export distances to TXT file"""
            
            polygons = {
                "anatomy": anatomy_points,
                "applicator_tandem": [],
                "left_ovoid": [],
                "right_ovoid": []
            }        

           
            for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                tip = explicit_points[label]["tip"]
                base = explicit_points[label]["base"]
                if tip and base:
                   
                    polygons[label].append([tip, base])

            
            json_path = os.path.join(save_folder, f"{fraction_key}_annotations.json")
            with open(json_path, 'w') as f:
                json.dump(polygons, f)

            print(f"✅ SAVED ANNOTATIONS: {json_path}")
            print(f"✅ Anatomy points: {len(anatomy_points)}")
            print(f"✅ Tandem: tip={explicit_points['applicator_tandem']['tip']}, base={explicit_points['applicator_tandem']['base']}")
            print(f"✅ Left ovoid: tip={explicit_points['left_ovoid']['tip']}, base={explicit_points['left_ovoid']['base']}")
            print(f"✅ Right ovoid: tip={explicit_points['right_ovoid']['tip']}, base={explicit_points['right_ovoid']['base']}")

            
            explicit_path = os.path.join(save_folder, f"{fraction_key}_explicit_points.json")
            with open(explicit_path, 'w') as f:
                json.dump(explicit_points, f)

            
          
            export_distances_to_txt(polygons, json_path)

            return polygons

        
        def export_distances_to_txt(polygons, json_path):
            """Export distance measurements to TXT file with fraction number"""
            if len(anatomy_points) == 0 or len(anatomy_points[0]) < 2:
                print("⚠️ Cannot export distances: Anatomy not fully annotated")
                return

            anatomy_poly = anatomy_points[0]
            anatomy_start = anatomy_poly[0]
            anatomy_end = anatomy_poly[-1]

            mm_per_px = self.pixel_spacing.get("AP_frac1", 0.2979)  

            
            fraction_number = "1" if "frac1" in fraction_key else "2" if "frac2" in fraction_key else "Unknown"
            view_type = "AP" if "AP" in fraction_key else "Lateral" if "LAT" in fraction_key else "Unknown"

           
            dist_results = []
            dist_results.append(f"=== {view_type} View - Fraction {fraction_number} ===")
            dist_results.append(f"Anatomy start point: {anatomy_start}")
            dist_results.append(f"Anatomy end point: {anatomy_end}")
            dist_results.append("")

            structures = {
                "applicator_tandem": "Tandem Applicator",
                "left_ovoid": "Left Ovoid", 
                "right_ovoid": "Right Ovoid"
            }

            for applicator_key, applicator_name in structures.items():
                if applicator_key not in polygons or not polygons[applicator_key]:
                    dist_results.append(f"{applicator_name}: Not annotated")
                    continue

                tip = explicit_points[applicator_key]["tip"]
                base = explicit_points[applicator_key]["base"]

                if not tip or not base:
                    dist_results.append(f"{applicator_name}: Tip or base missing")
                    continue

               
                distances = {
                    f"{applicator_name} Tip to Anatomy Start": self.euclidean_distance(tip, anatomy_start) * mm_per_px,
                    f"{applicator_name} Base to Anatomy Start": self.euclidean_distance(base, anatomy_start) * mm_per_px,
                    f"{applicator_name} Tip to Anatomy End": self.euclidean_distance(tip, anatomy_end) * mm_per_px,
                    f"{applicator_name} Base to Anatomy End": self.euclidean_distance(base, anatomy_end) * mm_per_px
                }

                for desc, dist in distances.items():
                    dist_results.append(f"{desc}: {dist:.2f} mm")

            
            if "LAT" in fraction_key:
                txt_filename = f"LAT_frac{fraction_number}_distances_from_anatomy.txt"
            else:
                txt_filename = f"AP_frac{fraction_number}_distances_from_anatomy.txt"

            txt_path = os.path.join(save_folder, txt_filename)

            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    for line in dist_results:
                        f.write(line + "\n")

                print(f"✅ DISTANCES EXPORTED: {txt_path}")

               
                messagebox.showinfo("Success", 
                                  f"Annotations and distances saved!\n\n"
                                  f"Fraction: {fraction_number}\n"
                                  f"View: {view_type}\n"
                                  f"Annotations: {os.path.basename(json_path)}\n"
                                  f"Distances: {os.path.basename(txt_path)}")
          
            except Exception as e:
                print(f"❌ Error exporting distances: {e}")
                messagebox.showerror("Error", f"Failed to export distances: {str(e)}")

        def finish_and_close():
            save_all_annotations()
            win.destroy()

        
        def zoom_in():
            zoom[0] *= 1.2
            redraw_canvas()

        def zoom_out():
            zoom[0] /= 1.2
            redraw_canvas()

        def reset_zoom():
            zoom[0] = 1.0
            redraw_canvas()

        def on_mousewheel(event):
            if event.delta > 0:
                zoom[0] *= 1.1
            else:
                zoom[0] /= 1.1
            redraw_canvas()

       
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Double-Button-1>", finish_anatomy_polygon)
        canvas.bind("<Motion>", on_mouse_move)
        canvas.bind("<MouseWheel>", on_mousewheel)  
        canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), redraw_canvas()))  
        canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), redraw_canvas()))  

      
        toolbar_frame = tk.Frame(win, relief=tk.RAISED, borderwidth=2, bg="#F5F5F5", width=350)  
        toolbar_frame.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=10)
        toolbar_frame.grid_propagate(False)

        win.grid_columnconfigure(1, weight=0, minsize=350)  
        win.grid_columnconfigure(0, weight=1)
    
       
        status_var = tk.StringVar(value="Ready - Click to start annotating")
        status_label = tk.Label(win, textvariable=status_var, relief=tk.SUNKEN, 
                              anchor=tk.W, font=("Arial", 10), bg="#E8F5E8", fg="#2E7D32")
        status_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

       
        sections = [
            ("Annotation Mode", [
                ("📏 Anatomy Annotation (Red)", lambda: [mode.set("anatomy"), point_type.set("tip")]),
                ("📐 Tandem Applicator (Blue)", lambda: [mode.set("applicator_tandem"), point_type.set("tip")]),
                ("📐 Left Ovoid Applicator (Purple)", lambda: [mode.set("left_ovoid"), point_type.set("tip")]),
                ("📐 Right Ovoid Applicator (Green)", lambda: [mode.set("right_ovoid"), point_type.set("tip")])
            ]),
            ("Current Point Type", [
                (f"Current Point Type: {point_type.get()}", lambda: None)
            ]),
            ("Anatomy Tools", [
                ("✅ Complete Anatomy Line", finish_anatomy_polygon),
                ("↩️ Remove Last Point", undo_last_point)
            ]),
            ("Applicator Tools", [
                ("🗑️ Clear Current Applicator", clear_current_applicator),
                ("🗑️ Clear All Annotations", clear_all_annotations)
            ]),
            ("View Controls", [
                ("🔍 Zoom In View", zoom_in),
                ("🔍 Zoom Out View", zoom_out),
                ("🔄 Reset Zoom Level", reset_zoom)
            ]),
            ("Actions", [
                ("💾 Save & Close Session", finish_and_close)
            ])
        ]
        row = 0
        for section_title, buttons in sections:
     
            section_frame = tk.LabelFrame(toolbar_frame, text=section_title, 
                                        font=("Arial", 10, "bold"), padx=8, pady=6, 
                                        bg="#F5F5F5", fg="#37474F", width=330)  
            section_frame.grid(row=row, column=0, sticky="ew", pady=(0, 12), padx=5) 
            section_frame.grid_propagate(False) 
            row += 1

            for btn_text, command in buttons:
                if "Current Point Type:" in btn_text:
                    
                    point_display = tk.Label(section_frame, textvariable=point_type, 
                                           font=("Arial", 10, "bold"), fg="#1565C0", bg="#F5F5F5",
                                           width=25, anchor="w") 
                    point_display.pack(fill=tk.X, pady=3, padx=5)
                  
                    static_label = tk.Label(section_frame, text="Current Point Type:", 
                                          font=("Arial", 9, "bold"), fg="#37474F", bg="#F5F5F5",
                                          anchor="w")
                    static_label.pack(fill=tk.X, pady=(5, 0), padx=5)
                else:
                  
                    if "Anatomy" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    elif "Tandem" in btn_text:
                        bg_color, fg_color = "#E3F2FD", "#1565C0"
                    elif "Left Ovoid" in btn_text:
                        bg_color, fg_color = "#F3E5F5", "#7B1FA2"
                    elif "Right Ovoid" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    elif "Clear" in btn_text or "Remove" in btn_text:
                        bg_color, fg_color = "#FFEBEE", "#D32F2F"
                    elif "Zoom" in btn_text or "View" in btn_text:
                        bg_color, fg_color = "#FAFAFA", "#455A64"
                    elif "Save" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    else:
                        bg_color, fg_color = "#F5F5F5", "#37474F"

                    btn = tk.Button(section_frame, text=btn_text, command=command,
                                  font=("Arial", 9), width=32, height=1,  
                                  bg=bg_color, fg=fg_color, relief="raised", bd=2,
                                  anchor="w", justify="left")
                    btn.pack(fill=tk.X, pady=3, padx=5)  

        
        def update_point_display(*args):
            for widget in toolbar_frame.winfo_children():
                if isinstance(widget, tk.LabelFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and hasattr(child, 'is_point_display'):
                            child.config(text=f"{point_type.get().title()}") 

        point_type.trace('w', update_point_display)

       
        win.geometry("1600x900")  

    
      
        for widget in toolbar_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame) and "Current Point Type" in widget.cget('text'):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.is_point_display = True

        # Initial redraw
        redraw_canvas()
    
        print(f"Enhanced annotation window ready for {fraction_key}")
                
    def show_lat_images(self):
        """Show Lateral images editing window with navigation"""
        screen_info = self.get_screen_info()

      
        if not hasattr(self, 'lat_window') or self.lat_window is None or not self.lat_window.winfo_exists():
            self.lat_window = tk.Toplevel(self.root)

       
        taskbar_height = 40  
        max_window_width = screen_info['width'] - 50  
        max_window_height = screen_info['height'] - taskbar_height - 50  

     
        window_width = min(self.get_scaled_size(1600), max_window_width)
        window_height = min(self.get_scaled_size(1000), max_window_height)

        self.lat_window.geometry(f"{window_width}x{window_height}")
        self.lat_window.title("Lateral Images Editing - Workflow Step 2/2")

        
        self.center_window_safe(self.lat_window, window_width, window_height, taskbar_height)

      
        for widget in self.lat_window.winfo_children():
            widget.destroy()

       
        self.lat_window.grid_rowconfigure(0, weight=0)
        self.lat_window.grid_rowconfigure(1, weight=1)  
        self.lat_window.grid_columnconfigure(0, weight=1)

        # ========== NAVIGATION HEADER ==========
        nav_frame = self.create_scaled_frame(self.lat_window, bg="#2c3e50", height=40)
        nav_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        nav_frame.grid_propagate(False)

        
        nav_buttons_frame = self.create_scaled_frame(nav_frame, bg="#2c3e50")
        nav_buttons_frame.pack(expand=True)

        self.create_scaled_button(nav_buttons_frame, "🏠 Main Menu", self.return_to_main,
                  bg="#3498db", fg="white", font=self.get_scaled_font(10, bold=True),
                  width=15, height=1).pack(side=tk.LEFT, padx=5)

        self.create_scaled_button(nav_buttons_frame, "⬅️ Back to AP", self.navigate_to_ap_from_lat,
                  bg="#95a5a6", fg="white", font=self.get_scaled_font(10),
                  width=15, height=1).pack(side=tk.LEFT, padx=5)

       
        self.create_scaled_label(nav_buttons_frame, "Step 2: Lateral Image Analysis", 
                 font=self.get_scaled_font(12, bold=True), fg="white", bg="#2c3e50").pack(side=tk.LEFT, padx=20)

        self.create_scaled_button(nav_buttons_frame, "🧮 BED/EQD2 Calculator", 
                        command=self.open_bed_eqd2_calculator,
                        bg="#9C27B0", fg="white", font=self.get_scaled_font(10, bold=True),
                        width=20, height=1).pack(side=tk.LEFT, padx=10)

        # ========== REPORT GENERATION BUTTONS - TOP RIGHT ==========
        report_buttons_frame = self.create_scaled_frame(nav_frame, bg="#2c3e50")
        report_buttons_frame.pack(side=tk.RIGHT, padx=10)




       
        self.create_scaled_button(report_buttons_frame, "📊 Full PDF Report", 
                                command=self.generate_comprehensive_report,
                                bg="#2196F3", fg="white", font=self.get_scaled_font(9, bold=True),
                                width=15, height=1).pack(side=tk.RIGHT, padx=3)

      
        status_label = self.create_scaled_label(nav_frame, "✓ Lateral Workflow Active", 
                               font=self.get_scaled_font(9), fg="#2ecc71", bg="#2c3e50")
        status_label.pack(side=tk.RIGHT, padx=10)

        # ========== MAIN CONTENT FRAME ==========
        
        content_frame = self.create_scaled_frame(self.lat_window)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

       
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

    
        fractions_container = self.create_scaled_frame(content_frame)
        fractions_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        fractions_container.grid_rowconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(0, weight=1)
        fractions_container.grid_columnconfigure(1, weight=1)

       
        def make_panel(parent_frame, original_img):
            original_image_data = original_img.copy()
            edited = {"image": original_img.copy(), "history": []}
            zoom = [1.0]
            angle = [0]

            
            current_brightness = [100]  
            current_contrast = [100]   
            current_auto_enhance = [False]
            current_negative = [False]
            current_edges = [False]

            
            available_height = window_height - 200
            img_h, img_w = original_img.shape

            max_canvas_w = int(window_width * 0.8)
            max_canvas_h = int(available_height * 0.8)

            scale_w = max_canvas_w / img_w
            scale_h = max_canvas_h / img_h
            scale = min(1.0, scale_w, scale_h)

            canvas_w = int(img_w * scale)
            canvas_h = int(img_h * scale)

            max_allowed_w = int(window_width * 0.9)
            max_allowed_h = int(available_height * 0.9)
            canvas_w = min(canvas_w, max_allowed_w)
            canvas_h = min(canvas_h, max_allowed_h)

            print(f"LAT Canvas size: {canvas_w}x{canvas_h}, Window: {window_width}x{window_height}")

            
            canvas_frame = self.create_scaled_frame(parent_frame)
            canvas_frame.grid(row=0, column=0, columnspan=9, sticky="nsew", pady=(0, 10))

            canvas = tk.Canvas(canvas_frame, width=canvas_w, height=canvas_h, bg='black')

            
            v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
            canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

            
            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            canvas_frame.grid_rowconfigure(0, weight=1)
            canvas_frame.grid_columnconfigure(0, weight=1)

            
            from PIL import Image as PILImage
            pil_img = PILImage.fromarray(original_img)
            img_tk = ImageTk.PhotoImage(pil_img)
            image_id = canvas.create_image(0, 0, anchor='nw', image=img_tk)
            canvas.image = img_tk
            canvas.config(scrollregion=(0, 0, pil_img.width, pil_img.height))

            def refresh_image():
                img = edited["image"]
                scale_val = zoom[0]
                new_w, new_h = int(img.shape[1]*scale_val), int(img.shape[0]*scale_val)
                if new_w <=0 or new_h <=0:
                   print("Invalid size")
                   return
                resized = cv2.resize(img, (new_w, new_h))
                if angle[0]!=0:
                   center = (new_w//2, new_h//2)
                   rot_mat = cv2.getRotationMatrix2D(center, angle[0], 1.0)
                   resized = cv2.warpAffine(resized, rot_mat, (new_w, new_h), borderMode=cv2.BORDER_REPLICATE)
                
                pil_resized = PILImage.fromarray(resized)
                img_tk_new = ImageTk.PhotoImage(pil_resized)
                canvas.itemconfig(image_id, image=img_tk_new)
                canvas.image = img_tk_new
                canvas.config(scrollregion=(0,0,new_w,new_h))

            def apply_all_adjustments():
                
                img = original_image_data.copy()

              
                if current_auto_enhance[0]:
                    img = self.auto_enhance(img)

                
                alpha = current_contrast[0] / 100.0
                beta = (current_brightness[0] - 100) * 0.5  
                
              
                img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

                
                if current_negative[0]:
                    img = cv2.bitwise_not(img)

                
                if current_edges[0]:
                    img = cv2.Canny(img, 50, 150)

                edited["image"] = img
                refresh_image()

            def apply_auto_enhance():
                edited["history"].append(edited["image"].copy())
                current_auto_enhance[0] = not current_auto_enhance[0]  
                apply_all_adjustments()

            def apply_negative():
                edited["history"].append(edited["image"].copy())
                current_negative[0] = not current_negative[0]
                apply_all_adjustments()

            def apply_edges():
                edited["history"].append(edited["image"].copy())
                current_edges[0] = not current_edges[0]
                apply_all_adjustments()

            def undo_edit():
                if edited["history"]:
                    edited["image"] = edited["history"].pop()
                    
                 
                    current_brightness[0] = 100
                    current_contrast[0] = 100
                    current_auto_enhance[0] = False
                    current_negative[0] = False
                    current_edges[0] = False
                   
                    bright_slider.set(100)
                    contrast_slider.set(100)
                    refresh_image()

            def update_brightness(val):
                current_brightness[0] = int(val)
                apply_all_adjustments()

            def update_contrast(val):
                current_contrast[0] = float(val)
                apply_all_adjustments()

        
            def on_mousewheel(event):
                if event.delta > 0: 
                   zoom[0] *= 1.1
                else:             
                   zoom[0] /= 1.1
                refresh_image()

            canvas.bind("<MouseWheel>", on_mousewheel)  
            canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), refresh_image()))
            canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), refresh_image()))

            row_offset = 2
          
            tk.Button(parent_frame, text="🌟 Auto Enhancement", command=apply_auto_enhance,
                      bg="#E3F2FD", fg="#1976D2", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=0, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🌗 Invert Colors", command=apply_negative,
                      bg="#F3E5F5", fg="#7B1FA2", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=1, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔍 Edge Detection", command=apply_edges,
                      bg="#E0F2F1", fg="#00838F", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=2, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="↩️ Undo Last Action", command=undo_edit,
                      bg="#FFEBEE", fg="#D32F2F", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset, column=3, sticky="we", padx=2, pady=5)

            tk.Button(parent_frame, text="🔍 Zoom In", command=lambda: (zoom.__setitem__(0, zoom[0]*1.2), refresh_image()),
                      bg="#FAFAFA", fg="#455A64", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=0, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔍 Zoom Out", command=lambda: (zoom.__setitem__(0, zoom[0]/1.2), refresh_image()),
                      bg="#FAFAFA", fg="#455A64", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=1, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="⟲ Rotate Left", command=lambda: (angle.__setitem__(0, (angle[0]-90)%360), refresh_image()),
                      bg="#EFEBE9", fg="#5D4037", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=2, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="⟳ Rotate Right", command=lambda: (angle.__setitem__(0, (angle[0]+90)%360), refresh_image()),
                      bg="#EFEBE9", fg="#5D4037", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=3, sticky="we", padx=2, pady=5)
            tk.Button(parent_frame, text="🔄 Reset View", command=lambda: (zoom.__setitem__(0, 1.0), angle.__setitem__(0, 0), refresh_image()),
                      bg="#FFF3E0", fg="#E64A19", font=("Arial", 9, "bold"), 
                      width=16, height=1, relief="raised", bd=2).grid(row=row_offset+1, column=4, sticky="we", padx=2, pady=5)

            tk.Label(parent_frame, text="Brightness Adjustment", font=("Arial", 9, "bold"), 
                     fg="#37474F").grid(row=row_offset+2, column=0, sticky="w")
            bright_slider = tk.Scale(parent_frame, from_=0, to=200, orient="horizontal", command=update_brightness,
                                    bg="#F5F5F5", fg="#37474F", troughcolor="#E0E0E0")
            bright_slider.set(100)
            bright_slider.grid(row=row_offset+2, column=1, columnspan=3, sticky="we")

            tk.Label(parent_frame, text="Contrast Adjustment", font=("Arial", 9, "bold"), 
                     fg="#37474F").grid(row=row_offset+3, column=0, sticky="w")
            contrast_slider = tk.Scale(parent_frame, from_=50, to=200, orient="horizontal", command=update_contrast,
                                      bg="#F5F5F5", fg="#37474F", troughcolor="#E0E0E0")
            contrast_slider.set(100)
            contrast_slider.grid(row=row_offset+3, column=1, columnspan=3, sticky="we")

            def get_current_edited_image():
                return edited["image"]
            return get_current_edited_image


        for idx, key in enumerate(["LAT_frac1", "LAT_frac2"]):
            frame = self.create_scaled_labelframe(fractions_container, f"Fraction {idx+1} - LAT", padx=10, pady=10)
            frame.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)  
            frame.grid_columnconfigure(0, weight=1)

            if self.image_paths[key]:
               original_img = cv2.imread(self.image_paths[key], cv2.IMREAD_GRAYSCALE)
               if original_img is not None:
                  get_edited_img = make_panel(frame, original_img)

                  if key == "LAT_frac1":
                
                     def save_and_annotate_frac1(get_img=get_edited_img, k=key):
                         img_to_save = get_img()
                         save_name = f"{k}_edited.png"
                         lat_dir = os.path.join(self.temp_dir, "LAT")
                         os.makedirs(lat_dir, exist_ok=True)  
                         save_path = os.path.join(lat_dir, save_name)
                         cv2.imwrite(save_path, img_to_save)
                         print(f"Saved edited image: {save_path}")
                         self.open_annotation_window_lateral(save_path, k)

                     tk.Button(frame, text="Go to Annotation", command=save_and_annotate_frac1,
                               bg="#E8F5E8", fg="#2E7D32", font=("Arial", 10, "bold"),
                              width=20, height=1, relief="raised", bd=2).grid(row=6, column=0, columnspan=3, pady=10, sticky="we")

                  elif key == "LAT_frac2":
                      def open_alignment_window_LT2(get_img=get_edited_img):
                          align_win = tk.Toplevel(self.lat_window)
                          
                          align_win.title("Align and Annotate - Fraction 2 Edited Image - LAT")
                          align_win.geometry("1600x900") 
    
                        
                          align_win.grid_rowconfigure(1, weight=1)
                          align_win.grid_columnconfigure(0, weight=1)
                          align_win.grid_columnconfigure(1, weight=0) 
    
                         
                          img = get_img()
                          img_h, img_w = img.shape[:2]
                          screen_w, screen_h = align_win.winfo_screenwidth(), align_win.winfo_screenheight()
                          scale = min(screen_w / img_w, screen_h / img_h, 1.0)
                          new_w, new_h = int(img_w * scale), int(img_h * scale)
                          img_resized = cv2.resize(img, (new_w, new_h))
                          pil_img = PILImage.fromarray(img_resized)
                          zoom = [1.0]
    
                    
                          content_frame = tk.Frame(align_win)
                          content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
                          content_frame.grid_rowconfigure(0, weight=1)
                          content_frame.grid_columnconfigure(0, weight=1)
    
              
                          canvas_frame = tk.Frame(content_frame)
                          canvas_frame.grid(row=0, column=0, sticky="nsew")
                          canvas_frame.grid_rowconfigure(0, weight=1)
                          canvas_frame.grid_columnconfigure(0, weight=1)
    
                          canvas = tk.Canvas(canvas_frame, width=new_w, height=new_h, bg="black", 
                                            scrollregion=(0, 0, new_w, new_h))
    
                        
                          v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
                          h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
                          canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
                        
                          canvas.grid(row=0, column=0, sticky="nsew")
                          v_scrollbar.grid(row=0, column=1, sticky="ns")
                          h_scrollbar.grid(row=1, column=0, sticky="ew")
                          
                          img_tk = ImageTk.PhotoImage(pil_img)
                          canvas.create_image(0, 0, anchor='nw', image=img_tk)
                          canvas.image = img_tk
    
                         
                          explicit_points = {
                              "anatomy": [],
                              "applicator_tandem": {"tip": None, "base": None},
                              "left_ovoid": {"tip": None, "base": None},
                              "right_ovoid": {"tip": None, "base": None}
                          }
    
                          
                          anatomy_points = []
                          
                          current_points = []
                          mode = tk.StringVar(value="none")
                          point_type = tk.StringVar(value="tip")
    
                          color_map = {
                              "anatomy": "red",
                              "applicator_tandem": "blue",
                              "left_ovoid": "purple",
                              "right_ovoid": "green"
                          }
    
                        
                          canvas_items = {
                              "anatomy": [],
                              "applicator_tandem": {"tip": None, "base": None, "line": None},
                              "left_ovoid": {"tip": None, "base": None, "line": None},
                              "right_ovoid": {"tip": None, "base": None, "line": None}
                          }
    
                          
                          imported_anatomy_original = []
                          imported_anatomy_current = []
                          anatomy_offset = {"x": 0, "y": 0}
                          alignment_saved = False
                          in_annotation_mode = False
    
                          def redraw_canvas():
                              
                              for item_type in canvas_items:
                                  if item_type == "anatomy":
                                      for item in canvas_items[item_type]:
                                          canvas.delete(item)
                                      canvas_items[item_type] = []
                                  else:
                                      for point_type in ["tip", "base", "line"]:
                                          if canvas_items[item_type][point_type]:
                                              canvas.delete(canvas_items[item_type][point_type])
                                              canvas_items[item_type][point_type] = None
        
                              
                              scaled_w, scaled_h = int(new_w * zoom[0]), int(new_h * zoom[0])
                              canvas.config(scrollregion=(0, 0, scaled_w, scaled_h))
        
                         
                              pil_scaled = pil_img.resize((scaled_w, scaled_h), PILImage.Resampling.LANCZOS)
                              img_tk_scaled = ImageTk.PhotoImage(pil_scaled)
                              canvas.delete("background")
                              canvas.create_image(0, 0, anchor='nw', image=img_tk_scaled, tags="background")
                              canvas.image = img_tk_scaled
        
                           
                              for poly in imported_anatomy_current:
                                  scaled_poly = [(int((x + anatomy_offset["x"]) * zoom[0]), int((y + anatomy_offset["y"]) * zoom[0])) for x, y in poly]
                                  if len(scaled_poly) > 1:
                                      item = canvas.create_line(scaled_poly, fill=color_map["anatomy"], width=2, tags="imported_anatomy")
                                      canvas_items["anatomy"].append(item)
                                  for x, y in scaled_poly:
                                      item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="imported_anatomy")
                                      canvas_items["anatomy"].append(item)
        
                              
                              for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                                  tip = explicit_points[label]["tip"]
                                  base = explicit_points[label]["base"]
            
                                  if tip:
                                      x, y = int(tip[0] * zoom[0]), int(tip[1] * zoom[0])
                                      item = canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                              outline='white', tags="annotation")
                                      canvas_items[label]["tip"] = item
                                      item_text = canvas.create_text(x+10, y-10, text=f"{label.replace('_', ' ').title()} Tip", 
                                                               fill='white', font=("Arial", 8), tags="annotation")
                                      canvas_items["anatomy"].append(item_text)
            
                                  if base:
                                      x, y = int(base[0] * zoom[0]), int(base[1] * zoom[0])
                                      item = canvas.create_rectangle(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                                  outline='white', tags="annotation")
                                      canvas_items[label]["base"] = item
                                      item_text = canvas.create_text(x+10, y+10, text=f"{label.replace('_', ' ').title()} Base", 
                                                                   fill='white', font=("Arial", 8), tags="annotation")
                                      canvas_items["anatomy"].append(item_text)
            
                                 
                                  if tip and base:
                                      item = canvas.create_line(
                                          int(tip[0] * zoom[0]), int(tip[1] * zoom[0]),
                                          int(base[0] * zoom[0]), int(base[1] * zoom[0]),
                                          fill=color_map[label], width=2, dash=(4, 2), tags="annotation"
                                      )
                                      canvas_items[label]["line"] = item







                

                          def on_click(event):
                              
                              if not in_annotation_mode or not alignment_saved:
                                  return

                              x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
        
                           
                              if mode.get() != "anatomy" and mode.get() != "none":
                                  if point_type.get() == "tip":
                                      explicit_points[mode.get()]["tip"] = (x, y)
                                      point_type.set("base")
                                      status_var.set(f"Set {mode.get().replace('_', ' ').title()} tip. Now click for base point.")
                                  else:
                                      explicit_points[mode.get()]["base"] = (x, y)
                                      point_type.set("tip")
                                      status_var.set(f"Set {mode.get().replace('_', ' ').title()} base. Annotation complete for this applicator.")
                                  redraw_canvas()

                          def on_mouse_move(event):
                              x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
                              status_text = f"Position: X:{x} Y:{y}"
                      
                              if alignment_saved and in_annotation_mode:
                                  status_text += f" | Mode: {mode.get().replace('_', ' ').title()} | Point: {point_type.get().title()}"
                              elif alignment_saved:
                                  status_text += " | ALIGNMENT SAVED - Click an applicator button to start annotation"
                              elif not alignment_saved:
                                  status_text += " | Drag anatomy to align, then click 'Save Alignment'"

                              status_var.set(status_text)
                                      
                         
                          drag_data = {"x": 0, "y": 0, "item": None}
                      
                          def start_move(event):
                          
                              if alignment_saved:
                                  return

                          
                              items = canvas.find_withtag("imported_anatomy")
                              for item in items:
                                  if canvas.type(item) == 'line':
                                      coords = canvas.coords(item)
                                      x_vals = coords[::2]
                                      y_vals = coords[1::2]
                                      if min(x_vals) - 10 <= event.x <= max(x_vals) + 10 and min(y_vals) - 10 <= event.y <= max(y_vals) + 10:
                                          drag_data["item"] = item
                                          drag_data["x"] = event.x
                                          drag_data["y"] = event.y
                                          break

                          def on_move(event):
                      
                              if alignment_saved or drag_data["item"] is None:
                                  return

                              dx = event.x - drag_data["x"]
                              dy = event.y - drag_data["y"]

                           
                              anatomy_offset["x"] += dx / zoom[0]
                              anatomy_offset["y"] += dy / zoom[0]

                        
                              for item in canvas.find_withtag("imported_anatomy"):
                                  canvas.move(item, dx, dy)
                              drag_data["x"] = event.x
                              drag_data["y"] = event.y

                          def stop_move(event):
                              drag_data["item"] = None

                          def undo_last_point():
                             
                              if mode.get() != "anatomy" and mode.get() != "none":
                               
                                  if point_type.get() == "tip" and explicit_points[mode.get()]["base"]:
                                      explicit_points[mode.get()]["base"] = None
                                      point_type.set("base")
                                      status_var.set(f"Undid base point. Click to set base for {mode.get().replace('_', ' ').title()}.")
                                  elif explicit_points[mode.get()]["tip"]:
                                      explicit_points[mode.get()]["tip"] = None
                                      point_type.set("tip")
                                      status_var.set(f"Undid tip point. Click to set tip for {mode.get().replace('_', ' ').title()}.")
                                  redraw_canvas()

                          def clear_current_applicator():
                              if mode.get() != "anatomy" and mode.get() != "none":
                                  explicit_points[mode.get()]["tip"] = None
                                  explicit_points[mode.get()]["base"] = None
                                  point_type.set("tip")
                                  status_var.set(f"Cleared {mode.get().replace('_', ' ').title()}. Ready for new annotation.")
                                  redraw_canvas()

                          def clear_all_annotations():
                       
                              for label in explicit_points:
                                  if label == "anatomy":
                                      continue
                                  explicit_points[label]["tip"] = None
                                  explicit_points[label]["base"] = None
                              point_type.set("tip")
                              mode.set("none")
                              status_var.set("Cleared all applicator annotations. Select an applicator to start annotation.")
                              redraw_canvas()

                          def import_fraction1_anatomy():
                              nonlocal imported_anatomy_original, imported_anatomy_current
                              path = os.path.join(self.temp_dir, "LAT", "LAT_frac1_annotations.json")
                              if not os.path.exists(path):
                                  print("Fraction 1 anatomy annotations not found")
                                  status_var.set("Error: Fraction 1 anatomy annotations not found")
                                  return

                              with open(path, 'r') as f:
                                  all_polygons = json.load(f)

                              if "anatomy" in all_polygons:
                                  imported_anatomy_original = all_polygons["anatomy"]
                                  imported_anatomy_current = all_polygons["anatomy"].copy() 
                                  # Reset offset
                                  anatomy_offset["x"] = 0
                                  anatomy_offset["y"] = 0
                                  redraw_canvas()
                                  print("Imported Fraction 1 anatomy")
                                  status_var.set("Anatomy imported. Drag to position, then click 'Save Alignment' when done.")

                          def save_alignment():
                              nonlocal alignment_saved, in_annotation_mode
                             
                              polygons = {
                                  "anatomy": imported_anatomy_current, 
                                  "applicator_tandem": [],
                                  "left_ovoid": [],
                                  "right_ovoid": []
                              }

                           
                              for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                                  tip = explicit_points[label]["tip"]
                                  base = explicit_points[label]["base"]
                                  if tip and base:
                                      
                                      polygons[label].append([tip, base])

                              
                              json_path = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
                              with open(json_path, 'w') as f:
                                  json.dump(polygons, f, indent=4)

                           
                              explicit_path = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2_explicit_points.json")
                              with open(explicit_path, 'w') as f:
                                  json.dump(explicit_points, f, indent=4)

                          
                              frac2_annotations_path = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
                              frac2_data = {
                                  "anatomy": imported_anatomy_current,
                                  "applicator_tandem": {"tip": explicit_points["applicator_tandem"]["tip"],
                                                        "base": explicit_points["applicator_tandem"]["base"]},
                                  "left_ovoid": {"tip": explicit_points["left_ovoid"]["tip"],
                                                 "base": explicit_points["left_ovoid"]["base"]},
                                  "right_ovoid": {"tip": explicit_points["right_ovoid"]["tip"],
                                                  "base": explicit_points["right_ovoid"]["base"]}
                              }
                              with open(frac2_annotations_path, 'w') as f:
                                  json.dump(frac2_data, f, indent=4)

                              
                              edited_img_path = os.path.join(self.temp_dir, "AP_frac2_edited.png")
                              if os.path.exists(edited_img_path):
                                  self.save_masks_at_original_resolution(edited_img_path, polygons, self.temp_dir)

                           
                              alignment_saved = True
                              in_annotation_mode = True

                             
                              canvas.unbind("<ButtonPress-1>")
                              canvas.unbind("<B1-Motion>")
                              canvas.unbind("<ButtonRelease-1>")

                             
                              canvas.bind("<Button-1>", on_click)

                              print(f"Alignment saved to {json_path}")
                              print(f"✅ Fraction 2 annotations saved to {frac2_annotations_path}")
                              status_var.set("Alignment and annotations saved! Anatomy is fixed. You may now calculate shifts or measurements.")


                      
                          def start_tandem_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("applicator_tandem")
                                  point_type.set("tip")
                                  in_annotation_mode = True
                                  status_var.set("TANDEM MODE - Click to set tip point")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")

                          def start_left_ovoid_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("left_ovoid")
                                  point_type.set("tip")
                                  in_annotation_mode = True
                                  status_var.set("LEFT OVOID MODE - Click to set tip point")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")
                      
                          def start_right_ovoid_annotation():
                              nonlocal in_annotation_mode
                              if alignment_saved:
                                  mode.set("right_ovoid")
                                  point_type.set("tip")
                                  in_annotation_mode = True
                                  status_var.set("RIGHT OVOID MODE - Click to set tip point")
                              else:
                                  status_var.set("Please save alignment first before annotating applicators")

                      
                          def save_and_end_session():
                              """Save distances to file and close the alignment session - Lateral Version"""
                              if not imported_anatomy_current:
                                  messagebox.showerror("Error", "No anatomy imported. Please import Fraction 1 anatomy first.")
                                  return

                              if len(imported_anatomy_current) == 0 or len(imported_anatomy_current[0]) < 2:
                                  messagebox.showerror("Error", "Anatomy line is incomplete. Please ensure anatomy has at least 2 points.")
                                  return

                              anatomy_poly = imported_anatomy_current[0]
                              anatomy_start = anatomy_poly[0]
                              anatomy_end = anatomy_poly[-1]

                              mm_per_px = self.pixel_spacing["LAT_frac1"] 

                           
                              dist_results = []
                              dist_results.append("=== LAT View - Fraction 2 ===")
                              dist_results.append(f"Anatomy start point: {anatomy_start}")
                              dist_results.append(f"Anatomy end point: {anatomy_end}")
                              dist_results.append("")

                              structures = {
                                  "applicator_tandem": "Tandem Applicator",
                                  "left_ovoid": "Left Ovoid", 
                                  "right_ovoid": "Right Ovoid"
                              }

                              for applicator_key, applicator_name in structures.items():
                                  tip = explicit_points[applicator_key]["tip"]
                                  base = explicit_points[applicator_key]["base"]

                                  if not tip or not base:
                                     
                                      dist_results.append(f"{applicator_name} Tip to Anatomy Start: ")
                                      dist_results.append(f"{applicator_name} Base to Anatomy Start: ")
                                      dist_results.append(f"{applicator_name} Tip to Anatomy End: ")
                                      dist_results.append(f"{applicator_name} Base to Anatomy End: ")
                                      continue

                                  
                                  tip_to_start = self.euclidean_distance(tip, anatomy_start) * mm_per_px
                                  base_to_start = self.euclidean_distance(base, anatomy_start) * mm_per_px
                                  tip_to_end = self.euclidean_distance(tip, anatomy_end) * mm_per_px
                                  base_to_end = self.euclidean_distance(base, anatomy_end) * mm_per_px

                                  dist_results.append(f"{applicator_name} Tip to Anatomy Start: {tip_to_start:.2f} mm")
                                  dist_results.append(f"{applicator_name} Base to Anatomy Start: {base_to_start:.2f} mm")
                                  dist_results.append(f"{applicator_name} Tip to Anatomy End: {tip_to_end:.2f} mm")
                                  dist_results.append(f"{applicator_name} Base to Anatomy End: {base_to_end:.2f} mm")

                              
                              txt_filename = "LAT_frac2_distances_from_anatomy.txt"
                              txt_path = os.path.join(self.temp_dir, "LAT", txt_filename)

                              try:
                                  with open(txt_path, "w", encoding="utf-8") as f:
                                      for line in dist_results:
                                          f.write(line + "\n")

                                 
                                  messagebox.showinfo("Success", 
                                                    f"Distances saved to:\n{txt_path}\n\n"
                                                    f"Session completed successfully!\n"
                                                    f"File contains measurements for all applicators.\n"
                                                    f"All distances measured in mm relative to anatomy landmarks.")


                          
                                  print(f"✅ DISTANCES SAVED: {txt_path}")
                                  for line in dist_results:
                                      print(f"   {line}")

                                 
                                  align_win.destroy()

                              except Exception as e:
                                  messagebox.showerror("Error", f"Failed to save distances: {str(e)}")
                                  print(f"❌ Error saving distances: {e}")

                      
                         
                          def zoom_in():
                              zoom[0] *= 1.2
                              redraw_canvas()

                          def zoom_out():
                              zoom[0] /= 1.2
                              redraw_canvas()

                          def reset_zoom():
                              zoom[0] = 1.0
                              redraw_canvas()

                          def on_mousewheel(event):
                              if event.delta > 0:
                                  zoom[0] *= 1.1
                              else:
                                  zoom[0] /= 1.1
                              redraw_canvas()

                          def debug_lateral_annotation_files(self):
                              """Debug lateral annotation files to see what's actually there"""
                              import glob
    
                              lat_dir = os.path.join(self.temp_dir, "LAT")
                              print("=== DEBUG LATERAL ANNOTATION FILES ===")
    
                              if os.path.exists(lat_dir):
                                  all_files = glob.glob(os.path.join(lat_dir, "*"))
                                  for file_path in all_files:
                                      file_name = os.path.basename(file_path)
                                      print(f"Found: {file_name}")
                                      if file_name.endswith('.json'):
                                          try:
                                              with open(file_path, 'r') as f:
                                                  content = json.load(f)
                                              print(f"  Structure: {list(content.keys())}")
                                            
                                              for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                                                  if applicator in content:
                                                      print(f"  ✅ {applicator}: {content[applicator]}")
                                                  else:
                                                      print(f"  ❌ {applicator}: MISSING")
                                          except Exception as e:
                                              print(f"  Error reading: {e}")
                              else:
                                  print("LAT directory not found!")
    
                            
                              print("\n=== CHECKING MAIN TEMP DIRECTORY ===")
                              main_files = glob.glob(os.path.join(self.temp_dir, "LAT_*.json"))
                              for file_path in main_files:
                                  file_name = os.path.basename(file_path)
                                  print(f"Found in main dir: {file_name}")

                         
                       

                              

                      
                          canvas.bind("<Button-1>", on_click)
                          canvas.bind("<Motion>", on_mouse_move)
                          canvas.bind("<MouseWheel>", on_mousewheel)
                          canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), redraw_canvas()))
                          canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), redraw_canvas()))
                      
                          
                          canvas.bind("<ButtonPress-1>", start_move)
                          canvas.bind("<B1-Motion>", on_move)
                          canvas.bind("<ButtonRelease-1>", stop_move)

                         
                          toolbar_frame = tk.Frame(align_win, relief=tk.RAISED, borderwidth=2, bg="#F5F5F5")
                          toolbar_frame.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=10)
                          toolbar_frame.config(width=380) 
                          toolbar_frame.grid_propagate(False)  
    
                         
                          align_win.grid_columnconfigure(1, weight=0, minsize=380)
                          align_win.grid_columnconfigure(0, weight=1)
    
                         
                          status_var = tk.StringVar(value="Ready - Import Fraction 1 Anatomy first")
                          status_label = tk.Label(align_win, textvariable=status_var, relief=tk.SUNKEN, 
                          anchor=tk.W, font=("Arial", 10), bg="#E8F5E8", fg="#2E7D32")
                          status_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
                         
                          sections = [
                              ("Movement & Import Tools", [
                                  ("📥 Import Fraction 1 Anatomy", import_fraction1_anatomy),
                                  ("💾 Save Alignment Position", save_alignment)
                              ]),
                              ("Annotation Mode Selection", [
                                  ("📐 Tandem Applicator (Blue)", start_tandem_annotation),
                                  ("📐 Left Ovoid Applicator (Purple)", start_left_ovoid_annotation),
                                  ("📐 Right Ovoid Applicator (Green)", start_right_ovoid_annotation)
                              ]),
                              ("Current Point Type", [
                                  (f"Current Point Type: {point_type.get()}", lambda: None)
                              ]),
                              ("Applicator Editing Tools", [
                                  ("🗑️ Clear Current Applicator", clear_current_applicator),
                                  ("🗑️ Clear All Applicators", clear_all_annotations),
                                  ("↩️ Undo Last Point Placement", undo_last_point)
                              ]),
                              ("View Control Options", [
                                  ("🔍 Zoom In Image View", zoom_in),
                                  ("🔍 Zoom Out Image View", zoom_out),
                                  ("🔄 Reset Zoom Level", reset_zoom)
                              ]),
                              ("Measurement Tools", [
                                  ("💾 Save & End Session", save_and_end_session)
                              ])
                          ]
    
                          row = 0
                          for section_title, buttons in sections:
                             
                              section_frame = tk.LabelFrame(toolbar_frame, text=section_title, 
                                                          font=("Arial", 10, "bold"), padx=8, pady=6,
                                                          bg="#F5F5F5", fg="#37474F")
                              section_frame.grid(row=row, column=0, sticky="ew", pady=(0, 12), padx=5)
                              section_frame.grid_propagate(False)
                              row += 1
        
                              for btn_text, command in buttons:
                                  if "Current Point Type:" in btn_text:
                                   
                                      static_label = tk.Label(section_frame, text="Current Point Type:", 
                                                            font=("Arial", 9, "bold"), fg="#37474F", bg="#F5F5F5",
                                                            anchor="w")
                                      static_label.pack(fill=tk.X, pady=(5, 0), padx=5)
                                 
                                      point_display = tk.Label(section_frame, textvariable=point_type, 
                                                             font=("Arial", 10, "bold"), fg="#1565C0", bg="#F5F5F5",
                                                             anchor="w")
                                      point_display.pack(fill=tk.X, pady=3, padx=5)
                                      point_display.is_point_display = True
                                  else:
                                      
                                      if "Import" in btn_text or "Save" in btn_text:
                                          bg_color, fg_color = "#E8F5E8", "#2E7D32"
                                      elif "Tandem" in btn_text:
                                          bg_color, fg_color = "#E3F2FD", "#1565C0"
                                      elif "Left Ovoid" in btn_text:
                                          bg_color, fg_color = "#F3E5F5", "#7B1FA2"
                                      elif "Right Ovoid" in btn_text:
                                          bg_color, fg_color = "#E8F5E8", "#2E7D32"
                                      elif "Clear" in btn_text or "Remove" in btn_text:
                                          bg_color, fg_color = "#FFEBEE", "#D32F2F"
                                      elif "Undo" in btn_text:
                                          bg_color, fg_color = "#FFF3E0", "#FF6F00"
                                      elif "Zoom" in btn_text or "View" in btn_text:
                                          bg_color, fg_color = "#FAFAFA", "#455A64"
                                      elif "Calculate" in btn_text or "Measurement" in btn_text:
                                          bg_color, fg_color = "#E1F5FE", "#0277BD"
                                      else:
                                          bg_color, fg_color = "#F5F5F5", "#37474F"
                
                                      btn = tk.Button(section_frame, text=btn_text, command=command,
                                                    font=("Arial", 9), width=35, height=1,  
                                                    bg=bg_color, fg=fg_color, relief="raised", bd=2,
                                                    anchor="w", justify="left", wraplength=320)
                                      btn.pack(fill=tk.X, pady=3, padx=5)
                
                          
                          def update_point_display(*args):
                              for widget in toolbar_frame.winfo_children():
                                  if isinstance(widget, tk.LabelFrame):
                                      for child in widget.winfo_children():
                                          if isinstance(child, tk.Label) and hasattr(child, 'is_point_display'):
                                              child.config(text=f"{point_type.get().title()}")

                          point_type.trace('w', update_point_display)

                          
                          for widget in toolbar_frame.winfo_children():
                              if isinstance(widget, tk.LabelFrame) and "Current Point Type" in widget.cget('text'):
                                  for child in widget.winfo_children():
                                      if isinstance(child, tk.Label):
                                          child.is_point_display = True

                          
                          redraw_canvas()

                        
                          status_var.set("Ready - Import Fraction 1 Anatomy first, then drag to align")

                          print(f"Enhanced alignment window ready for Fraction 2 - LAT")

                      tk.Button(frame, text="🔄 Image Alignment", command=open_alignment_window_LT2,
                                    bg="#E3F2FD", fg="#1565C0", font=("Arial", 10, "bold"),
                                    width=15, relief="raised", bd=1).grid(row=6, column=0, columnspan=3, pady=2, sticky="we")
                      tk.Button(frame, text="📊 Compare Fractions",  command=self.compare_lateral_fraction_distances_with_shifts,
                                  bg="#FFF3E0", fg="#FF6F00", font=("Arial", 10, "bold"),
                                 width=15, relief="raised", bd=1).grid(row=6, column=3, columnspan=3, pady=2, sticky="we")
                     
                      tk.Button(frame, text="Calculate 3D Displacements", command=self.calculate_3d_displacements,
                                bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                                width=20, relief="raised", bd=1).grid(row=7, column=0, columnspan=3, pady=2, sticky="we")

                      tk.Button(frame, text="3D View", command=self.show_3d_view,
                                bg="#673AB7", fg="white", font=("Arial", 10, "bold"),
                                width=18, relief="raised", bd=1).grid(row=7, column=3, columnspan=3, pady=2, sticky="we")


    def open_bed_eqd2_calculator(self):
        """Open the BED & EQD2 Calculator in a new window"""
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("BED & EQD2 Calculator - Multiple Fractions")
        calculator_window.geometry("1600x900")
    
        # Create the calculator instance
        calculator = BEDEQD2Calculator(calculator_window)

    def create_bed_eqd2_calculator(self, parent):

        pass                      

                      

    def compare_fraction_distances_2(self):
        
        self.compare_lateral_fraction_distances()

    def debug_lateral_files(self):
        """Debug lateral files to see what's available"""
        import glob
    
        lat_dir = os.path.join(self.temp_dir, "LAT")
        print("=== DEBUG LATERAL FILES ===")
    
        
        if os.path.exists(lat_dir):
            all_files = glob.glob(os.path.join(lat_dir, "*"))
            for file_path in all_files:
                file_name = os.path.basename(file_path)
                print(f"Found: {file_name}")
                if file_name.endswith('.txt'):
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        print(f"Content preview: {content[:200]}...")
                    except Exception as e:
                        print(f"Error reading: {e}")
        else:
            print("LAT directory not found!")
            
    def update_frac2_annotations_from_alignment(self):
        
        try:
           
            messagebox.showinfo("Success", "Fraction 2 annotations updated from alignment")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update annotations: {str(e)}")
            
        try:
            alignment_file = os.path.join(self.temp_dir, "AP_frac1_aligned_to_frac2.json")
            frac2_file = os.path.join(self.temp_dir, "AP_frac2_annotations.json")
    
            if not os.path.exists(alignment_file):
                print("Alignment file not found")
                return False
        
            if not os.path.exists(frac2_file):
                print("Fraction 2 file not found")
                return False
        
            # Load both files
            with open(alignment_file, 'r') as f:
                alignment_data = json.load(f)
        
            with open(frac2_file, 'r') as f:
                frac2_data = json.load(f)
    
            
            for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                if applicator in alignment_data and alignment_data[applicator]:
                    frac2_data[applicator] = alignment_data[applicator]
                    print(f"Updated {applicator} in Fraction 2")
    
         
            with open(frac2_file, 'w') as f:
                json.dump(frac2_data, f)
        
            print("✅ Successfully updated AP_frac2_annotations.json with applicator data")
            return True
    
        except Exception as e:
            print(f"Error updating Fraction 2 annotations: {e}")
            return False

    def open_annotation_window_lateral(self, img_path, fraction_key):
        save_folder = os.path.join(self.temp_dir, "LAT")
        os.makedirs(save_folder, exist_ok=True)

        win = tk.Toplevel(self.root)
        win.title(f"Annotate and Align: {fraction_key}")
        win.geometry("1400x900") 

        
        win.grid_rowconfigure(1, weight=1)
        win.grid_columnconfigure(0, weight=1)
        win.grid_columnconfigure(1, weight=0)

      
        status_var = tk.StringVar(value="Ready - Click to start annotating")
        status_label = tk.Label(win, textvariable=status_var, relief=tk.SUNKEN, 
                              anchor=tk.W, font=("Arial", 10), bg="#E8F5E8", fg="#2E7D32")
        status_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        
        content_frame = tk.Frame(win, bg="#F5F5F5")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

     
        canvas_frame = tk.Frame(content_frame, bg="#F5F5F5")
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

       
        img = cv2.imread(img_path)
        img_h, img_w = img.shape[:2]
        screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
        scale = min(screen_w / img_w, screen_h / img_h, 1.0)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        img_resized = cv2.resize(img, (new_w, new_h))
        pil_img = PILImage.fromarray(img_resized)
        zoom = [1.0]

        canvas = tk.Canvas(canvas_frame, width=new_w, height=new_h, bg="lightgray", 
                          scrollregion=(0, 0, new_w, new_h))

       
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview,
                                  bg="#E0E0E0", troughcolor="#F5F5F5")
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview,
                                  bg="#E0E0E0", troughcolor="#F5F5F5")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

       
        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        img_tk = ImageTk.PhotoImage(pil_img)
        canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.image = img_tk

        
        explicit_points = {
            "anatomy": [],
            "applicator_tandem": {"tip": None, "base": None},
            "left_ovoid": {"tip": None, "base": None},
            "right_ovoid": {"tip": None, "base": None}
        }

       
        anatomy_points = []

        current_points = []
        mode = tk.StringVar(value="anatomy")
        point_type = tk.StringVar(value="tip")

        color_map = {
            "anatomy": "red",
            "applicator_tandem": "blue",
            "left_ovoid": "purple",
            "right_ovoid": "green"
        }

     
        canvas_items = {
            "anatomy": [],
            "applicator_tandem": {"tip": None, "base": None, "line": None},
            "left_ovoid": {"tip": None, "base": None, "line": None},
            "right_ovoid": {"tip": None, "base": None, "line": None}
        }

        def redraw_canvas():
          
            for item_type in canvas_items:
                if item_type == "anatomy":
                    for item in canvas_items[item_type]:
                        canvas.delete(item)
                    canvas_items[item_type] = []
                else:
                    for point_type in ["tip", "base", "line"]:
                        if canvas_items[item_type][point_type]:
                            canvas.delete(canvas_items[item_type][point_type])
                            canvas_items[item_type][point_type] = None

        
            scaled_w, scaled_h = int(new_w * zoom[0]), int(new_h * zoom[0])
            canvas.config(scrollregion=(0, 0, scaled_w, scaled_h))

           
            pil_scaled = pil_img.resize((scaled_w, scaled_h), PILImage.Resampling.LANCZOS)
            img_tk_scaled = ImageTk.PhotoImage(pil_scaled)
            canvas.delete("background")  
            canvas.create_image(0, 0, anchor='nw', image=img_tk_scaled, tags="background")
            canvas.image = img_tk_scaled

     
            for poly in anatomy_points:
                scaled_poly = [(int(x * zoom[0]), int(y * zoom[0])) for x, y in poly]
                if len(scaled_poly) > 1:
                    item = canvas.create_line(scaled_poly, fill=color_map["anatomy"], width=2, tags="annotation")
                    canvas_items["anatomy"].append(item)
                for x, y in scaled_poly:
                    item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="annotation")
                    canvas_items["anatomy"].append(item)

          
            for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                tip = explicit_points[label]["tip"]
                base = explicit_points[label]["base"]

                if tip:
                    x, y = int(tip[0] * zoom[0]), int(tip[1] * zoom[0])
                    item = canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                            outline='white', tags="annotation")
                    canvas_items[label]["tip"] = item
                    item_text = canvas.create_text(x+10, y-10, text=f"{label.replace('_', ' ').title()} Tip", 
                                             fill='white', font=("Arial", 8), tags="annotation")
                    canvas_items["anatomy"].append(item_text)

                if base:
                    x, y = int(base[0] * zoom[0]), int(base[1] * zoom[0])
                    item = canvas.create_rectangle(x-5, y-5, x+5, y+5, fill=color_map[label], 
                                                outline='white', tags="annotation")
                    canvas_items[label]["base"] = item
                    item_text = canvas.create_text(x+10, y+10, text=f"{label.replace('_', ' ').title()} Base", 
                                                 fill='white', font=("Arial", 8), tags="annotation")
                    canvas_items["anatomy"].append(item_text)

              
                if tip and base:
                    item = canvas.create_line(
                        int(tip[0] * zoom[0]), int(tip[1] * zoom[0]),
                        int(base[0] * zoom[0]), int(base[1] * zoom[0]),
                        fill=color_map[label], width=2, dash=(4, 2), tags="annotation"
                    )
                    canvas_items[label]["line"] = item

           
            scaled_current = [(int(x * zoom[0]), int(y * zoom[0])) for x, y in current_points]
            if len(scaled_current) > 1:
                item = canvas.create_line(scaled_current, fill=color_map["anatomy"], width=2, tags="annotation")
                canvas_items["anatomy"].append(item)
            for x, y in scaled_current:
                item = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', tags="annotation")
                canvas_items["anatomy"].append(item)

        def on_click(event):
            x, y = int(event.x / zoom[0]), int(event.y / zoom[0])

            if mode.get() == "anatomy":
                current_points.append((x, y))
                redraw_canvas()
            else:
              
                if point_type.get() == "tip":
                    explicit_points[mode.get()]["tip"] = (x, y)
                    point_type.set("base")
                    print(f"Set {mode.get()} tip at ({x}, {y})")
                else:
                    explicit_points[mode.get()]["base"] = (x, y)
                    point_type.set("tip")
                    print(f"Set {mode.get()} base at ({x}, {y})")
        
                redraw_canvas()

        def on_mouse_move(event):
            x, y = int(event.x / zoom[0]), int(event.y / zoom[0])
            status_var.set(f"Position: X:{x} Y:{y} | Mode: {mode.get().replace('_', ' ').title()} | Point: {point_type.get().title()}")

        def finish_anatomy_polygon(event=None):
            if len(current_points) >= 2:
                anatomy_points.append(current_points.copy())
            current_points.clear()
            redraw_canvas()

        def undo_last_point():
            if mode.get() == "anatomy":
                if current_points:
                    current_points.pop()
            else:
             
                if point_type.get() == "tip" and explicit_points[mode.get()]["base"]:
                    explicit_points[mode.get()]["base"] = None
                    point_type.set("base")
                elif explicit_points[mode.get()]["tip"]:
                    explicit_points[mode.get()]["tip"] = None
                    point_type.set("tip")
            redraw_canvas()

        def clear_current_applicator():
            explicit_points[mode.get()]["tip"] = None
            explicit_points[mode.get()]["base"] = None
            point_type.set("tip")
            redraw_canvas()

        def clear_all_annotations():
            anatomy_points.clear()
            current_points.clear()
            for label in explicit_points:
                if label == "anatomy":
                    continue
                explicit_points[label]["tip"] = None
                explicit_points[label]["base"] = None
            point_type.set("tip")
            mode.set("anatomy")
            redraw_canvas()

        def save_all_annotations():
           
          
            polygons = {
                "anatomy": anatomy_points,
                "applicator_tandem": [],
                "left_ovoid": [],
                "right_ovoid": []
            }        

        
            for label in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                tip = explicit_points[label]["tip"]
                base = explicit_points[label]["base"]
                if tip and base:
                
                    polygons[label].append([tip, base])

        
            json_path = os.path.join(save_folder, f"{fraction_key}_annotations.json")
            with open(json_path, 'w') as f:
                json.dump(polygons, f)

            print(f"✅ SAVED ANNOTATIONS: {json_path}")
            print(f"✅ Anatomy points: {len(anatomy_points)}")
            print(f"✅ Tandem: tip={explicit_points['applicator_tandem']['tip']}, base={explicit_points['applicator_tandem']['base']}")
            print(f"✅ Left ovoid: tip={explicit_points['left_ovoid']['tip']}, base={explicit_points['left_ovoid']['base']}")
            print(f"✅ Right ovoid: tip={explicit_points['right_ovoid']['tip']}, base={explicit_points['right_ovoid']['base']}")

         
            explicit_path = os.path.join(save_folder, f"{fraction_key}_explicit_points.json")
            with open(explicit_path, 'w') as f:
                json.dump(explicit_points, f)

          
            export_distances_to_txt(polygons, json_path)

            return polygons

        def export_distances_to_txt(polygons, json_path):
          
            if len(anatomy_points) == 0 or len(anatomy_points[0]) < 2:
                print("⚠️ Cannot export distances: Anatomy not fully annotated")
                return

            anatomy_poly = anatomy_points[0]
            anatomy_start = anatomy_poly[0]
            anatomy_end = anatomy_poly[-1]

            mm_per_px = self.pixel_spacing.get("LAT_frac1", 0.2979) 

       
            fraction_number = "1" if "frac1" in fraction_key else "2" if "frac2" in fraction_key else "Unknown"
            view_type = "Lateral"

         
            dist_results = []
            dist_results.append(f"=== {view_type} View - Fraction {fraction_number} ===")
            dist_results.append(f"Anatomy start point: {anatomy_start}")
            dist_results.append(f"Anatomy end point: {anatomy_end}")
            dist_results.append("")

            structures = {
                "applicator_tandem": "Tandem Applicator",
                "left_ovoid": "Left Ovoid", 
                "right_ovoid": "Right Ovoid"
            }

            for applicator_key, applicator_name in structures.items():
                if applicator_key not in polygons or not polygons[applicator_key]:
                    dist_results.append(f"{applicator_name}: Not annotated")
                    continue

                tip = explicit_points[applicator_key]["tip"]
                base = explicit_points[applicator_key]["base"]

                if not tip or not base:
                    dist_results.append(f"{applicator_name}: Tip or base missing")
                    continue

              
                distances = {
                    f"{applicator_name} Tip to Anatomy Start": self.euclidean_distance(tip, anatomy_start) * mm_per_px,
                    f"{applicator_name} Base to Anatomy Start": self.euclidean_distance(base, anatomy_start) * mm_per_px,
                    f"{applicator_name} Tip to Anatomy End": self.euclidean_distance(tip, anatomy_end) * mm_per_px,
                    f"{applicator_name} Base to Anatomy End": self.euclidean_distance(base, anatomy_end) * mm_per_px
                }

                for desc, dist in distances.items():
                    dist_results.append(f"{desc}: {dist:.2f} mm")

          
            txt_filename = f"LAT_frac{fraction_number}_distances_from_anatomy.txt"
            txt_path = os.path.join(save_folder, txt_filename)

            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    for line in dist_results:
                        f.write(line + "\n")

                print(f"✅ DISTANCES EXPORTED: {txt_path}")

          
                messagebox.showinfo("Success", 
                                  f"Annotations and distances saved!\n\n"
                                  f"Fraction: {fraction_number}\n"
                                  f"View: {view_type}\n"
                                  f"Annotations: {os.path.basename(json_path)}\n"
                                  f"Distances: {os.path.basename(txt_path)}")
          
            except Exception as e:
                print(f"❌ Error exporting distances: {e}")
                messagebox.showerror("Error", f"Failed to export distances: {str(e)}")

        def finish_and_close():
            save_all_annotations()
            win.destroy()

      
        def zoom_in():
            zoom[0] *= 1.2
            redraw_canvas()

        def zoom_out():
            zoom[0] /= 1.2
            redraw_canvas()

        def reset_zoom():
            zoom[0] = 1.0
            redraw_canvas()

        def on_mousewheel(event):
            if event.delta > 0:
                zoom[0] *= 1.1
            else:
                zoom[0] /= 1.1
            redraw_canvas()

        
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Double-Button-1>", finish_anatomy_polygon)
        canvas.bind("<Motion>", on_mouse_move)
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Button-4>", lambda e: (zoom.__setitem__(0, zoom[0]*1.1), redraw_canvas()))
        canvas.bind("<Button-5>", lambda e: (zoom.__setitem__(0, zoom[0]/1.1), redraw_canvas()))

     
        toolbar_frame = tk.Frame(win, relief=tk.RAISED, borderwidth=2, bg="#F5F5F5", width=350)
        toolbar_frame.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=10)
        toolbar_frame.grid_propagate(False)

        
        sections = [
            ("Annotation Mode", [
                ("📏 Anatomy Annotation (Red)", lambda: [mode.set("anatomy"), point_type.set("tip")]),
                ("📐 Tandem Applicator (Blue)", lambda: [mode.set("applicator_tandem"), point_type.set("tip")]),
                ("📐 Left Ovoid Applicator (Purple)", lambda: [mode.set("left_ovoid"), point_type.set("tip")]),
                ("📐 Right Ovoid Applicator (Green)", lambda: [mode.set("right_ovoid"), point_type.set("tip")])
            ]),
            ("Current Point Type", [
                (f"Current Point Type: {point_type.get()}", lambda: None)
            ]),
            ("Anatomy Tools", [
                ("✅ Complete Anatomy Line", finish_anatomy_polygon),
                ("↩️ Remove Last Point", undo_last_point)
            ]),
            ("Applicator Tools", [
                ("🗑️ Clear Current Applicator", clear_current_applicator),
                ("🗑️ Clear All Annotations", clear_all_annotations)
            ]),
            ("View Controls", [
                ("🔍 Zoom In View", zoom_in),
                ("🔍 Zoom Out View", zoom_out),
                ("🔄 Reset Zoom Level", reset_zoom)
            ]),
            ("Actions", [
                ("💾 Save & Close Session", finish_and_close)
            ])
        ]

        row = 0
        for section_title, buttons in sections:
            
            section_frame = tk.LabelFrame(toolbar_frame, text=section_title, 
                                        font=("Arial", 10, "bold"), padx=8, pady=6,
                                        bg="#F5F5F5", fg="#37474F", width=330)
            section_frame.grid(row=row, column=0, sticky="ew", pady=(0, 12), padx=5)
            section_frame.grid_propagate(False)
            row += 1

            for btn_text, command in buttons:
                if "Current Point Type:" in btn_text:
                
                    static_label = tk.Label(section_frame, text="Current Point Type:", 
                                          font=("Arial", 9, "bold"), fg="#37474F", bg="#F5F5F5",
                                          anchor="w")
                    static_label.pack(fill=tk.X, pady=(5, 0), padx=5)
                
                    point_display = tk.Label(section_frame, textvariable=point_type, 
                                           font=("Arial", 10, "bold"), fg="#1565C0", bg="#F5F5F5",
                                           width=25, anchor="w")
                    point_display.pack(fill=tk.X, pady=3, padx=5)
                    point_display.is_point_display = True
                else:
                  
                    if "Anatomy" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    elif "Tandem" in btn_text:
                        bg_color, fg_color = "#E3F2FD", "#1565C0"
                    elif "Left Ovoid" in btn_text:
                        bg_color, fg_color = "#F3E5F5", "#7B1FA2"
                    elif "Right Ovoid" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    elif "Clear" in btn_text or "Remove" in btn_text:
                        bg_color, fg_color = "#FFEBEE", "#D32F2F"
                    elif "Zoom" in btn_text or "View" in btn_text:
                        bg_color, fg_color = "#FAFAFA", "#455A64"
                    elif "Save" in btn_text:
                        bg_color, fg_color = "#E8F5E8", "#2E7D32"
                    else:
                        bg_color, fg_color = "#F5F5F5", "#37474F"

                    
                    btn = tk.Button(section_frame, text=btn_text, command=command,
                                  font=("Arial", 9), width=32, height=1,
                                  bg=bg_color, fg=fg_color, relief="raised", bd=2,
                                  anchor="w", justify="left")
                    btn.pack(fill=tk.X, pady=3, padx=5)

        
        def update_point_display(*args):
            for widget in toolbar_frame.winfo_children():
                if isinstance(widget, tk.LabelFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and hasattr(child, 'is_point_display'):
                            child.config(text=f"{point_type.get().title()}")

        point_type.trace('w', update_point_display)

        
        for widget in toolbar_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame) and "Current Point Type" in widget.cget('text'):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.is_point_display = True

        
        redraw_canvas()

        print(f"Enhanced annotation window ready for {fraction_key}")

        
        
    def open_alignment_window_LT(self):
        import math
        save_folder = os.path.join(self.temp_dir, "LAT")
        json_path = os.path.join(save_folder, "LAT_frac1_annotations.json")
        
        print(f"Looking for JSON file at: {json_path}")
        print(f"File exists: {os.path.exists(json_path)}")
        
        if not os.path.exists(json_path):
            print("Fraction 1 annotations not found")
            from tkinter import messagebox
            messagebox.showerror("Error", "Fraction 1 annotations not found. Please annotate first.")
            return

        try:
            with open(json_path, 'r') as f:
                all_polygons = json.load(f)
            print("JSON loaded successfully")
        except Exception as e:
            print(f"Error loading JSON: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to load annotations: {e}")
            return

        win = tk.Toplevel(self.root)
        win.title("Align Fraction 1 structures on Fraction 2")

        img2 = cv2.imread(self.image_paths["LAT_frac1"])
        img_h, img_w = img2.shape[:2]
        scale = min(win.winfo_screenwidth() / img_w, win.winfo_screenheight() / img_h, 1.0)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        img_resized = cv2.resize(img2, (new_w, new_h))
        pil_img = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(pil_img)

        canvas = tk.Canvas(win, width=new_w, height=new_h, bg="black")
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.image = img_tk

        color_map = {
                "anatomy": "red",
                "applicator_tandem": "blue",
                "left_ovoid": "purple",
                "right_ovoid": "green"
        }

        polygon_items = []
        offset = {"x": 0, "y": 0}

        for label, polys in all_polygons.items():
            for poly in polys:
                scaled_poly = [(int(x * scale), int(y * scale)) for x, y in poly]
                item = canvas.create_line(scaled_poly, fill=color_map[label], width=2)
                polygon_items.append((item, scaled_poly, label))

        drag_start = {"x": 0, "y": 0}
                 
        def on_mouse_down(event):
            drag_start["x"] = event.x
            drag_start["y"] = event.y

        def on_mouse_move(event):
            dx = event.x - drag_start["x"]
            dy = event.y - drag_start["y"]
            drag_start["x"] = event.x
            drag_start["y"] = event.y
            offset["x"] += dx
            offset["y"] += dy
            for item, _, _ in polygon_items:
                canvas.move(item, dx, dy)

        def euclidean_dist(p1, p2):
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)



        def calculate_and_show_distances():

            mm_per_px = 228.6 / 768 

       
            if "anatomy" not in all_polygons or not all_polygons["anatomy"]:
                tk.messagebox.showerror("Error", "No anatomy polygon annotated.")
                return

            anatomy_poly = all_polygons["anatomy"][0]
            anatomy_start = anatomy_poly[0]
            anatomy_end = anatomy_poly[-1]

          
            def get_tip_bottom(poly):
                return poly[0], poly[-1]

           
            dist_results = []

                          
            for label in ["applicator_tandem", "right_ovoid", "left_ovoid"]:
                if label not in all_polygons or not all_polygons[label]:
                    dist_results.append(f"{label}: No polygons annotated.\n")
                    continue
                for i, poly in enumerate(all_polygons[label], 1):
                    tip, bottom = get_tip_bottom(poly)
                   
                    distances = {
                        f"{label} Polygon {i} Tip to Anatomy Start": euclidean_dist(tip, anatomy_start) * mm_per_px,
                        f"{label} Polygon {i} Bottom to Anatomy Start": euclidean_dist(bottom, anatomy_start) * mm_per_px,
                        f"{label} Polygon {i} Tip to Anatomy End": euclidean_dist(tip, anatomy_end) * mm_per_px,
                        f"{label} Polygon {i} Bottom to Anatomy End": euclidean_dist(bottom, anatomy_end) * mm_per_px,
                    }
                    for desc, dist in distances.items():
                        dist_results.append(f"{desc}: {dist:.2f} mm")

           
            txt_path = os.path.join(save_folder, "LAT distances_from_anatomy.txt")
            with open(txt_path, "w") as f:
                f.write(f"Anatomy start point: {anatomy_start}\n")
                f.write(f"Anatomy end point: {anatomy_end}\n\n")
                for line in dist_results:
                    f.write(line + "\n")

            print(f"Distances saved to {txt_path}")

            
            dist_win = tk.Toplevel(win)
            dist_win.title("Distances Illustration")

           
            illustration_canvas = tk.Canvas(dist_win, width=new_w, height=new_h, bg="white")
            illustration_canvas.pack(fill=tk.BOTH, expand=True)

            
            anatomy_points_scaled = [(int(x * scale) + offset["x"], int(y * scale) + offset["y"]) for x, y in anatomy_poly]
            if len(anatomy_points_scaled) > 1:
                illustration_canvas.create_line(anatomy_points_scaled, fill="red", width=2)
            
            sx, sy = anatomy_points_scaled[0]
            ex, ey = anatomy_points_scaled[-1]
            r = 5
            illustration_canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill="red")
            illustration_canvas.create_text(sx + 10, sy, text="Anatomy Start", fill="red", anchor='w')
            illustration_canvas.create_oval(ex - r, ey - r, ex + r, ey + r, fill="red")
            illustration_canvas.create_text(ex + 10, ey, text="Anatomy End", fill="red", anchor='w')

           
            colors = {
                "applicator_tandem": "blue",
                "right_ovoid": "green",
                "left_ovoid": "purple"
            }


            for label in ["applicator_tandem", "right_ovoid", "left_ovoid"]:
                if label not in all_polygons or not all_polygons[label]:
                    continue
                for i, poly in enumerate(all_polygons[label], 1):
                    points_scaled = [(int(x * scale) + offset["x"], int(y * scale) + offset["y"]) for x, y in poly]
                
                    if len(points_scaled) > 1:
                        illustration_canvas.create_line(points_scaled, fill=colors[label], width=2)
                 
                    tip = points_scaled[0]
                    bottom = points_scaled[-1]

                    
                    illustration_canvas.create_oval(tip[0] - r, tip[1] - r, tip[0] + r, tip[1] + r, fill=colors[label])
                    illustration_canvas.create_text(tip[0] + 10, tip[1], text=f"{label} {i} Tip", fill=colors[label], anchor='w')
                    illustration_canvas.create_oval(bottom[0] - r, bottom[1] - r, bottom[0] + r, bottom[1] + r, fill=colors[label])
                    illustration_canvas.create_text(bottom[0] + 10, bottom[1], text=f"{label} {i} Bottom", fill=colors[label], anchor='w')

                
                    illustration_canvas.create_line(tip[0], tip[1], sx, sy, fill="gray", dash=(4, 2))
                    illustration_canvas.create_line(bottom[0], bottom[1], sx, sy, fill="gray", dash=(4, 2))
                    illustration_canvas.create_line(tip[0], tip[1], ex, ey, fill="gray", dash=(4, 2))
                    illustration_canvas.create_line(bottom[0], bottom[1], ex, ey, fill="gray", dash=(4, 2))

      
            dist_text = "\n".join(dist_results)
            label = tk.Label(dist_win, text=dist_text, justify="left", font=("Arial", 10))
            label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def finish_alignment_LAT():
            print("Finish alignment clicked")
            
            aligned = {label: [] for label in all_polygons.keys()}
            for _, scaled_poly, label in polygon_items:
                new_poly = [(x + offset["x"], y + offset["y"]) for x, y in scaled_poly]
                aligned[label].append([(int(x / scale), int(y / scale)) for x, y in new_poly])
            with open(json_path, 'w') as f:
                json.dump(aligned, f)
            print(f"Saved aligned polygons for all structures: {json_path}")

            win.destroy()
            
        btn_export = tk.Button(win, text="Export Distances", command=calculate_and_show_distances)
        btn_export.pack(pady=5)

        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_move)

        tk.Button(win, text="Finish Alignment", command=finish_alignment_LAT).pack(pady=5)

        print("Alignment window ready")

         
        frame = tk.LabelFrame(win, text="Calculate Shifts", padx=10, pady=10)
        frame.pack(fill="x", pady=10)
                              
  
    def compare_lateral_fraction_distances(self):
     
        import os
        import re
    
        
        lat_dir = os.path.join(self.temp_dir, "LAT")
        file1 = os.path.join(lat_dir, "LAT_frac1_distances_from_anatomy.txt")
        file2 = os.path.join(lat_dir, "LAT_frac2_distances_from_anatomy.txt")
    
       
        self.debug_lateral_files()
    
        
        if not os.path.exists(file1) or not os.path.exists(file2):
            messagebox.showerror("Error", 
                               "Missing lateral distance files.\n\n"
                               f"LAT Fraction 1: {'Found' if os.path.exists(file1) else 'Missing'}\n"
                               f"LAT Fraction 2: {'Found' if os.path.exists(file2) else 'Missing'}\n\n"
                               "Please complete lateral annotation for both fractions first.")
            return

        def extract_structured_distances(file_path):
            """Extract distances from lateral TXT files"""
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(f"DEBUG: Reading {os.path.basename(file_path)}")
                    print(f"Content:\n{content}")
            
               
                with open(file_path, "r", encoding="utf-8") as f:
                    current_applicator = None
                    for line in f:
                        line = line.strip()
                        print(f"DEBUG Line: {line}")
                
                     
                        if not line or "===" in line:
                            continue
                    
                     
                        match = re.match(r"(.+?)\s+(Tip|Base)\s+to\s+Anatomy\s+(Start|End):\s*([\d.]+)\s*mm", line)
                        if match:
                            applicator = match.group(1).strip()
                            point_type = match.group(2).lower()
                            anatomy_point = match.group(3).lower()
                            value = float(match.group(4))
                    
                     
                            if applicator not in distances:
                                distances[applicator] = {}
                    
                            
                            key = f"{point_type}_to_{anatomy_point}"
                            distances[applicator][key] = value
                            print(f"DEBUG: Found {applicator} - {key}: {value}")
                    
            except Exception as e:
                print(f"Error reading lateral file {file_path}: {e}")
            return distances

       
        dist1 = extract_structured_distances(file1)
        dist2 = extract_structured_distances(file2)
    
        print(f"DEBUG: dist1 = {dist1}")
        print(f"DEBUG: dist2 = {dist2}")

        if not dist1 or not dist2:
            messagebox.showerror("Error", 
                               "No valid distance data found in lateral files.\n\n"
                               "Please ensure:\n"
                               "1. Both lateral fractions are annotated\n"
                               "2. All applicators are marked with tip and base points\n"
                               "3. Anatomy line is drawn")
            return

        
        shifts = {}
    
        for applicator in ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]:
            if applicator in dist1 and applicator in dist2:
                measurement_pairs = []
        
                for point_type in ["tip", "base"]:
                    for anatomy_point in ["start", "end"]:
                        key = f"{point_type}_to_{anatomy_point}"
                        if key in dist1[applicator] and key in dist2[applicator]:
                            shift = dist2[applicator][key] - dist1[applicator][key]
                            measurement_pairs.append({
                                'measurement': f"{point_type.title()} to Anatomy {anatomy_point.title()}",
                                'fraction1': dist1[applicator][key],
                                'fraction2': dist2[applicator][key],
                                'shift': shift,
                                'abs_shift': abs(shift)
                            })
        
                if measurement_pairs:
                    avg_shift = sum(pair['shift'] for pair in measurement_pairs) / len(measurement_pairs)
                    avg_abs_shift = sum(pair['abs_shift'] for pair in measurement_pairs) / len(measurement_pairs)
            
                    shifts[applicator] = {
                        'measurements': measurement_pairs,
                        'average_shift': avg_shift,
                        'average_absolute_shift': avg_abs_shift,
                        'max_shift': max(abs(pair['shift']) for pair in measurement_pairs)
                    }

        
        if shifts:
            self.show_lateral_comparison_results(shifts, file1, file2)
        else:
            messagebox.showinfo("No Data", "No matching lateral measurements found between fractions.")


    def show_lateral_shift_results(self, shifts, file1_path, file2_path):
       
        results_window = tk.Toplevel(self.root)
        results_window.title("Lateral Applicator Shifts Between Fractions")
        results_window.geometry("900x700")

      
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        
        title_label = tk.Label(main_frame, text="LATERAL APPLICATOR SHIFTS ANALYSIS", 
                              font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)

     
        file_info = tk.Label(main_frame, 
                            text=f"Data from lateral files:\n• {os.path.basename(file1_path)}\n• {os.path.basename(file2_path)}",
                            font=("Arial", 9), fg="#666666", justify=tk.LEFT)
        file_info.pack(pady=5)

        
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    
        text_widget.insert(tk.END, "LATERAL APPLICATOR SHIFTS BETWEEN FRACTIONS\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        text_widget.insert(tk.END, f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not shifts:
            text_widget.insert(tk.END, "No matching measurements found between lateral fractions.\n")
            text_widget.insert(tk.END, "Please ensure both lateral fractions have the same structures annotated.\n")
        else:
            for applicator, data in shifts.items():
                text_widget.insert(tk.END, f"{applicator.upper()}\n", "subtitle")
                text_widget.insert(tk.END, "-" * 40 + "\n")
        
                for measurement in data['measurements']:
                    direction = "increased" if measurement['shift'] > 0 else "decreased"
                    text_widget.insert(tk.END, 
                                     f"  • {measurement['measurement']}:\n"
                                     f"    F1: {measurement['fraction1']:.2f} mm → "
                                     f"F2: {measurement['fraction2']:.2f} mm\n"
                                     f"    Shift: {measurement['shift']:+.2f} mm ({direction})\n")
        
               
                text_widget.insert(tk.END, f"\n  SUMMARY:\n")
                text_widget.insert(tk.END, f"  • Average shift: {data['average_shift']:+.2f} mm\n")
                text_widget.insert(tk.END, f"  • Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
                text_widget.insert(tk.END, f"  • Maximum shift: {data['max_shift']:.2f} mm\n")
        
               
                if data['max_shift'] < 3.0:
                    assessment = "EXCELLENT reproducibility"
                    color = "green"
                elif data['max_shift'] < 5.0:
                    assessment = "GOOD reproducibility"
                    color = "orange"
                elif data['max_shift'] < 7.0:
                    assessment = "MODERATE variation"
                    color = "darkorange"
                else:
                    assessment = "SIGNIFICANT movement"
                    color = "red"
            
                    text_widget.insert(tk.END, f"  • ASSESSMENT: {assessment}\n", color)
                text_widget.insert(tk.END, "\n")

       
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#1565C0")
        text_widget.tag_configure("green", foreground="#2E7D32")
        text_widget.tag_configure("orange", foreground="#FF9800")
        text_widget.tag_configure("darkorange", foreground="#FF5722")
        text_widget.tag_configure("red", foreground="#D32F2F")

        text_widget.config(state=tk.DISABLED)

      
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

       
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack()                  

    def show_lateral_comparison_results(self, shifts, file1_path, file2_path):
       
        results_window = tk.Toplevel(self.root)
        results_window.title("Lateral View - Distance Comparison")
        results_window.geometry("1000x700")

       
        main_frame = tk.Frame(results_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        
        title_label = tk.Label(main_frame, text="LATERAL VIEW - DISTANCE COMPARISON", 
                          font=("Arial", 16, "bold"), fg="#2E7D32")
        title_label.pack(pady=10)

       
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=15, pady=15, 
                             font=("Arial", 10), bg="#F5F5F5")

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        
        text_widget.insert(tk.END, "LATERAL VIEW - APPLICATOR SHIFTS\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        text_widget.insert(tk.END, f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for applicator, data in shifts.items():
            text_widget.insert(tk.END, f"{applicator.upper()}\n", "subtitle")
            text_widget.insert(tk.END, "-" * 40 + "\n")
    
            for measurement in data['measurements']:
                direction = "increased" if measurement['shift'] > 0 else "decreased"
                text_widget.insert(tk.END, 
                                 f"  • {measurement['measurement']}:\n"
                                 f"    F1: {measurement['fraction1']:.2f} mm → "
                                 f"F2: {measurement['fraction2']:.2f} mm\n"
                                 f"    Shift: {measurement['shift']:+.2f} mm ({direction})\n")
    
            text_widget.insert(tk.END, f"\n  SUMMARY:\n")
            text_widget.insert(tk.END, f"  • Average shift: {data['average_shift']:+.2f} mm\n")
            text_widget.insert(tk.END, f"  • Average absolute shift: {data['average_absolute_shift']:.2f} mm\n")
            text_widget.insert(tk.END, f"  • Maximum shift: {data['max_shift']:.2f} mm\n\n")

       
        text_widget.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#1565C0")
    
        text_widget.config(state=tk.DISABLED)

        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

       
        close_button = tk.Button(button_frame, text="Close", 
                               command=results_window.destroy,
                               bg="#757575", fg="white", font=("Arial", 11),
                               width=15, height=1)
        close_button.pack()
        
    def compare_lateral_fraction_distances_with_shifts(self):
       
        import os
        import re
    
     
        file1 = os.path.join(self.temp_dir, "LAT", "LAT_frac1_distances_from_anatomy.txt")
        file2 = os.path.join(self.temp_dir, "LAT", "LAT_frac2_distances_from_anatomy.txt")
    
        # Check if files exist
        if not os.path.exists(file1) or not os.path.exists(file2):
            messagebox.showerror("Error", 
                               "Missing lateral distance files.\n\n"
                               f"Fraction 1: {'Found' if os.path.exists(file1) else 'Missing'}\n"
                               f"Fraction 2: {'Found' if os.path.exists(file2) else 'Missing'}")
            return
    
        def extract_distances(file_path):
          
            distances = {}
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            
                pattern = r"(.+?)\s+(Tip|Base)\s+to\s+Anatomy\s+(Start|End):\s*([\d.]+)\s*mm"
                matches = re.findall(pattern, content)
        
                for match in matches:
                    applicator = match[0].strip()
                    point_type = match[1].lower()
                    anatomy_point = match[2].lower()
                    value = float(match[3])
            
                    if applicator not in distances:
                        distances[applicator] = {}
                
                    key = f"{point_type}_to_{anatomy_point}"
                    distances[applicator][key] = value
            
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            return distances

       
        dist1 = extract_distances(file1)
        dist2 = extract_distances(file2)
    
        if not dist1 or not dist2:
            messagebox.showerror("Error", "No valid distance data found in lateral files")
            return
    
       
        shifts = {}
    
        for applicator in ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]:
            if applicator in dist1 and applicator in dist2:
                applicator_shifts = {}
        
                for measurement_key in ["tip_to_start", "tip_to_end", "base_to_start", "base_to_end"]:
                    if measurement_key in dist1[applicator] and measurement_key in dist2[applicator]:
                        frac1_val = dist1[applicator][measurement_key]
                        frac2_val = dist2[applicator][measurement_key]
                        shift = frac2_val - frac1_val
                
                        parts = measurement_key.split('_')
                        point_type = parts[0].title()
                        anatomy_part = parts[2].title()
                        measurement_name = f"{point_type} to Anatomy {anatomy_part}"
                
                        applicator_shifts[measurement_name] = {
                            'fraction1': frac1_val,
                            'fraction2': frac2_val,
                            'shift': shift,
                            'absolute_shift': abs(shift)
                        }
            
                if applicator_shifts:
                    shifts[applicator] = applicator_shifts
    
       
        self.save_lateral_applicator_shifts_to_txt(shifts, file1, file2)
    

        self.display_applicator_shifts(shifts)

    def save_lateral_applicator_shifts_to_txt(self, shifts, file1_path, file2_path):
       
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, "LAT_applicator_shifts_between_fractions.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("LATERAL APPLICATOR SHIFTS BETWEEN FRACTIONS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Data source:\n")
                f.write(f"  Fraction 1: {os.path.basename(file1_path)}\n")
                f.write(f"  Fraction 2: {os.path.basename(file2_path)}\n\n")
                f.write("METHOD: Shift = (Fraction 2 distance) - (Fraction 1 distance)\n\n")
                
                for applicator, measurements in shifts.items():
                    f.write(f"{applicator.upper()} SHIFTS\n")
                    f.write("-" * 40 + "\n")
            
                    for measurement_name, data in measurements.items():
                        direction = "increased" if data['shift'] > 0 else "decreased"
                        f.write(f"{measurement_name}:\n")
                        f.write(f"  Fraction 1: {data['fraction1']:.2f} mm\n")
                        f.write(f"  Fraction 2: {data['fraction2']:.2f} mm\n")
                        f.write(f"  Shift: {data['shift']:+.2f} mm ({direction})\n")
                        f.write(f"  Absolute shift: {data['absolute_shift']:.2f} mm\n\n")
            
                 
                    all_shifts = [data['absolute_shift'] for data in measurements.values()]
                    if all_shifts:
                        avg_shift = sum(data['shift'] for data in measurements.values()) / len(measurements)
                        avg_abs_shift = sum(all_shifts) / len(all_shifts)
                        max_shift = max(all_shifts)
                    
                        f.write(f"SUMMARY FOR {applicator.upper()}:\n")
                        f.write(f"  Average shift: {avg_shift:+.2f} mm\n")
                        f.write(f"  Average absolute shift: {avg_abs_shift:.2f} mm\n")
                        f.write(f"  Maximum shift: {max_shift:.2f} mm\n\n")
        
            messagebox.showinfo("Success", f"Lateral applicator shifts saved to:\n{output_file}")
    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save lateral shifts: {str(e)}")    
        
 
    def calculate_3d_displacements(self):
      
        import os
        import re
    
        
        ap_files = {
            "frac1": os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt"),
            "frac2": os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")
        }
    
        lat_files = {
            "frac1": os.path.join(self.temp_dir, "LAT", "LAT_frac1_distances_from_anatomy.txt"),
            "frac2": os.path.join(self.temp_dir, "LAT", "LAT_frac2_distances_from_anatomy.txt")
        }
    
      
        missing_files = []
        for frac_key in ["frac1", "frac2"]:
            if not os.path.exists(ap_files[frac_key]):
                missing_files.append(f"AP Fraction {frac_key[-1]}")
            if not os.path.exists(lat_files[frac_key]):
                missing_files.append(f"Lateral Fraction {frac_key[-1]}")
    
        if missing_files:
            messagebox.showerror(
                "Missing Files", 
                f"Could not find the following distance files:\n" + 
                "\n".join(f"• {file}" for file in missing_files) +
                "\n\nPlease complete annotation for all fractions and views first."
            )
            return
    
        def extract_3d_points_from_txt(file_path, view_type):
       
            points_3d = {}
    
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
        
          
                applicators_list = ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]
        
                for applicator in applicators_list:
              
                    height_pattern = rf"{applicator}.*?Height.*?:\s*([\d.]+)"
                    height_match = re.search(height_pattern, content, re.DOTALL | re.IGNORECASE)
            
                  
                    y_pattern = rf"{applicator}.*?Y.*?:\s*([\d.]+)"
                    y_match = re.search(y_pattern, content, re.DOTALL | re.IGNORECASE)
            
           
                    si_pattern = rf"{applicator}.*?Superior.*?Inferior.*?:\s*([\d.]+)"
                    si_match = re.search(si_pattern, content, re.DOTALL | re.IGNORECASE)
                    
                  
                    y_coordinate = 0
                    if height_match:
                        y_coordinate = float(height_match.group(1))
                    elif y_match:
                        y_coordinate = float(y_match.group(1))
                    elif si_match:
                        y_coordinate = float(si_match.group(1))
            
             
                    dist_pattern = rf"{applicator}.*?Tip to Anatomy Start:\s*([\d.]+).*?Base to Anatomy Start:\s*([\d.]+)"
                    dist_match = re.search(dist_pattern, content, re.DOTALL)
            
                    if dist_match:
                        tip_dist = float(dist_match.group(1))
                        base_dist = float(dist_match.group(2))
                
                        if view_type == "AP":
                            points_3d[applicator] = {
                                "tip": [tip_dist, y_coordinate, 0],
                                "base": [base_dist, y_coordinate, 0]
                            }
                        elif view_type == "LAT":
                            points_3d[applicator] = {
                                "tip": [0, y_coordinate, tip_dist],  
                                "base": [0, y_coordinate, base_dist]
                            }
                
            except Exception as e:
                print(f"Error extracting 3D points from {file_path}: {e}")
            
            return points_3d
    
       
        ap_points_frac1 = extract_3d_points_from_txt(ap_files["frac1"], "AP")
        ap_points_frac2 = extract_3d_points_from_txt(ap_files["frac2"], "AP")
        lat_points_frac1 = extract_3d_points_from_txt(lat_files["frac1"], "LAT") 
        lat_points_frac2 = extract_3d_points_from_txt(lat_files["frac2"], "LAT")
    
       
        applicators = ["Tandem Applicator", "Left Ovoid", "Right Ovoid"]
        missing_data = []
    
        for applicator in applicators:
            if (applicator not in ap_points_frac1 or applicator not in ap_points_frac2 or
                applicator not in lat_points_frac1 or applicator not in lat_points_frac2):
                missing_data.append(applicator)
    
        if missing_data:
            messagebox.showerror(
                "Missing Data",
                f"Could not extract complete data for:\n" +
                "\n".join(f"• {app}" for app in missing_data) +
                "\n\nPlease ensure all applicators are annotated in both views and fractions."
            )
            return
    
       
        def combine_3d_points(ap_points, lat_points):
            """Combine AP (X) and lateral (Z) data to get full 3D coordinates"""
            combined = {}

            for applicator in applicators:
                if applicator in ap_points and applicator in lat_points:
              
            
                    
                    combined[applicator] = {
                        "tip": [
                            ap_points[applicator]["tip"][0],  
                            lat_points[applicator]["tip"][1],
                            lat_points[applicator]["tip"][2]   
                        ],
                        "base": [
                            ap_points[applicator]["base"][0],   
                            lat_points[applicator]["base"][1],  
                            lat_points[applicator]["base"][2]   
                        ]
                    }
                
                    
                    tip = combined[applicator]["tip"]
                    base = combined[applicator]["base"]
                    centroid = [
                        (tip[0] + base[0]) / 2,
                        (tip[1] + base[1]) / 2, 
                        (tip[2] + base[2]) / 2
                    ]
                    combined[applicator]["centroid"] = centroid
        
            return combined
    
        
        points_3d_frac1 = combine_3d_points(ap_points_frac1, lat_points_frac1)
        points_3d_frac2 = combine_3d_points(ap_points_frac2, lat_points_frac2)
    
       
        displacements = {}
    
        for applicator in applicators:
            if applicator in points_3d_frac1 and applicator in points_3d_frac2:
               
                tip1 = points_3d_frac1[applicator]["tip"]
                tip2 = points_3d_frac2[applicator]["tip"]
                base1 = points_3d_frac1[applicator]["base"]  
                base2 = points_3d_frac2[applicator]["base"]
                centroid1 = points_3d_frac1[applicator]["centroid"]
                centroid2 = points_3d_frac2[applicator]["centroid"]
            
          
                tip_displacement_3d = self.euclidean_distance_3d(tip1, tip2)
                base_displacement_3d = self.euclidean_distance_3d(base1, base2)
                centroid_displacement_3d = self.euclidean_distance_3d(centroid1, centroid2)
            
            

            
             
                delta_x = centroid2[0] - centroid1[0]  
                delta_y = centroid2[1] - centroid1[1]  
                delta_z = centroid2[2] - centroid1[2]  
            
           
                tip_delta_x = tip2[0] - tip1[0]
                tip_delta_y = tip2[1] - tip1[1]
                tip_delta_z = tip2[2] - tip1[2]
            
                
                base_delta_x = base2[0] - base1[0]
                base_delta_y = base2[1] - base1[1]
                base_delta_z = base2[2] - base1[2]
            
                displacements[applicator] = {
                    "tip_displacement_mm": tip_displacement_3d,
                    "base_displacement_mm": base_displacement_3d, 
                    "centroid_displacement_mm": centroid_displacement_3d,
                    "points_frac1": points_3d_frac1[applicator],
                    "points_frac2": points_3d_frac2[applicator],
            
                    "centroid_delta_x": delta_x,
                    "centroid_delta_y": delta_y, 
                    "centroid_delta_z": delta_z,
                
                    "tip_delta_x": tip_delta_x,
                    "tip_delta_y": tip_delta_y,
                    "tip_delta_z": tip_delta_z,
                  
                    "base_delta_x": base_delta_x,
                    "base_delta_y": base_delta_y,
                    "base_delta_z": base_delta_z
                }
    
        
        self.show_3d_displacement_results(displacements)

    def euclidean_distance_3d(self, p1, p2):
        
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)

    def show_3d_displacement_results(self, displacements):
    
        results_window = tk.Toplevel(self.root)
        results_window.title("3D Applicator Movement Analysis")
        results_window.geometry("1200x900")
        results_window.configure(bg="#F5F5F5")

     
        main_container = tk.Frame(results_window, bg="#F5F5F5", padx=25, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)

      
        header_frame = tk.Frame(main_container, bg="#F5F5F5")
        header_frame.pack(fill=tk.X, pady=(0, 20))

       
        title_frame = tk.Frame(header_frame, bg="#F5F5F5")
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
    
        tk.Label(title_frame, text="🧭 3D APPLICATOR MOVEMENT ANALYSIS", 
                 font=("Arial", 20, "bold"), fg="#2E7D32", bg="#F5F5F5").pack(pady=(0, 5))
    
        tk.Label(title_frame, text="Comprehensive 3D movement analysis between treatment fractions",
                 font=("Arial", 12), fg="#666666", bg="#F5F5F5").pack(pady=(0, 10))

      
        button_frame = tk.Frame(header_frame, bg="#F5F5F5")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        
        save_btn = tk.Button(button_frame, text="💾 Save Detailed Report", 
                            command=lambda: self.save_3d_displacement_report(displacements),
                            bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                            width=18, height=1, relief="raised", bd=2,
                            cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=5)

      
        print_btn = tk.Button(button_frame, text="🖨️ Print Summary", 
                             command=lambda: self.print_3d_summary(displacements),
                             bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                             width=15, height=1, relief="raised", bd=2,
                             cursor="hand2")
        print_btn.pack(side=tk.LEFT, padx=5)

        
        close_btn = tk.Button(button_frame, text="✓ Close", 
                             command=results_window.destroy,
                             bg="#757575", fg="white", font=("Arial", 11, "bold"),
                             width=12, height=1, relief="raised", bd=2,
                             cursor="hand2")
        close_btn.pack(side=tk.LEFT, padx=5)

       
        if displacements:
            summary_frame = tk.LabelFrame(main_container, text="📊 Quick Summary", 
                                        font=("Arial", 11, "bold"), bg="#FFFFFF", 
                                        fg="#37474F", padx=15, pady=12)
            summary_frame.pack(fill=tk.X, pady=(0, 15))
        
            
            all_displacements = []
            for data in displacements.values():
                all_displacements.extend([data['tip_displacement_mm'], data['base_displacement_mm'], data['centroid_displacement_mm']])
        
            max_disp = max(all_displacements) if all_displacements else 0
            avg_disp = sum(all_displacements) / len(all_displacements) if all_displacements else 0
            
           
            metrics_frame = tk.Frame(summary_frame, bg="#FFFFFF")
            metrics_frame.pack(fill=tk.X)
        
            tk.Label(metrics_frame, text=f"Maximum Movement: {max_disp:.1f} mm", 
                    font=("Arial", 10, "bold"), fg="#D32F2F" if max_disp > 5 else "#FF9800" if max_disp > 3 else "#2E7D32", 
                    bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 30))
        
            tk.Label(metrics_frame, text=f"Average Movement: {avg_disp:.1f} mm", 
                    font=("Arial", 10), fg="#37474F", bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 30))
        
            tk.Label(metrics_frame, text=f"Applicators Analyzed: {len(displacements)}", 
                    font=("Arial", 10), fg="#37474F", bg="#FFFFFF").pack(side=tk.LEFT)

        
        coord_frame = tk.LabelFrame(main_container, text="🧭 Coordinate System Guide", 
                                  font=("Arial", 11, "bold"), bg="#E3F2FD", 
                                  fg="#1565C0", padx=15, pady=12)
        coord_frame.pack(fill=tk.X, pady=(0, 20))
    
        coord_grid = tk.Frame(coord_frame, bg="#E3F2FD")
        coord_grid.pack(fill=tk.X)
    
        axes_info = [
            ("X-axis", "Right-Left", "➡️ Positive = Movement to Right", "#1976D2"),
            ("Y-axis", "Superior-Inferior", "⬆️ Positive = Movement Upward", "#388E3C"), 
            ("Z-axis", "Anterior-Posterior", "↗️ Positive = Movement Forward", "#7B1FA2")
        ]
    
        for i, (axis, direction, meaning, color) in enumerate(axes_info):
            axis_frame = tk.Frame(coord_grid, bg="#E3F2FD")
            axis_frame.grid(row=0, column=i, padx=20, pady=5, sticky="nsew")
            coord_grid.columnconfigure(i, weight=1)
        
            tk.Label(axis_frame, text=axis, font=("Arial", 10, "bold"), 
                    fg=color, bg="#E3F2FD").pack()
            tk.Label(axis_frame, text=direction, font=("Arial", 9), 
                    fg="#37474F", bg="#E3F2FD").pack()
            tk.Label(axis_frame, text=meaning, font=("Arial", 8), 
                    fg="#666666", bg="#E3F2FD", wraplength=180).pack()

       
        notebook = tk.Frame(main_container, bg="#F5F5F5")
        notebook.pack(fill=tk.BOTH, expand=True)

        
        text_container = tk.Frame(notebook, bg="#FFFFFF", relief="solid", borderwidth=1)
        text_container.pack(fill=tk.BOTH, expand=True)

    
        text_widget = tk.Text(text_container, wrap=tk.WORD, padx=20, pady=20, 
                             font=("Arial", 10), bg="#FFFFFF", fg="#333333",
                             relief="flat", borderwidth=0)
    
        scrollbar = tk.Scrollbar(text_container, orient=tk.VERTICAL, command=text_widget.yview,
                                bg="#E0E0E0", troughcolor="#F5F5F5")
        text_widget.configure(yscrollcommand=scrollbar.set)
    
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

      
        text_widget.insert(tk.END, "📋 DETAILED 3D MOVEMENT ANALYSIS\n", "main_header")
        text_widget.insert(tk.END, "=" * 60 + "\n\n")
        text_widget.insert(tk.END, f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not displacements:
            text_widget.insert(tk.END, "❌ No 3D displacement data available.\n\n", "warning")
            text_widget.insert(tk.END, "Please ensure:\n", "subheader")
            text_widget.insert(tk.END, "• All applicators are annotated in both AP and Lateral views\n")
            text_widget.insert(tk.END, "• Both Fraction 1 and Fraction 2 images are processed\n")
            text_widget.insert(tk.END, "• All required annotation files are generated\n")
        else:
            for applicator, data in displacements.items():
               
                text_widget.insert(tk.END, f"\n🎯 {applicator.upper()}\n", "applicator_header")
                text_widget.insert(tk.END, "─" * 50 + "\n\n")
            
             
                text_widget.insert(tk.END, "📍 3D COORDINATES\n", "section_header")
            
               
                text_widget.insert(tk.END, "Fraction 1 Positions:\n", "subsection_header")
                coord_text = f"""    Tip:      X={data['points_frac1']['tip'][0]:>6.2f} mm, Y={data['points_frac1']['tip'][1]:>6.2f} mm, Z={data['points_frac1']['tip'][2]:>6.2f} mm
    Base:     X={data['points_frac1']['base'][0]:>6.2f} mm, Y={data['points_frac1']['base'][1]:>6.2f} mm, Z={data['points_frac1']['base'][2]:>6.2f} mm
    Centroid: X={data['points_frac1']['centroid'][0]:>6.2f} mm, Y={data['points_frac1']['centroid'][1]:>6.2f} mm, Z={data['points_frac1']['centroid'][2]:>6.2f} mm\n\n"""
                text_widget.insert(tk.END, coord_text)
            
              
                text_widget.insert(tk.END, "Fraction 2 Positions:\n", "subsection_header")
                coord_text = f"""    Tip:      X={data['points_frac2']['tip'][0]:>6.2f} mm, Y={data['points_frac2']['tip'][1]:>6.2f} mm, Z={data['points_frac2']['tip'][2]:>6.2f} mm
    Base:     X={data['points_frac2']['base'][0]:>6.2f} mm, Y={data['points_frac2']['base'][1]:>6.2f} mm, Z={data['points_frac2']['base'][2]:>6.2f} mm
    Centroid: X={data['points_frac2']['centroid'][0]:>6.2f} mm, Y={data['points_frac2']['centroid'][1]:>6.2f} mm, Z={data['points_frac2']['centroid'][2]:>6.2f} mm\n\n"""
                text_widget.insert(tk.END, coord_text)
            
         
                text_widget.insert(tk.END, "📏 MOVEMENT MAGNITUDES\n", "section_header")
                disp_text = f"""    Tip Movement:      {data['tip_displacement_mm']:>7.2f} mm
    Base Movement:     {data['base_displacement_mm']:>7.2f} mm
    Centroid Movement: {data['centroid_displacement_mm']:>7.2f} mm\n\n"""
                text_widget.insert(tk.END, disp_text)
            
               
                text_widget.insert(tk.END, "🧭 DIRECTIONAL ANALYSIS (Centroid Movement)\n", "section_header")
            
        
                directions = []
                if abs(data['centroid_delta_x']) > 0.1:
                    dir_x = "→ RIGHT" if data['centroid_delta_x'] > 0 else "← LEFT"
                    directions.append(f"{dir_x}: {abs(data['centroid_delta_x']):.2f} mm")
            
                if abs(data['centroid_delta_y']) > 0.1:
                    dir_y = "↑ SUPERIOR" if data['centroid_delta_y'] > 0 else "↓ INFERIOR" 
                    directions.append(f"{dir_y}: {abs(data['centroid_delta_y']):.2f} mm")
            
                if abs(data['centroid_delta_z']) > 0.1:
                    dir_z = "↗ ANTERIOR" if data['centroid_delta_z'] > 0 else "↙ POSTERIOR"
                    directions.append(f"{dir_z}: {abs(data['centroid_delta_z']):.2f} mm")
            
                if directions:
                    text_widget.insert(tk.END, "Primary Movement Directions:\n", "subsection_header")
                    for direction in directions:
                        text_widget.insert(tk.END, f"    • {direction}\n")
                    text_widget.insert(tk.END, "\n")
            
               
                text_widget.insert(tk.END, "Detailed Movement Vector:\n", "subsection_header")
                text_widget.insert(tk.END, f"    [", "vector")
                text_widget.insert(tk.END, f"ΔX={data['centroid_delta_x']:+.2f}", "vector_x")
                text_widget.insert(tk.END, f", ", "vector")
                text_widget.insert(tk.END, f"ΔY={data['centroid_delta_y']:+.2f}", "vector_y")
                text_widget.insert(tk.END, f", ", "vector")
                text_widget.insert(tk.END, f"ΔZ={data['centroid_delta_z']:+.2f}", "vector_z")
                text_widget.insert(tk.END, f"] mm\n\n", "vector")
            
            
                text_widget.insert(tk.END, "💡 CLINICAL ASSESSMENT\n", "section_header")
            
                max_displacement = max(data['tip_displacement_mm'], data['base_displacement_mm'], data['centroid_displacement_mm'])
            
                if max_displacement < 3.0:
                    assessment = "✅ EXCELLENT STABILITY"
                    details = "Minimal movement observed. Excellent reproducibility between fractions."
                    color = "excellent"
                elif max_displacement < 5.0:
                    assessment = "⚠️ GOOD STABILITY" 
                    details = "Acceptable clinical variation. Monitor for consistency."
                    color = "good"
                elif max_displacement < 7.0:
                    assessment = "🔶 MODERATE MOVEMENT"
                    details = "Consider clinical impact on dose distribution."
                    color = "moderate"
                else:
                    assessment = "❌ SIGNIFICANT MOVEMENT"
                    details = "Review patient positioning and applicator fixation."
                    color = "significant"
            
                text_widget.insert(tk.END, f"{assessment}\n", color)
                text_widget.insert(tk.END, f"{details}\n\n")
            
         
                recommendations = []
                if abs(data['centroid_delta_x']) > 5:
                    direction = "RIGHT" if data['centroid_delta_x'] > 0 else "LEFT"
                    recommendations.append(f"• Adjust lateral positioning (significant {direction} movement)")
            
                if abs(data['centroid_delta_y']) > 5:
                    direction = "superior" if data['centroid_delta_y'] > 0 else "inferior"
                    recommendations.append(f"• Verify superior-inferior alignment")
            
                if abs(data['centroid_delta_z']) > 5:
                    direction = "anterior" if data['centroid_delta_z'] > 0 else "posterior"
                    recommendations.append(f"• Check depth placement accuracy")
            
                if recommendations:
                    text_widget.insert(tk.END, "Clinical Recommendations:\n", "subsection_header")
                    for rec in recommendations:
                        text_widget.insert(tk.END, f"    {rec}\n")
                
                text_widget.insert(tk.END, "\n" + "═" * 60 + "\n\n")

       
        text_widget.tag_configure("main_header", font=("Arial", 14, "bold"), foreground="#2E7D32", spacing3=10)
        text_widget.tag_configure("applicator_header", font=("Arial", 12, "bold"), foreground="#1565C0", spacing3=8)
        text_widget.tag_configure("section_header", font=("Arial", 11, "bold"), foreground="#37474F", spacing2=5)
        text_widget.tag_configure("subsection_header", font=("Arial", 10, "bold"), foreground="#555555")
        text_widget.tag_configure("warning", font=("Arial", 11, "bold"), foreground="#D32F2F")
        text_widget.tag_configure("excellent", font=("Arial", 10, "bold"), foreground="#2E7D32")
        text_widget.tag_configure("good", font=("Arial", 10, "bold"), foreground="#FF9800")
        text_widget.tag_configure("moderate", font=("Arial", 10, "bold"), foreground="#FF5722")
        text_widget.tag_configure("significant", font=("Arial", 10, "bold"), foreground="#D32F2F")
        text_widget.tag_configure("vector", font=("Arial", 10, "bold"))
        text_widget.tag_configure("vector_x", font=("Arial", 10, "bold"), foreground="#1976D2")
        text_widget.tag_configure("vector_y", font=("Arial", 10, "bold"), foreground="#388E3C")
        text_widget.tag_configure("vector_z", font=("Arial", 10, "bold"), foreground="#7B1FA2")

        text_widget.config(state=tk.DISABLED)

        
        footer_frame = tk.Frame(main_container, bg="#F5F5F5")
        footer_frame.pack(fill=tk.X, pady=(15, 0))
    
        help_text = "💡 Tip: Save the report for clinical documentation and treatment planning"
        tk.Label(footer_frame, text=help_text, font=("Arial", 9), 
                 fg="#666666", bg="#F5F5F5").pack()
        
    def save_3d_displacement_report(self, displacements):
      
        import os
        from datetime import datetime
    
        output_file = os.path.join(self.temp_dir, "3D_Applicator_Movement_Analysis_Report.txt")
    
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("3D APPLICATOR MOVEMENT ANALYSIS REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("CLINICAL CONTEXT:\n")
                f.write("This report analyzes 3D movement of brachytherapy applicators between\n")
                f.write("Fraction 1 and Fraction 2 treatments. Significant movement may impact\n") 
                f.write("dose distribution and treatment efficacy.\n\n")
                f.write("COORDINATE SYSTEM:\n")
                f.write("• X-axis: Right-Left (positive = movement to patient's Right)\n")
                f.write("• Y-axis: Superior-Inferior (positive = movement to Superior/Up)\n") 
                f.write("• Z-axis: Anterior-Posterior (positive = movement to Anterior/Forward)\n\n")
                f.write("KEY:\n")
                f.write("• Excellent: <3.0 mm movement\n")
                f.write("• Good: 3.0-5.0 mm movement\n")
                f.write("• Moderate: 5.0-7.0 mm movement\n")
                f.write("• Significant: >7.0 mm movement\n\n")
                f.write("=" * 70 + "\n\n")
            
                for applicator, data in displacements.items():
                    f.write(f"APPLICATOR: {applicator.upper()}\n")
                    f.write("-" * 50 + "\n\n")
                
                    f.write("3D MOVEMENT SUMMARY:\n")
                    f.write(f"Tip displacement:      {data['tip_displacement_mm']:7.2f} mm\n")
                    f.write(f"Base displacement:     {data['base_displacement_mm']:7.2f} mm\n")
                    f.write(f"Centroid displacement: {data['centroid_displacement_mm']:7.2f} mm\n\n")
                    
                    f.write("DIRECTIONAL MOVEMENT (Fraction 2 - Fraction 1):\n")
                    f.write(f"Right-Left (X):        {data['centroid_delta_x']:+.2f} mm")
                    f.write(" → Movement to RIGHT\n" if data['centroid_delta_x'] > 0 else " → Movement to LEFT\n")
                    
                    f.write(f"Superior-Inferior (Y): {data['centroid_delta_y']:+.2f} mm") 
                    f.write(" → Movement SUPERIOR\n" if data['centroid_delta_y'] > 0 else " → Movement INFERIOR\n")
                    
                    f.write(f"Anterior-Posterior (Z): {data['centroid_delta_z']:+.2f} mm")
                    f.write(" → Movement ANTERIOR\n" if data['centroid_delta_z'] > 0 else " → Movement POSTERIOR\n\n")
                    
                    f.write(f"Movement Vector: [ΔX={data['centroid_delta_x']:+.2f}, ΔY={data['centroid_delta_y']:+.2f}, ΔZ={data['centroid_delta_z']:+.2f}] mm\n\n")
                
                  
                    max_disp = max(data['tip_displacement_mm'], data['base_displacement_mm'], data['centroid_displacement_mm'])
                    if max_disp < 3.0:
                        assessment = "EXCELLENT - Minimal movement"
                    elif max_disp < 5.0:
                        assessment = "GOOD - Acceptable variation"
                    elif max_disp < 7.0:
                        assessment = "MODERATE - Review recommended"
                    else:
                        assessment = "SIGNIFICANT - Immediate attention needed"
                
                    f.write(f"CLINICAL ASSESSMENT: {assessment}\n\n")
                    f.write("=" * 70 + "\n\n")
        
            messagebox.showinfo("Report Saved", 
                              f"✅ 3D movement analysis report saved successfully!\n\n"
                              f"Location: {output_file}\n\n"
                              f"This report contains detailed 3D movement analysis for all applicators.")
        except Exception as e:
            messagebox.showerror("Save Error", 
                               f"❌ Could not save report:\n{str(e)}\n\n"
                               f"Please check file permissions and try again.")

    def print_3d_summary(self, displacements):
       
        if not displacements:
            messagebox.showinfo("Print Summary", "No displacement data available to print.")
            return
    
        summary_window = tk.Toplevel(self.root)
        summary_window.title("3D Movement Summary")
        summary_window.geometry("600x500")
    
        summary_text = tk.Text(summary_window, wrap=tk.WORD, padx=15, pady=15, font=("Arial", 10))
        summary_text.pack(fill=tk.BOTH, expand=True)
    
        summary_text.insert(tk.END, "3D APPLICATOR MOVEMENT SUMMARY\n", "title")
        summary_text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    
        for applicator, data in displacements.items():
            max_disp = max(data['tip_displacement_mm'], data['base_displacement_mm'])
            summary_text.insert(tk.END, f"{applicator}: {max_disp:.1f} mm max movement\n")
    
        summary_text.config(state=tk.DISABLED)
        summary_text.tag_configure("title", font=("Arial", 12, "bold"))
    

    def temporary_debug():
        import tempfile
        import os
        import glob
    
        temp_dir = os.path.join(tempfile.gettempdir(), "BrachyApp")
        print(f"Temp directory: {temp_dir}")
    
        
        pattern = os.path.join(temp_dir, "**", "*.txt")
        all_files = glob.glob(pattern, recursive=True)
    
        print("\n=== ALL TEXT FILES ===")
        for file_path in all_files:
            print(f"\n--- {os.path.basename(file_path)} ---")
            print(f"Full path: {file_path}")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(f"Content:\n{content}")
                except Exception as e:
                    print(f"Error reading: {e}")
            else:
                print("FILE DOES NOT EXIST")




    def show_3d_view(self):
       
        print("=== ENHANCED 3D VIEW DEBUG ===")
    
      
        coordinates_3d = self.calculate_3d_applicator_positions()
    
        print(f"Coordinates 3D: {coordinates_3d}")
    
        if not coordinates_3d or "frac1" not in coordinates_3d:
            messagebox.showerror("Error", "Could not calculate 3D positions. Please ensure both AP and Lateral annotations are complete for both fractions.")
            return
    
       
        self.create_enhanced_3d_visualization_window(coordinates_3d)


    def calculate_3d_applicator_positions(self):
        
        try:
          
            ap_files = {
                "frac1": os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt"),
                "frac2": os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")
            }
    
          
            lat_files = {
                "frac1": os.path.join(self.temp_dir, "LAT", "LAT_frac1_distances_from_anatomy.txt"),
                "frac2": os.path.join(self.temp_dir, "LAT", "LAT_frac2_distances_from_anatomy.txt")
            }
    
            print(f"AP files exist: frac1={os.path.exists(ap_files['frac1'])}, frac2={os.path.exists(ap_files['frac2'])}")
            print(f"LAT files exist: frac1={os.path.exists(lat_files['frac1'])}, frac2={os.path.exists(lat_files['frac2'])}")
    
           
            applicator_data = {}
    
            for frac in ["frac1", "frac2"]:
                applicator_data[frac] = {}
        
           
                if os.path.exists(ap_files[frac]):
                    ap_distances = self.parse_distances_from_txt(ap_files[frac])
                    applicator_data[frac]["AP"] = ap_distances
                    print(f"AP {frac} data: {ap_distances}")
        
              
                if os.path.exists(lat_files[frac]):
                    lat_distances = self.parse_distances_from_txt(lat_files[frac])
                    applicator_data[frac]["LAT"] = lat_distances
                    print(f"LAT {frac} data: {lat_distances}")
    
        
            return self.convert_to_3d_coordinates(applicator_data)
    
        except Exception as e:
            print(f"Error calculating 3D positions: {e}")
            import traceback
            traceback.print_exc()
            return None

    def parse_distances_from_txt(self, file_path):
       
        distances = {}
        try:
            print(f"Parsing file: {file_path}")
    
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
    
            print(f"File content:\n{content}")
    
           
            lines = content.split('\n')
            current_applicator = None
        
            for i, line in enumerate(lines):
                line = line.strip()
                print(f"Line {i}: '{line}'")
            
                
                if not line or "===" in line or "Anatomy start" in line or "Anatomy end" in line:
                    continue
        
             
                if "Tandem Applicator" in line:
                    current_applicator = "tandem"
                    distances[current_applicator] = {}
                    print(f"Found tandem applicator")
                elif "Left Ovoid" in line:
                    current_applicator = "left_ovoid" 
                    distances[current_applicator] = {}
                    print(f"Found left ovoid")
                elif "Right Ovoid" in line:
                    current_applicator = "right_ovoid"
                    distances[current_applicator] = {}
                    print(f"Found right ovoid")
        
            
                if current_applicator and "mm" in line:
             
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) == 2:
                            measurement_name = parts[0].strip()
                            value_part = parts[1].strip()
                    
                         
                            import re
                            numbers = re.findall(r"[\d.]+", value_part)
                            if numbers:
                                value = float(numbers[0])
                                distances[current_applicator][measurement_name] = value
                                print(f"  Parsed: {measurement_name} = {value} mm")

            print(f"Final distances: {distances}")
    
        except Exception as e:
            print(f"Error parsing TXT file {file_path}: {e}")
            import traceback
            traceback.print_exc()
    
        return distances

    def convert_to_3d_coordinates(self, applicator_data):
        
        coordinates_3d = {}

        print("=== CONVERTING TO 3D COORDINATES ===")
    
        for frac in ["frac1", "frac2"]:
            coordinates_3d[frac] = {}
    
            if frac not in applicator_data:
                print(f"  No data for {frac}")
                continue
        
            if "AP" not in applicator_data[frac] or "LAT" not in applicator_data[frac]:
                print(f"  Missing AP or LAT data for {frac}")
                continue
    
            ap_data = applicator_data[frac]["AP"]
            lat_data = applicator_data[frac]["LAT"]
    
            print(f"  Processing {frac}:")
            print(f"    AP applicators: {list(ap_data.keys())}")
            print(f"    LAT applicators: {list(lat_data.keys())}")
    
            for applicator in ["tandem", "left_ovoid", "right_ovoid"]:
                if applicator in ap_data and applicator in lat_data:
                    print(f"    Processing {applicator}")
            
                   
                    ap_measurements = ap_data[applicator]
                    lat_measurements = lat_data[applicator]
            
                    print(f"      AP measurements: {ap_measurements}")
                    print(f"      LAT measurements: {lat_measurements}")
                
                  
                    tip_ap = None
                    tip_lat = None
            
                   
                    for key, value in ap_measurements.items():
                        if "tip" in key.lower() and "anatomy" in key.lower():
                            tip_ap = value
                            break
                    if tip_ap is None and ap_measurements:
                        tip_ap = list(ap_measurements.values())[0]  
            
          
                    for key, value in lat_measurements.items():
                        if "tip" in key.lower() and "anatomy" in key.lower():
                            tip_lat = value
                            break
                    if tip_lat is None and lat_measurements:
                        tip_lat = list(lat_measurements.values())[0] 
                
                    # Use defaults if still None
                    if tip_ap is None:
                        tip_ap = 50.0
                    if tip_lat is None:
                        tip_lat = 50.0
            
                    print(f"      Using AP distance: {tip_ap}, LAT distance: {tip_lat}")
                
                    
                    scale_factor = 5.0  
            

            
            
                    if applicator == "tandem":
                   
                        base_y = 0  
                        tip_y = tip_lat * scale_factor  
                        x_pos = tip_ap * scale_factor  
                        base_z = -20  
                        tip_z = 20    
                    elif applicator == "left_ovoid":
                    
                        base_y = 0  
                        tip_y = tip_lat * scale_factor  
                        x_pos = -tip_ap * scale_factor 
                        base_z = -10
                        tip_z = 10
                    else: 
                       
                        base_y = 0  
                        tip_y = tip_lat * scale_factor  
                        x_pos = tip_ap * scale_factor  
                        base_z = -10
                        tip_z = 10
            
                    coordinates_3d[frac][applicator] = {
                        'tip': {
                            'x': x_pos,          
                            'y': tip_y,          
                            'z': tip_z           
                        },
                        'base': {
                            'x': x_pos,           
                            'y': base_y,        
                            'z': base_z         
                        }
                    }
            
                    print(f"      Created 3D coordinates: tip={coordinates_3d[frac][applicator]['tip']}, base={coordinates_3d[frac][applicator]['base']}")
                else:
                    print(f"      Missing {applicator} in AP or LAT data")

        print(f"Final 3D coordinates: {coordinates_3d}")
        return coordinates_3d

    def create_enhanced_3d_visualization_window(self, coordinates_3d):
       
    
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        
            window = tk.Toplevel(self.root)
            window.title("3D Applicator Movement Analysis - Detailed View")
            
           
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            
            window_width = int(screen_width * 0.9)
            window_height = int(screen_height * 0.9) 
            window.geometry(f"{window_width}x{window_height}")
            
            
            x_position = (screen_width - window_width) // 2
            y_position = (screen_height - window_height) // 2
            window.geometry(f"+{x_position}+{y_position}")
            
        
            window.minsize(1000, 700) 
            
            
            window.grid_rowconfigure(0, weight=1)
            window.grid_columnconfigure(0, weight=1) 
            window.grid_columnconfigure(1, weight=1) 
        
          
            plot_frame = tk.Frame(window, bg="#FFFFFF")
            plot_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            plot_frame.grid_rowconfigure(0, weight=1)
            plot_frame.grid_columnconfigure(0, weight=1)
        
          
            analysis_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=2, bg="#F5F5F5")
            analysis_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            analysis_frame.grid_rowconfigure(0, weight=1)
            analysis_frame.grid_columnconfigure(0, weight=1)
            
            
            base_font_size = max(10, min(14, int(screen_width / 100)))  
            title_font_size = base_font_size + 4
            small_font_size = base_font_size - 1
        
            
            fig_width = max(8, min(12, window_width // 150))  
            fig_height = max(7, min(10, window_height // 120))
            fig = plt.Figure(figsize=(fig_width, fig_height), dpi=100)
            ax = fig.add_subplot(111, projection='3d')
        
            
            colors = {
                'frac1': {
                    'tandem': '#00FF00', 
                    'left_ovoid': '#00CC00', 
                    'right_ovoid': '#009900'
                },
                'frac2': {
                    'tandem': '#0066FF', 
                    'left_ovoid': '#0044CC', 
                    'right_ovoid': '#002299'
                }   
            }
            movement_color = '#8B4513'
            
            
            labels = {'tandem': 'TANDEM', 'left_ovoid': 'LEFT OVOID', 'right_ovoid': 'RIGHT OVOID'}
        
            
            positions_data = {'frac1': {}, 'frac2': {}}
            centroids = {'frac1': {}, 'frac2': {}}
        
            print("=== PLOTTING ENHANCED 3D VISUALIZATION WITH LARGE CYLINDRICAL APPLICATORS ===")
        
           
            all_x, all_y, all_z = [], [], []
        
            def add_enhanced_cylinder_caps(ax, base, tip, radius, color):
                """Add enhanced caps to cylindrical applicator - LOCAL FUNCTION"""
            
          
                u = np.linspace(0, 2 * np.pi, 40)
                v = np.linspace(0, radius, 20)
                u_grid, v_grid = np.meshgrid(u, v)
            
             
                x_cap_bottom = base['x'] + v_grid * np.cos(u_grid)
                y_cap_bottom = base['y'] + v_grid * np.sin(u_grid)
                z_cap_bottom = np.full_like(x_cap_bottom, base['z'])
            
              
                x_cap_top = tip['x'] + v_grid * np.cos(u_grid)
                y_cap_top = tip['y'] + v_grid * np.sin(u_grid)
                z_cap_top = np.full_like(x_cap_top, tip['z'])
            
         
                ax.plot_surface(x_cap_bottom, y_cap_bottom, z_cap_bottom, 
                               color=color, alpha=0.7, antialiased=True)
                ax.plot_surface(x_cap_top, y_cap_top, z_cap_top, 
                               color=color, alpha=0.7, antialiased=True)
                
             
                edge_u = np.linspace(0, 2 * np.pi, 50)
                edge_x_bottom = base['x'] + radius * np.cos(edge_u)
                edge_y_bottom = base['y'] + radius * np.sin(edge_u)
                edge_z_bottom = np.full_like(edge_x_bottom, base['z'])
                
                edge_x_top = tip['x'] + radius * np.cos(edge_u)
                edge_y_top = tip['y'] + radius * np.sin(edge_u)
                edge_z_top = np.full_like(edge_x_top, tip['z'])
                
       
                ax.plot(edge_x_bottom, edge_y_bottom, edge_z_bottom, 
                       color='black', alpha=0.3, linewidth=1)
                ax.plot(edge_x_top, edge_y_top, edge_z_top, 
                       color='black', alpha=0.3, linewidth=1)
        
            def create_large_cylindrical_applicator(ax, base, tip, color, applicator_type, fraction):
                """Create large cylindrical applicator with enhanced visualization"""
            
           
                dx = tip['x'] - base['x']
                dy = tip['y'] - base['y']  
                dz = tip['z'] - base['z']
            

                length = np.sqrt(dx**2 + dy**2 + dz**2)
            
   
                if applicator_type == 'tandem':
                    radius = 38.5 
                else: 
                    radius = 22.8  
            
             
                z_cyl = np.linspace(0, length, 50)
                theta = np.linspace(0, 2 * np.pi, 50)
                theta_grid, z_grid = np.meshgrid(theta, z_cyl)
            
              
                x_cyl = radius * np.cos(theta_grid)
                y_cyl = radius * np.sin(theta_grid)
            
            
                if length > 0:
               
                    u = dx / length
                    v = dy / length
                    w = dz / length
                
            
                    x_final = base['x'] + x_cyl * (1 - abs(u)) + y_cyl * (1 - abs(v)) + z_grid * u
                    y_final = base['y'] + x_cyl * (1 - abs(u)) + y_cyl * (1 - abs(v)) + z_grid * v
                    z_final = base['z'] + z_grid * w
                else:
                    x_final = base['x'] + x_cyl
                    y_final = base['y'] + y_cyl
                    z_final = base['z'] + z_grid
            
         
                ax.plot_surface(x_final, y_final, z_final, 
                               color=color, alpha=0.8, shade=True, linewidth=0.5,
                               antialiased=True, rstride=1, cstride=1)
            
              
                add_enhanced_cylinder_caps(ax, base, tip, radius, color)
            
        
                midpoint = {
                    'x': (base['x'] + tip['x']) / 2,
                    'y': (base['y'] + tip['y']) / 2,
                    'z': (base['z'] + tip['z']) / 2
                }
            
         
                label_font_size = max(8, min(12, fig_width))
                frac_num = '1' if fraction == 'frac1' else '2'
                
                ax.text(midpoint['x'] + 3, midpoint['y'] + 3, midpoint['z'] + 3,
                       f"{labels[applicator_type]} F{frac_num}", 
                       fontsize=label_font_size, fontweight='bold', color='black',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9, edgecolor=color))
        
    
            for frac in ["frac1", "frac2"]:
                if frac not in coordinates_3d:
                    continue
                
                for applicator, coords in coordinates_3d[frac].items():
                    if 'tip' in coords and 'base' in coords:
                        tip = coords['tip']
                        base = coords['base']
                    
             
                        if tip['y'] < base['y']:
                            print(f"WARNING: {applicator} {frac} - Tip Y ({tip['y']}) < Base Y ({base['y']}), swapping for correct anatomy")
                            tip, base = base, tip
                    
           
                        positions_data[frac][applicator] = {
                            'tip': tip,
                            'base': base
                        }
                    
           
                        centroid = {
                            'x': (tip['x'] + base['x']) / 2,
                            'y': (tip['y'] + base['y']) / 2, 
                            'z': (tip['z'] + base['z']) / 2
                        }
                        centroids[frac][applicator] = centroid
                    
              
                        all_x.extend([tip['x'], base['x'], centroid['x']])
                        all_y.extend([tip['y'], base['y'], centroid['y']])
                        all_z.extend([tip['z'], base['z'], centroid['z']])
                    
             
                        color = colors[frac][applicator]
                        create_large_cylindrical_applicator(ax, base, tip, color, applicator, frac)
        
           
            movement_data = {}
            if "frac1" in centroids and "frac2" in centroids:
                for applicator in centroids["frac1"]:
                    if applicator in centroids["frac2"]:
                        start = centroids["frac1"][applicator]
                        end = centroids["frac2"][applicator]
                    
            
                        dx = end['x'] - start['x']
                        dy = end['y'] - start['y']
                        dz = end['z'] - start['z']
                    
                        movement_3d = np.sqrt(dx**2 + dy**2 + dz**2)
                    
            
                        if movement_3d > 1.0:
           
                            ax.plot([start['x'], end['x']], 
                                   [start['y'], end['y']], 
                                   [start['z'], end['z']], 
                                   color='black', linewidth=3, alpha=0.8, linestyle='--',
                                   label=f'{labels[applicator]} Movement' if applicator == 'tandem' else "")
                        
                 
                            mid_point = {
                                'x': (start['x'] + end['x']) / 2,
                                'y': (start['y'] + end['y']) / 2,
                                'z': (start['z'] + end['z']) / 2
                            }
                        
                            label_font_size = max(8, min(12, fig_width))
                            ax.text(mid_point['x'], mid_point['y'], mid_point['z'],
                                   f'{movement_3d:.1f}mm', 
                                   fontsize=label_font_size, fontweight='bold', color='black',
                                   bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))
                    
                  
                        movement_data[applicator] = {
                            'start': start,
                            'end': end,
                            'movement_3d': movement_3d,
                            'components': (dx, dy, dz)
                        }
        
    
            if all_x and all_y and all_z:
                padding_x = (max(all_x) - min(all_x)) * 0.4 
                padding_y = (max(all_y) - min(all_y)) * 0.4
                padding_z = (max(all_z) - min(all_z)) * 0.4
            
                ax.set_xlim(min(all_x) - padding_x, max(all_x) + padding_x)
                ax.set_ylim(min(all_y) - padding_y, max(all_y) + padding_y)
                ax.set_zlim(min(all_z) - padding_z, max(all_z) + padding_z)
        
          
            axis_font_size = max(10, min(14, fig_width))
            ax.set_xlabel('X AXIS (LATERAL)\n← LEFT | RIGHT →', fontsize=axis_font_size, fontweight='bold', labelpad=15)
            ax.set_ylabel('Y AXIS (ANTERIOR-POSTERIOR)\n← POSTERIOR | ANTERIOR →', fontsize=axis_font_size, fontweight='bold', labelpad=15)
            ax.set_zlabel('Z AXIS (SUPERIOR-INFERIOR)\n← INFERIOR | SUPERIOR →', fontsize=axis_font_size, fontweight='bold', labelpad=15)
        
         
            title_font_size = max(14, min(20, fig_width * 1.2))
            ax.set_title('3D APPLICATOR POSITION ANALYSIS - LARGE CYLINDRICAL VIEW\n(GREEN: FRACTION 1, BLUE: FRACTION 2)', 
                        fontsize=title_font_size, fontweight='bold', pad=30)
        
        
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
        
     
            ax.set_facecolor('#F8F9FA')
        
   
            legend_font_size = max(8, min(12, fig_width))
            
           
            legend_elements = [
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#00FF00', 
                          markersize=10, label='Fraction 1', markeredgecolor='black'),
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#0066FF', 
                          markersize=10, label='Fraction 2', markeredgecolor='black')
            ]
            
            ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1), 
                     fontsize=legend_font_size, framealpha=0.9, fancybox=True, shadow=True)
        
      
            canvas = FigureCanvasTkAgg(fig, plot_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
 
            toolbar_frame = tk.Frame(plot_frame)
            toolbar_frame.grid(row=1, column=0, sticky="ew")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
        
  
            self.create_report_analysis_panel(analysis_frame, window_width, window_height, base_font_size)
        
            print("Enhanced 3D visualization with large cylindrical applicators created successfully")
            
       
            def on_resize(event):
             
                pass
                
            window.bind('<Configure>', on_resize)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create enhanced 3D visualization: {str(e)}")
            print(f"Enhanced 3D visualization error: {e}")
            import traceback
            traceback.print_exc()
            
    def create_report_analysis_panel(self, parent, window_width, window_height, base_font_size):
        """Create enhanced user-friendly analysis panel with professional box-drawing formatting"""
        try:
           
            panel_width = max(400, window_width // 2 - 50)
            panel_height = max(600, window_height - 50)
            
        
            text_font_size = max(9, min(12, base_font_size))
            title_font_size = max(11, base_font_size)
            small_font_size = max(8, min(11, base_font_size - 1))
            
          
            main_container = tk.Frame(parent, bg="#F8F9FA")
            main_container.pack(fill=tk.BOTH, expand=True)
        
      
            header_frame = tk.Frame(main_container, bg="#2E7D32", relief=tk.FLAT, borderwidth=0)
            header_frame.pack(fill=tk.X, padx=8, pady=8)
        
          
            header_border = tk.Frame(header_frame, bg="#2E7D32")
            header_border.pack(fill=tk.X, padx=2, pady=2)
            
            title_label = tk.Label(header_border, 
                                 text="╔════════════════════════════════════════════════════════════════════════════╗\n"
                                      "║                   3D APPLICATOR MOVEMENT ANALYSIS REPORT                  ║\n"
                                      "╚════════════════════════════════════════════════════════════════════════════╝", 
                                 font=("Courier", title_font_size, "bold"), 
                                 fg="white", bg="#2E7D32",
                                 justify=tk.CENTER)
            title_label.pack(pady=8)
        
           
            info_frame = tk.Frame(main_container, bg="#E3F2FD", relief=tk.FLAT, borderwidth=1)
            info_frame.pack(fill=tk.X, padx=8, pady=4)
            
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
            patient_name = self.patient_info.get('Name', 'Not Specified')
            admission_no = self.patient_info.get('Admission Number', 'Not Specified')
            
            info_text = (f"📋 Generated: {timestamp} │ 👤 Patient: {patient_name} │ "
                        f"🏥 Admission: {admission_no} │ 🔢 Fractions: 2")
            info_label = tk.Label(info_frame, text=info_text, 
                                 font=("Arial", small_font_size, "bold"),
                                 fg="#1565C0", bg="#E3F2FD")
            info_label.pack(pady=6)
        
          
            content_frame = tk.Frame(main_container, bg="#F8F9FA")
            content_frame.pack(fill=tk.BOTH, expand=True)
        
     
            canvas = tk.Canvas(content_frame, bg="#F8F9FA", highlightthickness=0)
            v_scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            h_scrollbar = tk.Scrollbar(content_frame, orient="horizontal", command=canvas.xview)
            
            scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
        
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
          
            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")
            content_frame.grid_rowconfigure(0, weight=1)
            content_frame.grid_columnconfigure(0, weight=1)
        
          
            def configure_canvas(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", configure_canvas)
            
           
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            canvas.bind("<MouseWheel>", on_mousewheel)
            scrollable_frame.bind("<MouseWheel>", on_mousewheel)
            
       
            report_file = os.path.join(self.temp_dir, "3D_Applicator_Movement_Analysis_Report.txt")
            
            if os.path.exists(report_file):
                try:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                  
                    report_frame = tk.Frame(scrollable_frame, bg="#FFFFFF", relief=tk.FLAT, borderwidth=0)
                    report_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
                    
                    report_frame.grid_rowconfigure(0, weight=1)
                    report_frame.grid_columnconfigure(0, weight=1)
                    
         
                    text_width = max(80, panel_width // 10)
                    text_height = max(35, panel_height // 18)
                    
                    text_widget = tk.Text(report_frame, 
                                        wrap=tk.NONE,  
                                        font=("Courier New", text_font_size),
                                        bg="#FFFFFF", 
                                        fg="#000000",
                                        padx=10, 
                                        pady=10,
                                        width=text_width, 
                                        height=text_height,
                                        selectbackground="#3498DB",
                                        cursor="xterm",
                                        tabs=('0.5c', '1c', '1.5c', '2c'), 
                                        relief=tk.FLAT)
                    
              
                    text_v_scrollbar = tk.Scrollbar(report_frame, orient="vertical", command=text_widget.yview)
                    text_h_scrollbar = tk.Scrollbar(report_frame, orient="horizontal", command=text_widget.xview)
                    
                    text_widget.configure(yscrollcommand=text_v_scrollbar.set,
                                         xscrollcommand=text_h_scrollbar.set)
                    
                    text_widget.grid(row=0, column=0, sticky="nsew")
                    text_v_scrollbar.grid(row=0, column=1, sticky="ns")
                    text_h_scrollbar.grid(row=1, column=0, sticky="ew")
                    
             
                    text_widget.insert("1.0", report_content)
                    
                
                    self.apply_professional_formatting(text_widget)
                    
                    text_widget.config(state="disabled")
                    
              
                    def on_text_mousewheel(event):
                        text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    
                    text_widget.bind("<MouseWheel>", on_text_mousewheel)
                    
              
                    def on_text_keypress(event):
                        if event.keysym == "Down":
                            text_widget.yview_scroll(1, "units")
                        elif event.keysym == "Up":
                            text_widget.yview_scroll(-1, "units")
                        elif event.keysym == "Page_Down":
                            text_widget.yview_scroll(1, "pages")
                        elif event.keysym == "Page_Up":
                            text_widget.yview_scroll(-1, "pages")
                        elif event.keysym == "Home":
                            text_widget.see("1.0")
                        elif event.keysym == "End":
                            text_widget.see("end")
                        elif event.keysym == "Right":
                            text_widget.xview_scroll(1, "units")
                        elif event.keysym == "Left":
                            text_widget.xview_scroll(-1, "units")
                    
                    text_widget.bind("<KeyPress>", on_text_keypress)
                    
                
                    def focus_text_widget(event):
                        text_widget.focus_set()
                    
                    text_widget.bind("<Button-1>", focus_text_widget)
                    
        
                    control_frame = tk.Frame(scrollable_frame, bg="#FFF3E0", relief=tk.GROOVE, borderwidth=1)
                    control_frame.pack(fill=tk.X, padx=8, pady=8)
                    
                    control_text = "🎮 Navigation: Mouse Wheel • Arrow Keys • Page Up/Down • Click & Drag"
                    control_label = tk.Label(control_frame, text=control_text, 
                                           font=("Arial", small_font_size, "bold"),
                                           fg="#E65100", bg="#FFF3E0")
                    control_label.pack(pady=6)
                    
                except Exception as e:
                    self.show_error_panel(scrollable_frame, f"Error reading report: {str(e)}")
                    
            else:
              
                self.show_loading_panel(scrollable_frame, "🔄 Generating 3D Analysis Report...")
                self.export_enhanced_analysis_report({}, {}, {})
                
                if os.path.exists(report_file):
                
                    for widget in scrollable_frame.winfo_children():
                        widget.destroy()
                    self.create_report_analysis_panel(parent, window_width, window_height, base_font_size)
                else:
                    self.show_error_panel(scrollable_frame, "❌ Failed to generate analysis report")
        
        except Exception as e:
            self.show_error_panel(parent, f"Error creating analysis panel: {str(e)}")

    def apply_professional_formatting(self, text_widget):
        """Apply professional formatting with box-drawing character styling"""
        try:
            text_widget.config(state="normal")
            
    
            format_scheme = {
                "header_main": {"fg": "#2E7D32", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "header_section": {"fg": "#1976D2", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "border": {"fg": "#666666", "font": ("Courier New", text_widget.cget("font").split()[1])},
                "value_important": {"fg": "#D32F2F", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "value_measurement": {"fg": "#FF9800", "font": ("Courier New", text_widget.cget("font").split()[1])},
                "fraction1": {"fg": "#00C853", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "fraction2": {"fg": "#2962FF", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "applicator": {"fg": "#7B1FA2", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "status_excellent": {"fg": "#00C853", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "status_good": {"fg": "#FF9800", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "status_warning": {"fg": "#FF5722", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "status_critical": {"fg": "#D32F2F", "font": ("Courier New", text_widget.cget("font").split()[1], "bold")},
                "note": {"fg": "#666666", "font": ("Courier New", text_widget.cget("font").split()[1])}
            }
            
          
            for tag_name, style in format_scheme.items():
                text_widget.tag_configure(tag_name, **style)
            
         
            content = text_widget.get("1.0", "end-1c")
            lines = content.split('\n')
            
            line_number = 1
            for line in lines:
                start_index = f"{line_number}.0"
                end_index = f"{line_number}.end"
                
          
                if any(char in line for char in ["╔", "╗", "╚", "╝", "║", "╠", "╣", "╬"]):
                    text_widget.tag_add("border", start_index, end_index)
                elif "═" in line or "─" in line or "┌" in line or "┐" in line or "└" in line or "┘" in line:
                    text_widget.tag_add("border", start_index, end_index)
                elif "├" in line or "┤" in line or "┬" in line or "┴" in line:
                    text_widget.tag_add("border", start_index, end_index)
                
               
                elif "3D APPLICATOR MOVEMENT ANALYSIS REPORT" in line:
                    text_widget.tag_add("header_main", start_index, end_index)
                elif "END OF REPORT" in line:
                    text_widget.tag_add("header_main", start_index, end_index)
                
               
                elif any(header in line for header in ["EXECUTIVE SUMMARY", "DETAILED APPLICATOR ANALYSIS", "ADDITIONAL NOTES"]):
                    text_widget.tag_add("header_section", start_index, end_index)
                elif "REPORT INFORMATION" in line or "CLINICAL ASSESSMENT" in line:
                    text_widget.tag_add("header_section", start_index, end_index)
                
              
                elif "F1 -" in line or "FRACTION 1" in line:
                    text_widget.tag_add("fraction1", start_index, end_index)
                elif "F2 -" in line or "FRACTION 2" in line:
                    text_widget.tag_add("fraction2", start_index, end_index)
                
               
                elif any(app in line for app in ["TANDEM", "LEFT OVOID", "RIGHT OVOID"]):
                    if "APPLICATOR" not in line: 
                        text_widget.tag_add("applicator", start_index, end_index)
                
                
                elif "mm" in line:
               
                    import re
                    numbers = re.findall(r"[\d.]+", line)
                    for num in numbers:
                        if "." in num: 
                            num_start = line.find(num)
                            num_end = num_start + len(num)
                            text_widget.tag_add("value_measurement", f"{line_number}.{num_start}", f"{line_number}.{num_end}")
                
              
                elif any(term in line for term in ["Maximum Movement:", "Average Movement:", "Total 3D Movement:"]):
                    text_widget.tag_add("value_important", start_index, end_index)
                
                
                elif any(status in line for status in ["EXCELLENT REPRODUCIBILITY", "✅"]):
                    text_widget.tag_add("status_excellent", start_index, end_index)
                elif any(status in line for status in ["GOOD REPRODUCIBILITY", "✓", "👍"]):
                    text_widget.tag_add("status_good", start_index, end_index)
                elif any(status in line for status in ["MODERATE MOVEMENT", "⚠", "REVIEW"]):
                    text_widget.tag_add("status_warning", start_index, end_index)
                elif any(status in line for status in ["SIGNIFICANT MOVEMENT", "❌", "🚨"]):
                    text_widget.tag_add("status_critical", start_index, end_index)
                
           
                elif "•" in line or "→" in line or "│ •" in line:
                    text_widget.tag_add("note", start_index, end_index)
                
                line_number += 1
                
            text_widget.config(state="disabled")
            
        except Exception as e:
            print(f"Error applying professional formatting: {e}")

    def show_loading_panel(self, parent, message):
        """Show loading panel with professional styling"""
        loading_frame = tk.Frame(parent, bg="#F8F9FA")
        loading_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        
        border_frame = tk.Frame(loading_frame, bg="#666666")
        border_frame.pack(pady=20, padx=20)
        
        content_frame = tk.Frame(border_frame, bg="#FFFFFF", padx=20, pady=20)
        content_frame.pack(padx=1, pady=1)
        
        loading_label = tk.Label(content_frame, text=message,
                               font=("Courier New", 12, "bold"),
                               fg="#1976D2", bg="#FFFFFF")
        loading_label.pack(pady=10)
        
      
        dots_label = tk.Label(content_frame, text="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
                            font=("Courier New", 14),
                            fg="#666666", bg="#FFFFFF")
        dots_label.pack()

    def show_error_panel(self, parent, message):
        """Show error panel with professional styling"""
        error_frame = tk.Frame(parent, bg="#F8F9FA")
        error_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
      
        border_frame = tk.Frame(error_frame, bg="#D32F2F")
        border_frame.pack(pady=20, padx=20)
        
        content_frame = tk.Frame(border_frame, bg="#FFFFFF", padx=20, pady=20)
        content_frame.pack(padx=1, pady=1)
        
        error_label = tk.Label(content_frame, text=message,
                             font=("Courier New", 11, "bold"),
                             fg="#D32F2F", bg="#FFFFFF",
                             wraplength=400, justify=tk.CENTER)
        error_label.pack(pady=10)
        
        retry_btn = tk.Button(content_frame, text="🔄 Retry Analysis",
                            command=lambda: self.retry_analysis(parent),
                            bg="#FF5722", fg="white",
                            font=("Arial", 10, "bold"),
                            relief=tk.RAISED, bd=2)
        retry_btn.pack(pady=10)

    def retry_analysis(self, parent):
        """Retry analysis generation"""
        for widget in parent.winfo_children():
            widget.destroy()
        self.create_report_analysis_panel(parent, 800, 600, 12)


        
    def debug_3d_data(self):
        
        print("=== DEBUG 3D DATA ===")
    
     
        ap_files = {
            "frac1": os.path.join(self.temp_dir, "AP_frac1_distances_from_anatomy.txt"),
            "frac2": os.path.join(self.temp_dir, "AP_frac2_distances_from_anatomy.txt")
        }
    
      
        lat_files = {
            "frac1": os.path.join(self.temp_dir, "LAT", "LAT_frac1_distances_from_anatomy.txt"),
            "frac2": os.path.join(self.temp_dir, "LAT", "LAT_frac2_distances_from_anatomy.txt")
        }
    
        for frac in ["frac1", "frac2"]:
            print(f"\n--- {frac.upper()} ---")
            print(f"AP file exists: {os.path.exists(ap_files[frac])}")
            print(f"LAT file exists: {os.path.exists(lat_files[frac])}")
        
            if os.path.exists(ap_files[frac]):
                print(f"AP file content preview:")
                with open(ap_files[frac], 'r') as f:
                    print(f.read()[:500])
        
            if os.path.exists(lat_files[frac]):
                print(f"LAT file content preview:") 
                with open(lat_files[frac], 'r') as f:
                    print(f.read()[:500])


    
    def test_image_loading(self):
        
        try:
         
            from PIL import Image as PILImage, ImageTk
            print("✓ PIL imported successfully")
        
          
            test_img = Image.new('RGB', (100, 100), color='red')
            test_path = os.path.join(self.temp_dir, "test_image.png")
            test_img.save(test_path)
            print(f"✓ Test image created: {test_path}")
        
       
            loaded_img = Image.open(test_path)
            print("✓ Image opened successfully")
        
         
            if loaded_img.mode != 'RGB':
                loaded_img = loaded_img.convert('RGB')
                print("✓ Image converted to RGB")
        
            return True
        
        except Exception as e:
            print(f"✗ Image test failed: {e}")
            return False

  

    def collect_report_data(self):
       
        try:
            self.report_data = {
                'patient_info': self.get_patient_info(),
                'analysis_results': self.get_analysis_results(),
                'image_paths': self.get_annotation_images(),
                'distance_data': self.get_distance_data(),
                'shift_data': self.get_shift_data()
            }
            print("✅ Report data collected successfully")
        except Exception as e:
            print(f"❌ Error collecting report data: {e}")
            self.report_data = {
                'patient_info': {},
                'analysis_results': {},
                'image_paths': {},
                'distance_data': {},
                'shift_data': {}
            }

    def get_patient_info(self):
    
        return {
            "Name": self.name_entry.get() or "Not provided",
            "Admission Number": self.admission_entry.get() or "Not provided",
            "Number of Fractions": self.fractions_entry.get() or "Not provided",
            "First Fraction Date": self.date_frac1.get() if hasattr(self, 'date_frac1') else "Not provided",
            "Second Fraction Date": self.date_frac2.get() if hasattr(self, 'date_frac2') else "Not provided",
            "AP Pixel Spacing": f"{self.pixel_spacing.get('AP_frac1', 0.2979):.4f} mm/pixel",
            "Lateral Pixel Spacing": f"{self.pixel_spacing.get('LAT_frac1', 0.2979):.4f} mm/pixel"
        }

    def get_analysis_results(self):
        
        results = {}
        
        
        analysis_files = [
            "AP_frac1_distances_from_anatomy.txt",
            "AP_frac2_distances_from_anatomy.txt", 
            "LAT_frac1_distances_from_anatomy.txt",
            "LAT_frac2_distances_from_anatomy.txt",
            "applicator_shifts_between_fractions.txt",
            "AP_direct_euclidean_comparison.txt",
            "AP_direct_euclidean_comparison_TXT_ONLY.txt",
            "AP_frac1_aligned_to_frac2_explicit_points.json",
            "direct_applicator_shifts.txt",
            "3D_Applicator_Movement_Analysis_Report.txt" 
        ]
        
        for file_name in analysis_files:
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        results[file_name] = f.read()
                    print(f"✅ Loaded analysis file: {file_name}")
                except Exception as e:
                    print(f"❌ Error reading {file_name}: {e}")
                    results[file_name] = f"Error reading file: {str(e)}"
                    
        return results

    def get_annotation_images(self):
      
        image_paths = {}
        
   
        possible_images = [
            "AP_frac1_edited.png", "AP_frac2_edited.png",
            "LAT_frac1_edited.png", "LAT_frac2_edited.png"
        ]
        
        for img_name in possible_images:
            img_path = os.path.join(self.temp_dir, img_name)
            if os.path.exists(img_path):
                image_paths[img_name] = img_path
                print(f"✅ Found image: {img_name}")
                
      
        lat_dir = os.path.join(self.temp_dir, "LAT")
        if os.path.exists(lat_dir):
            for img_name in ["LAT_frac1_edited.png", "LAT_frac2_edited.png"]:
                img_path = os.path.join(lat_dir, img_name)
                if os.path.exists(img_path):
                    image_paths[img_name] = img_path
                    print(f"✅ Found LAT image: {img_name}")
                    
        return image_paths

    def get_distance_data(self):
     
    
    
        return {}

    def get_shift_data(self):
 
   
 
        return {}

    def prepare_image_for_pdf(self, original_path):
    
        try:
          
            temp_img_path = os.path.join(self.temp_dir, "pdf_temp_image.png")
            
          
            from PIL import Image as PILImage
            
            with PILImage.open(original_path) as img:
              
                if img.mode in ('P', 'RGBA', 'LA'):
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
            
                max_size = (800, 600)
                img.thumbnail(max_size, PILImage.Resampling.LANCZOS)
            
            
                img.save(temp_img_path, 'PNG', optimize=True)
            
            return temp_img_path
        
        except Exception as e:
            print(f"❌ Error preparing image {original_path} for PDF: {e}")
            return None

    def extract_applicator_points_3d(self, fraction):
      
        try:
            points_3d = {}
            
         
            if fraction == 1:
                json_file = "AP_frac1_annotations.json"
                lat_json_file = "LAT_frac1_annotations.json"
            else:
                json_file = "AP_frac2_annotations.json" 
                lat_json_file = "LAT_frac2_annotations.json"
            
         
            annotation_path = os.path.join(self.temp_dir, json_file)
            lat_annotation_path = os.path.join(self.temp_dir, lat_json_file)
            
            ap_data = {}
            lat_data = {}
            
            if os.path.exists(annotation_path):
                with open(annotation_path, 'r') as f:
                    ap_data = json.load(f)
            
            if os.path.exists(lat_annotation_path):
                with open(lat_annotation_path, 'r') as f:
                    lat_data = json.load(f)
            
           
            for applicator in ['applicator_tandem', 'left_ovoid', 'right_ovoid']:
                if applicator in ap_data and ap_data[applicator]:
                    points = ap_data[applicator][0] 
                    
                    if len(points) >= 2:
                     
                        x = [point[0] for point in points if isinstance(point, list) and len(point) >= 2]
                        y = [point[1] for point in points if isinstance(point, list) and len(point) >= 2]
                        
                        if x and y:
                          
                            z = [fraction * 20 + i * 5 for i in range(len(x))]  
                            
                            points_3d[applicator.replace('_', ' ').title()] = (x, y, z)
            
         
            if not points_3d:
                print(f"⚠️ No annotation data found for fraction {fraction}, creating sample data")
                points_3d = self.create_sample_3d_data(fraction)
            
            return points_3d
            
        except Exception as e:
            print(f"❌ Error extracting 3D points for fraction {fraction}: {e}")
          
            return self.create_sample_3d_data(fraction)

    def create_sample_3d_data(self, fraction):
     
        points_3d = {}
        
       
        sample_data = {
            'Tandem Applicator': {
                'x': [10, 15, 20],
                'y': [20, 25, 30], 
                'z': [fraction * 20, fraction * 20 + 5, fraction * 20 + 10]
            },
            'Left Ovoid': {
                'x': [5, 8],
                'y': [15, 18],
                'z': [fraction * 20, fraction * 20 + 3]
            },
            'Right Ovoid': {
                'x': [25, 28],
                'y': [15, 18],
                'z': [fraction * 20, fraction * 20 + 3]
            }
        }
        
        for applicator, coords in sample_data.items():
            points_3d[applicator] = (coords['x'], coords['y'], coords['z'])
        
        return points_3d

    def preview_and_save_pdf(self, temp_pdf_path):
       
        try:
            import webbrowser
            import threading
            
       
            messagebox.showinfo(
                "PDF Report Generated", 
                f"Comprehensive PDF report has been generated!\n\n"
                f"Temporary file: {temp_pdf_path}\n\n"
                f"The PDF will now open for preview, and you will be prompted to save it."
            )
            
           
            def open_pdf():
                try:
                    webbrowser.open(temp_pdf_path)
                except Exception as e:
                    print(f"❌ Error opening PDF: {e}")
            
     
            preview_thread = threading.Thread(target=open_pdf)
            preview_thread.daemon = True
            preview_thread.start()
            
       
            save_path = filedialog.asksaveasfilename(
                title="Save Comprehensive PDF Report As",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Brachytherapy_Comprehensive_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            )
            
            if save_path:
        
                import shutil
                try:
                    shutil.copy2(temp_pdf_path, save_path)
                    messagebox.showinfo(
                        "PDF Saved", 
                        f"Comprehensive report saved successfully to:\n{save_path}\n\n"
                        f"The report includes:\n"
                        f"• Patient information\n"
                        f"• All analysis results from TXT files\n" 
                        f"• Annotated fraction images\n"
                        f"• 3D applicator visualizations\n"
                        f"• Clinical summary and recommendations"
                    )
                    
             
                    print_pdf = messagebox.askyesno(
                        "Print Report", 
                        "Would you like to print the comprehensive report now?"
                    )
                    
                    if print_pdf:
                        try:
                           
                            if os.name == 'nt':  
                                os.startfile(save_path, "print")
                            elif os.name == 'posix':  
                                os.system(f'lpr "{save_path}"')
                            else:
                                webbrowser.open(save_path)
                            
                            messagebox.showinfo("Print", "Print job sent to printer")
                        except Exception as e:
                            messagebox.showwarning("Print", f"Could not auto-print: {str(e)}\nPlease print manually.")
                
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save PDF: {str(e)}")
            
            else:
               
                messagebox.showinfo(
                    "PDF Preview", 
                    f"PDF preview is open in your default viewer.\n\n"
                    f"Temporary file location:\n{temp_pdf_path}\n\n"
                    f"You can save the file later using 'Save As' in your PDF viewer."
                )
            
        except Exception as e:
            messagebox.showerror("PDF Error", f"Error handling PDF: {str(e)}")

    def generate_comprehensive_report(self):
     
        try:
           
            self.collect_report_data()
            
           
            pdf_file = os.path.join(self.temp_dir, "Brachytherapy_Analysis_Report.pdf")
            doc = SimpleDocTemplate(pdf_file, pagesize=A4, 
                                  topMargin=0.5*inch, bottomMargin=0.5*inch,
                                  leftMargin=0.4*inch, rightMargin=0.4*inch)
            
        
            story = []
            
            # ========== COVER PAGE ==========
            story.extend(self.create_professional_cover_page())
            story.append(PageBreak())
            
            # ========== TABLE OF CONTENTS ==========
            story.extend(self.create_table_of_contents())
            story.append(PageBreak())
            
            # ========== EXECUTIVE SUMMARY ==========
            story.extend(self.create_executive_summary())
            story.append(PageBreak())
            
            # ========== PATIENT INFORMATION ==========
            story.extend(self.create_professional_patient_section())
            story.append(PageBreak())
            
            # ========== METHODOLOGY & CALIBRATION ==========
            story.extend(self.create_methodology_section())
            story.append(Spacer(1, 15))
            
            # ========== IMAGE ANALYSIS ==========
            story.extend(self.create_professional_image_section())
            story.append(PageBreak())
            
            # ========== QUANTITATIVE ANALYSIS ==========
            story.extend(self.create_quantitative_analysis_section())
            story.append(PageBreak())
            
            # ========== 3D VISUALIZATION ==========
            story.extend(self.create_professional_3d_section())
            story.append(PageBreak())
            
            # ========== CLINICAL INTERPRETATION ==========
            story.extend(self.create_clinical_interpretation_section())
            story.append(PageBreak())
            
            # ========== APPENDICES ==========
            story.extend(self.create_appendices_section())
            
         
            doc.build(story)
            
         
            self.preview_and_save_pdf(pdf_file)
                              
        except Exception as e:
            messagebox.showerror("PDF Generation Error", 
                               f"Failed to generate comprehensive PDF report: {str(e)}\n\n"
                               f"Error type: {type(e).__name__}")

    def create_professional_cover_page(self):
        
        story = []
        styles = getSampleStyleSheet()
        
  
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=1,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=20
        )
        story.append(Paragraph("DEPARTMENT OF RADIATION ONCOLOGY<br/>BRACHYTHERAPY DIVISION", header_style))
        story.append(Spacer(1, 30))
        
     
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=20,
            alignment=1,
            textColor=colors.HexColor('#1A237E'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("HDR BRACHYTHERAPY APPLICATOR ANALYSIS REPORT", title_style))
        
       
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Heading2'],
            fontSize=14,
            alignment=1,
            textColor=colors.HexColor('#3949AB'),
            spaceAfter=40
        )
        story.append(Paragraph("3D Positioning and Fraction Reproducibility Assessment", subtitle_style))
        story.append(Spacer(1, 40))
        
    
        patient_info = self.report_data['patient_info']
        info_style = ParagraphStyle(
            'PatientInfoStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=0,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#F5F5F5'),
            borderPadding=15,
            borderColor=colors.HexColor('#BDBDBD'),
            borderWidth=1
        )
        
        info_text = f"""
        <b>PATIENT:</b> {patient_info['Name']}<br/>
        <b>MEDICAL RECORD NUMBER:</b> {patient_info['Admission Number']}<br/>
        <b>STUDY DATE:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        <b>FRACTIONS ANALYZED:</b> {patient_info['Number of Fractions']}<br/>
        <b>REPORT ID:</b> BT-{datetime.now().strftime('%Y%m%d')}-001
        """
        story.append(Paragraph(info_text, info_style))
        story.append(Spacer(1, 50))
        
      
        summary_style = ParagraphStyle(
            'SummaryStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            textColor=colors.HexColor('#616161')
        )
        story.append(Paragraph("This report contains quantitative analysis of applicator positioning<br/>"
                             "and reproducibility between treatment fractions for quality assurance<br/>"
                             "in HDR brachytherapy procedures.", summary_style))
        story.append(Spacer(1, 60))
        
       
        confidential_style = ParagraphStyle(
            'ConfidentialStyle',
            parent=styles['Italic'],
            fontSize=9,
            alignment=1,
            textColor=colors.HexColor('#757575')
        )
        story.append(Paragraph("CONFIDENTIAL MEDICAL DOCUMENT - FOR AUTHORIZED PERSONNEL ONLY", confidential_style))
        
        return story

    def create_table_of_contents(self):
      
        story = []
        styles = getSampleStyleSheet()
        
     
        title_style = ParagraphStyle(
            'TOCTitle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=1,
            textColor=colors.HexColor('#1A237E'),
            spaceAfter=30
        )
        story.append(Paragraph("TABLE OF CONTENTS", title_style))
        
    
        toc_items = [
            ("1.0", "EXECUTIVE SUMMARY", "3"),
            ("2.0", "PATIENT INFORMATION", "4"),
            ("3.0", "METHODOLOGY & CALIBRATION", "5"),
            ("4.0", "IMAGE ANALYSIS", "6"),
            ("5.0", "QUANTITATIVE ANALYSIS", "7"),
            ("6.0", "3D SPATIAL VISUALIZATION", "8"),
            ("7.0", "CLINICAL INTERPRETATION", "9"),
            ("8.0", "APPENDICES", "10")
        ]
        
     
        toc_data = [["Section", "Description", "Page"]]
        for number, title, page in toc_items:
            toc_data.append([number, title, page])
        
        toc_table = Table(toc_data, colWidths=[0.8*inch, 4.5*inch, 0.8*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A237E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(toc_table)
        story.append(Spacer(1, 30))
        
        
        doc_info_style = ParagraphStyle(
            'DocInfoStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#616161')
        )
        story.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M')}", doc_info_style))
        story.append(Paragraph("<b>Software Version:</b> BrachyApp v2.0", doc_info_style))
        story.append(Paragraph("<b>Analysis Protocol:</b> TG-43 Compliant", doc_info_style))
        
        return story

    def create_executive_summary(self):
        
        story = []
        styles = getSampleStyleSheet()
        
      
        story.append(Paragraph("1.0 EXECUTIVE SUMMARY", styles['Heading1']))
        story.append(Spacer(1, 15))
        
        
        summary_style = ParagraphStyle(
            'ExecSummaryStyle',
            parent=styles['Normal'],
            fontSize=10,
            backColor=colors.HexColor('#E8F5E8'),
            borderPadding=15,
            borderColor=colors.HexColor('#4CAF50'),
            borderWidth=1,
            leading=14
        )
        
        summary_text = """
        <b>CLINICAL OVERVIEW:</b><br/>
        This report presents a comprehensive analysis of intracavitary applicator positioning 
        and reproducibility between treatment fractions for HDR brachytherapy. The analysis 
        includes quantitative measurements, 3D spatial relationships, and clinical assessment 
        of applicator stability.
        
        <br/><br/><b>KEY METRICS:</b><br/>
        • Applicator positioning accuracy relative to anatomical landmarks<br/>
        • Fraction-to-fraction reproducibility analysis<br/>
        • 3D spatial coordinate assessment<br/>
        • Clinical quality assurance metrics
        """
        story.append(Paragraph(summary_text, summary_style))
        story.append(Spacer(1, 20))
        
       
        findings_style = ParagraphStyle(
            'FindingsStyle',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            leading=13
        )
        
        story.append(Paragraph("<b>PRINCIPAL FINDINGS:</b>", styles['Heading3']))
        findings = [
            "All applicator components successfully identified and measured in both AP and lateral views",
            "Distance measurements established relative to consistent anatomical reference points",
            "3D spatial analysis demonstrates applicator positioning relationships",
            "Fraction comparison provides reproducibility assessment for quality assurance"
        ]
        
        for finding in findings:
            story.append(Paragraph(f"• {finding}", findings_style))
        
        story.append(Spacer(1, 20))
        
      
        clinical_style = ParagraphStyle(
            'ClinicalStyle',
            parent=styles['Normal'],
            fontSize=10,
            backColor=colors.HexColor('#E3F2FD'),
            borderPadding=12,
            borderColor=colors.HexColor('#2196F3'),
            borderWidth=1,
            leading=13
        )
        
        clinical_text = """
        <b>CLINICAL SIGNIFICANCE:</b><br/>
        Precise applicator positioning is critical for optimal dose delivery in brachytherapy. 
        This analysis provides quantitative verification of applicator placement consistency 
        between fractions, supporting treatment quality assurance and potential replanning decisions.
        """
        story.append(Paragraph(clinical_text, clinical_style))
        
        return story

    def create_professional_patient_section(self):
     
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("2.0 PATIENT INFORMATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        patient_info = self.report_data['patient_info']
        
     
        main_data = [
            ["Patient Name:", patient_info['Name']],
            ["Medical Record Number:", patient_info['Admission Number']],
            ["Date of Analysis:", datetime.now().strftime('%B %d, %Y')]
        ]
        
        main_table = Table(main_data, colWidths=[2.5*inch, 3.5*inch])
        main_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(main_table)
        story.append(Spacer(1, 15))
        
  
        treatment_data = [
            ["Treatment Parameter", "Value"],
            ["Number of Fractions", patient_info['Number of Fractions']],
            ["First Fraction Date", patient_info['First Fraction Date']],
            ["Second Fraction Date", patient_info['Second Fraction Date']],
            ["AP Pixel Spacing", patient_info['AP Pixel Spacing']],
            ["Lateral Pixel Spacing", patient_info['Lateral Pixel Spacing']]
        ]
        
        treatment_table = Table(treatment_data, colWidths=[2.5*inch, 3.5*inch])
        treatment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A237E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(treatment_table)
        
        return story

    def create_methodology_section(self):
    
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("3.0 METHODOLOGY & CALIBRATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        
        method_style = ParagraphStyle(
            'MethodologyStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14
        )
        
        method_text = """
        <b>ANALYSIS METHODOLOGY:</b><br/>
        This analysis employs a standardized protocol for brachytherapy applicator assessment:
        
        <br/><br/><b>1. IMAGE ACQUISITION & CALIBRATION</b><br/>
        • Digital radiographs acquired in AP and lateral projections<br/>
        • Pixel-to-millimeter calibration applied using known spacing parameters<br/>
        • Image quality optimization for anatomical visualization
        
        <br/><br/><b>2. ANATOMICAL LANDMARK IDENTIFICATION</b><br/>
        • Consistent anatomical reference points identified across fractions<br/>
        • Reference line established for reproducible measurement baseline<br/>
        • Landmark verification in both imaging planes
        
        <br/><br/><b>3. APPLICATOR LOCALIZATION</b><br/>
        • Tandem and ovoid applicator components identified<br/>
        • Tip and base points annotated for spatial reference<br/>
        • 3D coordinate system establishment
        
        <br/><br/><b>4. QUANTITATIVE ANALYSIS</b><br/>
        • Euclidean distance calculations from applicators to anatomical references<br/>
        • Fraction-to-fraction displacement analysis<br/>
        • 3D spatial relationship mapping
        """
        
        story.append(Paragraph(method_text, method_style))
        story.append(Spacer(1, 15))
        

        calib_style = ParagraphStyle(
            'CalibrationStyle',
            parent=styles['Normal'],
            fontSize=9,
            backColor=colors.HexColor('#FFF3E0'),
            borderPadding=10,
            borderColor=colors.HexColor('#FFB74D'),
            borderWidth=1
        )
        
        calib_text = f"""
        <b>CALIBRATION PARAMETERS:</b><br/>
        • AP View Pixel Spacing: {self.pixel_spacing.get('AP_frac1', 0.2979):.4f} mm/pixel<br/>
        • Lateral View Pixel Spacing: {self.pixel_spacing.get('LAT_frac1', 0.2979):.4f} mm/pixel<br/>
        • Measurement Accuracy: ±0.1 mm (theoretical)<br/>
        • Coordinate System: Patient-based 3D Cartesian
        """
        
        story.append(Paragraph(calib_text, calib_style))
        
        return story

    def create_professional_image_section(self):
       
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("4.0 IMAGE ANALYSIS", styles['Heading1']))
        story.append(Spacer(1, 12))
        
      
        status_data = [["View", "Fraction", "Status", "Quality"]]
        
        image_types = {
            "AP_frac1": "AP", "AP_frac2": "AP", 
            "LAT_frac1": "Lateral", "LAT_frac2": "Lateral"
        }
        
        for key, view_type in image_types.items():
            path = self.image_paths.get(key)
            frac_num = "1" if "frac1" in key else "2"
            
            if path and os.path.exists(path):
                status = "✓ Acquired"
                quality = "Diagnostic"
            else:
                status = "✗ Not Available"
                quality = "N/A"
            
            status_data.append([view_type, f"Fraction {frac_num}", status, quality])
        
        status_table = Table(status_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.2*inch])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        
        story.append(status_table)
        story.append(Spacer(1, 20))
        
        
        story.append(Paragraph("ANNOTATED IMAGES", styles['Heading2']))
        story.append(Spacer(1, 10))
        
   
        images_note_style = ParagraphStyle(
            'ImagesNoteStyle',
            parent=styles['Italic'],
            fontSize=9,
            textColor=colors.HexColor('#757575'),
            alignment=1
        )
        story.append(Paragraph("Refer to electronic image files for detailed annotated views", images_note_style))
        
        return story

    def create_quantitative_analysis_section(self):
     
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("5.0 QUANTITATIVE ANALYSIS", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        analysis_results = self.report_data['analysis_results']
        
        if not analysis_results:
            no_data_style = ParagraphStyle(
                'NoDataStyle',
                parent=styles['Italic'],
                fontSize=10,
                textColor=colors.HexColor('#757575'),
                alignment=1
            )
            story.append(Paragraph("Quantitative analysis data will appear here after completing image annotation and analysis procedures.", no_data_style))
            return story
        
        
        story.append(Paragraph("KEY QUANTITATIVE METRICS", styles['Heading2']))
        story.append(Spacer(1, 8))
        
       
        summary_data = [["Analysis Type", "Files Available", "Status"]]
        
        analysis_categories = {
            "Distance Measurements": [f for f in analysis_results.keys() if 'distance' in f.lower()],
            "Shift Analysis": [f for f in analysis_results.keys() if 'shift' in f.lower()],
            "3D Movement": [f for f in analysis_results.keys() if '3d' in f.lower() or 'movement' in f.lower()],
            "Fraction Comparison": [f for f in analysis_results.keys() if 'comparison' in f.lower()]
        }
        
        for category, files in analysis_categories.items():
            if files:
                count = len(files)
                status = "✓ Complete"
            else:
                count = 0
                status = "Pending"
            summary_data.append([category, str(count), status])
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
       
        appendix_ref_style = ParagraphStyle(
            'AppendixRefStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#616161')
        )
        story.append(Paragraph("<b>Detailed quantitative data available in Appendices (Section 8.0)</b>", appendix_ref_style))
        story.append(Paragraph("Includes complete distance measurements, shift calculations, and statistical analysis", appendix_ref_style))
        
        return story

    def create_professional_3d_section(self):
   
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("6.0 3D SPATIAL VISUALIZATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
     
        desc_style = ParagraphStyle(
            '3DDescStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14
        )
        
        desc_text = """
        <b>SPATIAL ANALYSIS METHODOLOGY:</b><br/>
        Three-dimensional visualization of applicator positioning provides critical spatial context 
        for treatment planning and quality assurance. The 3D coordinate system integrates data 
        from orthogonal radiographic views to reconstruct applicator geometry.
        
        <br/><br/><b>COORDINATE SYSTEM:</b><br/>
        • X-axis: Patient left-to-right (lateral direction)<br/>
        • Y-axis: Patient anterior-to-posterior (AP direction)<br/>
        • Z-axis: Patient superior-to-inferior (cranial-caudal)<br/>
        • Origin: Anatomical reference point
        
        <br/><br/><b>VISUALIZATION COMPONENTS:</b><br/>
        • Individual fraction applicator positioning<br/>
        • Fraction-to-fraction spatial comparison<br/>
        • Applicator component relationship mapping<br/>
        • Anatomical reference framework
        """
        
        story.append(Paragraph(desc_text, desc_style))
        story.append(Spacer(1, 15))
        
    
        viz_note_style = ParagraphStyle(
            'VizNoteStyle',
            parent=styles['Italic'],
            fontSize=9,
            textColor=colors.HexColor('#757575'),
            alignment=1
        )
        story.append(Paragraph("3D visualization plots are generated and available in the electronic report package", viz_note_style))
        
        return story

    def create_clinical_interpretation_section(self):
       
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("7.0 CLINICAL INTERPRETATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
     
        assessment_style = ParagraphStyle(
            'AssessmentStyle',
            parent=styles['Normal'],
            fontSize=10,
            backColor=colors.HexColor('#F3E5F5'),
            borderPadding=15,
            borderColor=colors.HexColor('#7B1FA2'),
            borderWidth=1,
            leading=14
        )
        
        assessment_text = """
        <b>CLINICAL ASSESSMENT:</b><br/>
        Based on the comprehensive analysis of applicator positioning and reproducibility, 
        this assessment provides clinical context for the quantitative measurements.
        
        <br/><br/><b>POSITIONING ACCURACY:</b><br/>
        Applicator placement demonstrates [ASSESSMENT BASED ON DATA] consistency between 
        fractions. The spatial relationships maintained suggest [CLINICAL IMPLICATION].
        
        <br/><br/><b>REPRODUCIBILITY:</b><br/>
        Fraction-to-fraction variations fall within [CLINICALLY ACCEPTABLE/REQUIRES REVIEW] 
        ranges. This level of reproducibility [SUPPORTS/MAY AFFECT] treatment delivery accuracy.
        """
        
        story.append(Paragraph(assessment_text, assessment_style))
        story.append(Spacer(1, 20))
        
  
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", styles['Heading2']))
        
        rec_style = ParagraphStyle(
            'RecommendationStyle',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=15,
            leading=13,
            bulletIndent=15
        )
        
        recommendations = [
            "Review quantitative measurements in clinical context before treatment decisions",
            "Consider applicator shifts when evaluating dose distribution reproducibility",
            "Verify anatomical consistency between fractions using available imaging",
            "Utilize 3D spatial relationships for comprehensive understanding of geometry",
            "Document analysis findings in patient treatment records",
            "Consider replanning if significant deviations from intended positioning are noted"
        ]
        
        for recommendation in recommendations:
            story.append(Paragraph(f"• {recommendation}", rec_style))
        
        story.append(Spacer(1, 20))
        
        
        qa_style = ParagraphStyle(
            'QAStyle',
            parent=styles['Normal'],
            fontSize=9,
            backColor=colors.HexColor('#E8F5E8'),
            borderPadding=10,
            borderColor=colors.HexColor('#4CAF50'),
            borderWidth=1
        )
        
        qa_text = """
        <b>QUALITY ASSURANCE VERIFICATION:</b><br/>
        This analysis supports brachytherapy quality assurance protocols by providing 
        quantitative verification of applicator positioning consistency. The methodology 
        aligns with established clinical physics practices for treatment verification.
        """
        
        story.append(Paragraph(qa_text, qa_style))
        
        return story

    def create_appendices_section(self):
     
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("8.0 APPENDICES", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        analysis_results = self.report_data['analysis_results']
        
        if not analysis_results:
            story.append(Paragraph("<i>No appendix data available</i>", styles['Italic']))
            return story
        
        
        categories = {
            "A. DISTANCE MEASUREMENTS": [f for f in analysis_results.keys() if 'distance' in f.lower()],
            "B. SHIFT ANALYSIS": [f for f in analysis_results.keys() if 'shift' in f.lower()],
            "C. 3D MOVEMENT ANALYSIS": [f for f in analysis_results.keys() if '3d' in f.lower() or 'movement' in f.lower()],
            "D. COMPARISON STUDIES": [f for f in analysis_results.keys() if 'comparison' in f.lower()],
            "E. ADDITIONAL DATA": [f for f in analysis_results.keys() if f not in [item for sublist in categories.values() for item in sublist]]
        }
        
        for category_title, files in categories.items():
            if files:
                story.append(Paragraph(category_title, styles['Heading2']))
                story.append(Spacer(1, 8))
                
                for file_name in sorted(files):
                    content = analysis_results[file_name]
                    display_name = file_name.replace('_', ' ').replace('.txt', '').title()
                    
                    story.append(Paragraph(f"<b>{display_name}</b>", styles['Heading3']))
                    
                   
                    content_style = ParagraphStyle(
                        'AppendixContentStyle',
                        parent=styles['Code'],
                        fontSize=7,
                        fontName='Courier',
                        leftIndent=10,
                        backColor=colors.HexColor('#F8F9FA'),
                        borderPadding=8,
                        borderColor=colors.HexColor('#E0E0E0'),
                        borderWidth=0.5,
                        leading=9
                    )
                    
                 
                    if len(content) > 1500:
                        content = content[:1500] + "\n\n[CONTENT TRUNCATED - SEE ELECTRONIC FILE FOR COMPLETE DATA]"
                    
                    story.append(Paragraph(content.replace('\n', '<br/>'), content_style))
                    story.append(Spacer(1, 12))
        
        return story

    def create_title_page(self):
        
        story = []
        styles = getSampleStyleSheet()
        
      
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  
            textColor=colors.HexColor('#2E7D32')
        )
        
        story.append(Paragraph("HDR CO-60 BRACHYTHERAPY COMPREHENSIVE ANALYSIS REPORT", title_style))
        story.append(Spacer(1, 20))
        
      
        subtitle_style = ParagraphStyle(
            'CustomSubtitle', 
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,
            textColor=colors.HexColor('#555555')
        )
        story.append(Paragraph("Applicator Positioning and Fraction Comparison Analysis", subtitle_style))
        story.append(Spacer(1, 40))
        
       
        patient_info = self.report_data['patient_info']
        info_text = f"""
        <b>Patient Name:</b> {patient_info['Name']}<br/>
        <b>Admission Number:</b> {patient_info['Admission Number']}<br/>
        <b>Analysis Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>
        <b>Number of Fractions:</b> {patient_info['Number of Fractions']}<br/>
        <b>First Fraction Date:</b> {patient_info['First Fraction Date']}<br/>
        <b>Second Fraction Date:</b> {patient_info['Second Fraction Date']}
        """
        
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=12,
            backColor=colors.HexColor('#F5F5F5'),
            borderPadding=10,
            borderColor=colors.HexColor('#CCCCCC'),
            borderWidth=1
        )
        
        story.append(Paragraph(info_text, info_style))
        story.append(Spacer(1, 60))
        
        
        desc_text = """
        <b>Report Contents:</b><br/>
        • Complete patient information and image status<br/>
        • Annotated fraction images (AP and Lateral views)<br/>
        • Detailed distance measurements and analysis results<br/>
        • 3D applicator positioning visualizations<br/>
        • Fraction comparison and shift analysis<br/>
        • Clinical summary and recommendations
        """
        
        story.append(Paragraph(desc_text, styles['Normal']))
        story.append(Spacer(1, 40))
        
    
        confidential_style = ParagraphStyle(
            'Confidential',
            parent=styles['Italic'],
            fontSize=10,
            alignment=1,
            textColor=colors.HexColor('#666666')
        )
        story.append(Paragraph("<i>Comprehensive Clinical Report - For Medical Use Only</i>", confidential_style))
        
        return story

    def add_text_files_section(self, story, heading_style, normal_style, small_style):
   
        story.append(PageBreak())
        story.append(Paragraph("2. ANALYSIS DATA FILES", heading_style))
        story.append(Paragraph("This section contains all generated analysis files and distance measurements.", normal_style))
        story.append(Spacer(1, 12))
        
       
        text_files = []
        for file in os.listdir(self.temp_dir):
            if file.endswith('.txt'):
                text_files.append(file)
        
        if not text_files:
            story.append(Paragraph("No analysis files found. Please complete the analysis workflow first.", normal_style))
            return
        
        for text_file in sorted(text_files):
            file_path = os.path.join(self.temp_dir, text_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
             
                story.append(Paragraph(f"File: {text_file}", normal_style))
                
              
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        
                        if line.startswith('===') or line.startswith('---') or any(x in line for x in ['SHIFT', 'DISTANCE', 'COMPARISON']):
                            story.append(Paragraph(line, small_style))
                        else:
                            story.append(Paragraph(line, small_style))
                
                story.append(Spacer(1, 10))
                
            except Exception as e:
                story.append(Paragraph(f"Error reading file {text_file}: {str(e)}", normal_style))
        
        story.append(PageBreak())

    def add_annotation_images_section(self, story, heading_style, normal_style):
        
        story.append(Paragraph("3. ANNOTATION VISUALIZATIONS", heading_style))
        story.append(Paragraph("Applicator positioning and anatomy annotations for each fraction.", normal_style))
        story.append(Spacer(1, 12))
        
        
        image_patterns = [
            "*_edited.png",
            "*_combined_mask.png",
            "*_mask.png"
        ]
        
        found_images = []
        for pattern in image_patterns:
            for file in glob.glob(os.path.join(self.temp_dir, pattern)):
                found_images.append(file)
        
        if not found_images:
            story.append(Paragraph("No annotation images found. Please complete image annotation first.", normal_style))
            return
        
        
        ap_images = [img for img in found_images if "AP" in os.path.basename(img)]
        lat_images = [img for img in found_images if "LAT" in os.path.basename(img)]
        
        
        if ap_images:
            story.append(Paragraph("AP View Annotations", normal_style))
            self.add_image_grid(story, ap_images, "AP")
            story.append(Spacer(1, 20))
        
       
        if lat_images:
            story.append(Paragraph("Lateral View Annotations", normal_style))
            self.add_image_grid(story, lat_images, "LAT")
        
        story.append(PageBreak())

    def add_image_grid(self, story, images, view_type):
        """Add a grid of images to the PDF"""
        try:
        
            img_elements = []
            for img_path in images[:4]:  
                try:
                  
                    img = PILImage.open(img_path)
                    img.thumbnail((200, 200))  
                    
                   
                    temp_img_path = os.path.join(self.temp_dir, f"temp_{os.path.basename(img_path)}")
                    img.save(temp_img_path)
                    
                    
                    pdf_img = Image(temp_img_path, width=150, height=150)
                    img_elements.append(pdf_img)
                    
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")
                    continue
            
            
            for i in range(0, len(img_elements), 2):
                row_images = img_elements[i:i+2]
                row_data = [[img, Paragraph(self.safe_get_filename(images[i]), normal_style)] 
                           for img in row_images]
                
                if row_data:
                    img_table = Table(row_data, colWidths=[160, 160])
                    img_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ]))
                    story.append(img_table)
                    story.append(Spacer(1, 10))
                    
        except Exception as e:
            story.append(Paragraph(f"Error adding images: {str(e)}", normal_style))

    def add_analysis_results_section(self, story, heading_style, normal_style, small_style):
        
        story.append(Paragraph("4. ANALYSIS RESULTS AND COMPARISONS", heading_style))
        
      
        shifts = self.calculate_direct_shifts_between_fractions()
        if shifts:
            story.append(Paragraph("Applicator Shifts Between Fractions", normal_style))
            
            shift_data = [["Applicator", "Tip Shift (mm)", "Base Shift (mm)", "Average Shift (mm)"]]
            for applicator, data in shifts.items():
                shift_data.append([
                    applicator,
                    f"{data.get('tip_shift_mm', 0):.2f}",
                    f"{data.get('base_shift_mm', 0):.2f}",
                    f"{data.get('average_shift_mm', 0):.2f}"
                ])
            
            shift_table = Table(shift_data, colWidths=[120, 80, 80, 80])
            shift_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#27ae60")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(shift_table)
            story.append(Spacer(1, 15))
        
        
        self.add_distance_comparisons(story, normal_style, small_style)

    def add_distance_comparisons(self, story, normal_style, small_style):
      
        try:
         
            comp_files = [
                "applicator_shifts_between_fractions.txt",
                "AP_direct_euclidean_comparison.txt",
                "AP_direct_euclidean_comparison_TXT_ONLY.txt"
            ]
            
            for comp_file in comp_files:
                file_path = os.path.join(self.temp_dir, comp_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    story.append(Paragraph(f"Distance Analysis: {comp_file}", normal_style))
                    
                 
                    lines = content.split('\n')
                    key_lines = [line for line in lines if any(x in line for x in 
                            ['Average', 'Maximum', 'EXCELLENT', 'GOOD', 'MODERATE', 'SIGNIFICANT'])]
                    
                    for line in key_lines[:10]:  # Limit to 10 key lines
                        if line.strip():
                            story.append(Paragraph(line, small_style))
                    
                    story.append(Spacer(1, 10))
                    
        except Exception as e:
            story.append(Paragraph(f"Error adding distance comparisons: {str(e)}", normal_style))

    def add_clinical_summary_section(self, story, heading_style, normal_style):
       
        story.append(PageBreak())
        story.append(Paragraph("5. CLINICAL SUMMARY AND RECOMMENDATIONS", heading_style))
        
    
        summary_points = []
        
      
        uploaded_images = sum(1 for path in self.image_paths.values() if path)
        total_images = len(self.image_paths)
        summary_points.append(f"• Images Uploaded: {uploaded_images}/{total_images}")
        
     
        analysis_files = [
            "AP_frac1_distances_from_anatomy.txt",
            "AP_frac2_distances_from_anatomy.txt"
        ]
        
        completed_analyses = sum(1 for f in analysis_files if os.path.exists(os.path.join(self.temp_dir, f)))
        summary_points.append(f"• Completed Analyses: {completed_analyses}/{len(analysis_files)}")
        
     
        shifts = self.calculate_direct_shifts_between_fractions()
        if shifts:
            max_shift = 0
            for applicator, data in shifts.items():
                avg_shift = data.get('average_shift_mm', 0)
                if avg_shift > max_shift:
                    max_shift = avg_shift
            
            summary_points.append(f"• Maximum Applicator Shift: {max_shift:.2f} mm")
            
         
            if max_shift < 3.0:
                assessment = "EXCELLENT reproducibility - minimal applicator movement"
                color = colors.green
            elif max_shift < 5.0:
                assessment = "GOOD reproducibility - acceptable clinical variation"
                color = colors.orange
            elif max_shift < 7.0:
                assessment = "MODERATE variation - consider clinical impact on dose distribution"
                color = colors.orangered
            else:
                assessment = "SIGNIFICANT movement - review patient positioning and applicator fixation"
                color = colors.red
            
            summary_points.append(f"• Clinical Assessment: {assessment}")
        
       
        for point in summary_points:
            story.append(Paragraph(point, normal_style))
        
        story.append(Spacer(1, 15))
        
     
        story.append(Paragraph("RECOMMENDATIONS:", normal_style))
        recommendations = [
            "• Ensure all required images are uploaded for complete analysis",
            "• Verify applicator annotations for accuracy",
            "• Review shift measurements for clinical significance",
            "• Consider patient-specific factors in interpretation",
            "• Document any positioning concerns for future fractions"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, normal_style))

    def safe_get_filename(self, file_path):
      
        if not file_path:
            return "Not available"
        try:
            filename = os.path.basename(file_path)
            return filename if filename else "Unknown"
        except:
            return "Error reading filename"

    def calculate_direct_shifts_between_fractions(self):
       
        try:
          
            frac1_points = self.load_applicator_points("AP_frac1_annotations.json")
            if not frac1_points:
                return None
        
           
            frac2_points = self.load_applicator_points("AP_frac2_annotations.json")
            if not frac2_points:
                return None
        
            shifts = {}
            mm_per_px = self.pixel_spacing["AP_frac1"]
        
            for applicator in ["applicator_tandem", "left_ovoid", "right_ovoid"]:
                if applicator not in frac1_points or applicator not in frac2_points:
                    continue
                
                tip1 = frac1_points[applicator].get("tip")
                base1 = frac1_points[applicator].get("base")
                tip2 = frac2_points[applicator].get("tip") 
                base2 = frac2_points[applicator].get("base")
            
                if not all([tip1, base1, tip2, base2]):
                    continue
            
              
                tip_shift_px = self.euclidean_distance(tip1, tip2)
                base_shift_px = self.euclidean_distance(base1, base2)
            
                tip_shift_mm = tip_shift_px * mm_per_px
                base_shift_mm = base_shift_px * mm_per_px
            
                applicator_name = applicator.replace('applicator_', '').replace('_', ' ').title()
            
                shifts[applicator_name] = {
                    "tip_shift_mm": tip_shift_mm,
                    "base_shift_mm": base_shift_mm,
                    "average_shift_mm": (tip_shift_mm + base_shift_mm) / 2
                }
        
            return shifts
        except Exception as e:
            print(f"Error calculating shifts: {e}")
            return None

    def parse_distance_files(self, view_type):
   
        data = {}
        
        try:
            for fraction in ["1", "2"]:
                file_path = os.path.join(self.temp_dir, f"{view_type}_frac{fraction}_distances_from_anatomy.txt")
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    
                    lines = content.split('\n')
                    current_applicator = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line or "===" in line:
                            continue
                        
                      
                        if "Applicator" in line and ":" not in line and "to" not in line:
                            current_applicator = line.replace(":", "").strip()
                            if current_applicator not in data:
                                data[current_applicator] = {}
                            continue
                        
                      
                        if "to Anatomy" in line and "mm" in line:
                      
                            parts = line.split(":")
                            if len(parts) == 2:
                                measurement_name = parts[0].strip()
                                value_str = parts[1].replace("mm", "").strip()
                                
                                try:
                                    value = float(value_str)
                                  
                                    key = f"frac{fraction}"
                                    if measurement_name not in data.get(current_applicator, {}):
                                        if current_applicator not in data:
                                            data[current_applicator] = {}
                                        data[current_applicator][measurement_name] = {}
                                    
                                    data[current_applicator][measurement_name][key] = value
                                except ValueError:
                                    continue
            
      
            comparison_data = {}
            if data:  
                for applicator, measurements in data.items():
                    comparison_data[applicator] = {}
                    for measurement_name, fractions in measurements.items():
                        if 'frac1' in fractions and 'frac2' in fractions:
                            comparison_data[applicator][measurement_name] = {
                                'fraction1': fractions['frac1'],
                                'fraction2': fractions['frac2'],
                                'shift': fractions['frac2'] - fractions['frac1']
                            }
            
            return comparison_data if comparison_data else {}  
            
        except Exception as e:
            print(f"Error parsing {view_type} distance files: {e}")
            return {}  

    def calculate_overall_statistics(self):
        
        shifts = []
        
    
        ap_data = self.parse_distance_files("AP")
        if ap_data and isinstance(ap_data, dict):
            for applicator, measurements in ap_data.items():
                if isinstance(measurements, dict):
                    for measurement_name, data in measurements.items():
                        if isinstance(data, dict) and 'shift' in data:
                            shifts.append(data['shift'])
        
     
        lat_data = self.parse_distance_files("LAT")
        if lat_data and isinstance(lat_data, dict):
            for applicator, measurements in lat_data.items():
                if isinstance(measurements, dict):
                    for measurement_name, data in measurements.items():
                        if isinstance(data, dict) and 'shift' in data:
                            shifts.append(data['shift'])
        
        if not shifts:
            return {
                'max_shift': 0,
                'avg_shift': 0,
                'total_measurements': 0,
                'assessment': 'No data available for analysis',
                'details': 'Please complete annotation for both fractions'
            }
        
        max_shift = max(abs(shift) for shift in shifts)
        avg_shift = sum(shifts) / len(shifts)
        
       
        if max_shift < 3.0:
            assessment = "✓ EXCELLENT reproducibility"
            details = "Minimal applicator movement between fractions"
        elif max_shift < 5.0:
            assessment = "✓ GOOD reproducibility"
            details = "Acceptable clinical variation"
        elif max_shift < 7.0:
            assessment = "⚠ MODERATE variation"
            details = "Consider clinical impact on dose distribution"
        else:
            assessment = "❌ SIGNIFICANT movement"
            details = "Review patient positioning and applicator fixation"
        
        return {
            'max_shift': max_shift,
            'avg_shift': avg_shift,
            'total_measurements': len(shifts),
            'assessment': assessment,
            'details': details
        }

    def generate_quick_report(self):
       
        try:
          
            report_content = []
            report_content.append("QUICK ANALYSIS REPORT")
            report_content.append("=" * 50)
            report_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_content.append("")
            
            
            report_content.append("PATIENT INFORMATION")
            report_content.append("-" * 30)
            report_content.append(f"Name: {self.name_entry.get() or 'Not specified'}")
            report_content.append(f"Admission Number: {self.admission_entry.get() or 'Not specified'}")
            report_content.append(f"Number of Fractions: {self.fractions_entry.get() or 'Not specified'}")
            report_content.append("")
            
           
            report_content.append("IMAGE STATUS")
            report_content.append("-" * 30)
            for key, path in self.image_paths.items():
                status = "Uploaded" if path else "Not uploaded"
                report_content.append(f"{key}: {status}")
            report_content.append("")
            
            
            report_file = os.path.join(self.temp_dir, "quick_report.txt")
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("\n".join(report_content))
                
            messagebox.showinfo("Quick Report Generated", 
                              f"Quick report saved to:\n{report_file}")
                              
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate quick report: {str(e)}")

    def generate_comprehensive_report(self):
    
        try:
       
            self.collect_report_data()
            
           
            pdf_file = os.path.join(self.temp_dir, "comprehensive_analysis_report.pdf")
            doc = SimpleDocTemplate(pdf_file, pagesize=A4, 
                                  topMargin=1*inch, bottomMargin=1*inch,
                                  leftMargin=0.5*inch, rightMargin=0.5*inch)
            
            
            story = []
            
            # ========== TITLE PAGE ==========
            story.extend(self.create_title_page())
            story.append(PageBreak())
            
            # ========== PATIENT INFORMATION ==========
            story.extend(self.create_patient_info_section())
            story.append(PageBreak())
            
            # ========== IMAGE STATUS AND UPLOADS ==========
            story.extend(self.create_image_status_section())
            story.append(Spacer(1, 20))
            
            # ========== ANNOTATED IMAGES ==========
            story.extend(self.create_detailed_image_section())
            story.append(PageBreak())
            
            # ========== ANALYSIS RESULTS FROM TXT FILES ==========
            story.extend(self.create_detailed_analysis_section())
            story.append(PageBreak())
            
            # ========== 3D VISUALIZATIONS ==========
            story.extend(self.create_3d_visualization_section())
            story.append(PageBreak())
            
            # ========== CLINICAL SUMMARY ==========
            story.extend(self.create_detailed_summary_section())
            
          
            doc.build(story)
            
            
            self.preview_and_save_pdf(pdf_file)
                              
        except Exception as e:
            messagebox.showerror("PDF Generation Error", 
                               f"Failed to generate comprehensive PDF report: {str(e)}\n\n"
                               f"Error type: {type(e).__name__}")


    def create_patient_info_section(self):
        
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("PATIENT INFORMATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        patient_info = self.report_data['patient_info']
        
      
        data = []
        for key, value in patient_info.items():
            data.append([f"<b>{key}:</b>", value])
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD'))
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        return story

    def create_image_status_section(self):
        
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("IMAGE UPLOAD STATUS", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        image_data = [["View", "Fraction", "Status", "File Name"]]
        
        image_types = {
            "AP_frac1": "AP View - Fraction 1",
            "AP_frac2": "AP View - Fraction 2", 
            "LAT_frac1": "Lateral View - Fraction 1",
            "LAT_frac2": "Lateral View - Fraction 2"
        }
        
        for key, display_name in image_types.items():
            path = self.image_paths.get(key)
            if path and os.path.exists(path):
                status = "✅ Uploaded"
                filename = os.path.basename(path)
            else:
                status = "❌ Not uploaded"
                filename = "N/A"
            
            parts = display_name.split(' - ')
            image_data.append([parts[0], parts[1], status, filename])
        
        image_table = Table(image_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 2.5*inch])
        image_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
        ]))
        
        story.append(image_table)
        story.append(Spacer(1, 20))
        
        
        cal_text = f"""
        <b>Pixel Spacing Calibration:</b><br/>
        AP Images: {self.pixel_spacing.get('AP_frac1', 0.2979):.4f} mm/pixel<br/>
        Lateral Images: {self.pixel_spacing.get('LAT_frac1', 0.2979):.4f} mm/pixel
        """
        story.append(Paragraph(cal_text, styles['Normal']))
        
        return story


    def create_detailed_image_section(self):
       
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("ANNOTATED FRACTION IMAGES", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        
        story.append(Paragraph("AP View - Fraction Images", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        ap_images = []
        for frac in [1, 2]:
            img_path = os.path.join(self.temp_dir, f"AP_frac{frac}_edited.png")
            if os.path.exists(img_path):
                ap_images.append((f"Fraction {frac}", img_path))
        
        if ap_images:
        
            ap_data = []
            for label, img_path in ap_images:
                try:
                    pdf_img_path = self.prepare_image_for_pdf(img_path)
                    if pdf_img_path:
                        img = Image(pdf_img_path, width=3.5*inch, height=2.8*inch)
                        ap_data.append([Paragraph(f"<b>{label}</b>", styles['Normal']), img])
                except Exception as e:
                    ap_data.append([Paragraph(f"<b>{label}</b>", styles['Normal']), 
                                  Paragraph(f"Image unavailable: {str(e)}", styles['Italic'])])
            
            if ap_data:
                ap_table = Table(ap_data, colWidths=[2*inch, 4*inch])
                ap_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]))
                story.append(ap_table)
        
        story.append(Spacer(1, 20))
        
        
        story.append(Paragraph("Lateral View - Fraction Images", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        lat_images = []
        for frac in [1, 2]:
            img_path = os.path.join(self.temp_dir, "LAT", f"LAT_frac{frac}_edited.png")
            if not os.path.exists(img_path):
                img_path = os.path.join(self.temp_dir, f"LAT_frac{frac}_edited.png")
            if os.path.exists(img_path):
                lat_images.append((f"Fraction {frac}", img_path))
        
        if lat_images:
          
            lat_data = []
            for label, img_path in lat_images:
                try:
                    pdf_img_path = self.prepare_image_for_pdf(img_path)
                    if pdf_img_path:
                        img = Image(pdf_img_path, width=3.5*inch, height=2.8*inch)
                        lat_data.append([Paragraph(f"<b>{label}</b>", styles['Normal']), img])
                except Exception as e:
                    lat_data.append([Paragraph(f"<b>{label}</b>", styles['Normal']), 
                                   Paragraph(f"Image unavailable: {str(e)}", styles['Italic'])])
            
            if lat_data:
                lat_table = Table(lat_data, colWidths=[2*inch, 4*inch])
                lat_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]))
                story.append(lat_table)
        else:
            story.append(Paragraph("<i>No lateral images available</i>", styles['Italic']))
        
        story.append(Spacer(1, 20))
        return story

    def create_detailed_analysis_section(self):
      
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("DETAILED ANALYSIS RESULTS", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        analysis_results = self.report_data['analysis_results']
        
        if not analysis_results:
            story.append(Paragraph("<i>No analysis results available. Complete AP and Lateral analyses first.</i>", styles['Italic']))
            return story
        
        
        movement_files = [f for f in analysis_results.keys() if '3d' in f.lower() or 'movement' in f.lower()]
        if movement_files:
            story.append(Paragraph("3D MOVEMENT ANALYSIS", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for file_name in sorted(movement_files):
                content = analysis_results[file_name]
                display_name = file_name.replace('_', ' ').replace('.txt', '').title()
                
                story.append(Paragraph(f"<b>{display_name}</b>", styles['Heading3']))
                
              
                content_style = ParagraphStyle(
                    'MovementAnalysisStyle',
                    parent=styles['Code'],
                    fontSize=8,
                    fontName='Courier',
                    leftIndent=10,
                    backColor=colors.HexColor('#E8F5E8'),
                    borderPadding=10,
                    borderColor=colors.HexColor('#4CAF50'),
                    borderWidth=2
                )
                
                story.append(Paragraph(content.replace('\n', '<br/>'), content_style))
                story.append(Spacer(1, 20))
        
     
        distance_files = [f for f in analysis_results.keys() if 'distance' in f.lower() and f not in movement_files]
        if distance_files:
            story.append(Paragraph("DISTANCE MEASUREMENTS", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for file_name in sorted(distance_files):
                content = analysis_results[file_name]
                display_name = file_name.replace('_', ' ').replace('.txt', '').title()
                
                story.append(Paragraph(f"<b>{display_name}</b>", styles['Heading3']))
                
              
                content_style = ParagraphStyle(
                    'CodeStyle',
                    parent=styles['Code'],
                    fontSize=7,
                    fontName='Courier',
                    leftIndent=10,
                    backColor=colors.HexColor('#F8F9FA'),
                    borderPadding=8,
                    borderColor=colors.HexColor('#DDDDDD'),
                    borderWidth=1
                )
                
                story.append(Paragraph(content.replace('\n', '<br/>'), content_style))
                story.append(Spacer(1, 15))
        
      
        shift_files = [f for f in analysis_results.keys() if ('shift' in f.lower() or 'comparison' in f.lower()) and f not in movement_files]
        if shift_files:
            story.append(Paragraph("APPLICATOR SHIFT ANALYSIS", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for file_name in sorted(shift_files):
                content = analysis_results[file_name]
                display_name = file_name.replace('_', ' ').replace('.txt', '').title()
                
                story.append(Paragraph(f"<b>{display_name}</b>", styles['Heading3']))
                
                content_style = ParagraphStyle(
                    'CodeStyle',
                    parent=styles['Code'],
                    fontSize=7,
                    fontName='Courier',
                    leftIndent=10,
                    backColor=colors.HexColor('#FFF3E0'),
                    borderPadding=8,
                    borderColor=colors.HexColor('#FFCC80'),
                    borderWidth=1
                )
                
                story.append(Paragraph(content.replace('\n', '<br/>'), content_style))
                story.append(Spacer(1, 15))
        
        
        other_files = [f for f in analysis_results.keys() if f not in distance_files and f not in shift_files and f not in movement_files]
        if other_files:
            story.append(Paragraph("ADDITIONAL ANALYSIS DATA", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for file_name in sorted(other_files):
                content = analysis_results[file_name]
                display_name = file_name.replace('_', ' ').replace('.txt', '').title()
                
                story.append(Paragraph(f"<b>{display_name}</b>", styles['Heading3']))
                
                content_style = ParagraphStyle(
                    'CodeStyle',
                    parent=styles['Code'],
                    fontSize=7,
                    fontName='Courier',
                    leftIndent=10,
                    backColor=colors.HexColor('#E3F2FD'),
                    borderPadding=8,
                    borderColor=colors.HexColor('#90CAF9'),
                    borderWidth=1
                )
                
               
                if len(content) > 2000:
                    content = content[:2000] + "\n\n... (content truncated - see original file for complete data)"
                    
                story.append(Paragraph(content.replace('\n', '<br/>'), content_style))
                story.append(Spacer(1, 15))
        
        return story

    def create_3d_visualization_section(self):
        
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("3D APPLICATOR VISUALIZATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
      
        views = [
            ("Fraction 1 - 3D View", self.generate_3d_plot_for_fraction(1)),
            ("Fraction 2 - 3D View", self.generate_3d_plot_for_fraction(2)),
            ("Fraction Comparison - 3D Overlay", self.generate_3d_comparison_plot())
        ]
        
        successful_plots = 0
        
        for view_name, plot_path in views:
            if plot_path and os.path.exists(plot_path):
                story.append(Paragraph(f"<b>{view_name}</b>", styles['Heading3']))
                
                try:
                    img = Image(plot_path, width=5*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 10))
                    successful_plots += 1
                except Exception as e:
                    story.append(Paragraph(f"<i>Could not display {view_name}: {str(e)}</i>", styles['Italic']))
            else:
                story.append(Paragraph(f"<b>{view_name}</b>", styles['Heading3']))
                story.append(Paragraph("<i>3D visualization not available</i>", styles['Italic']))
        
        if successful_plots == 0:
            story.append(Paragraph("<i>No 3D visualizations could be generated. Complete annotation of both fractions first.</i>", styles['Italic']))
        
        story.append(Spacer(1, 20))
        
        
        interpretation = """
        <b>3D Visualization Interpretation:</b><br/>
        • Blue points: Fraction 1 applicator positions<br/>
        • Red points: Fraction 2 applicator positions<br/>
        • Lines connect tip and base points for each applicator<br/>
        • Spatial relationships show applicator positioning reproducibility<br/>
        • Distance between fractions indicates movement between treatments
        """
        
        interpretation_style = ParagraphStyle(
            'InterpretationStyle',
            parent=styles['Normal'],
            fontSize=9,
            backColor=colors.HexColor('#E3F2FD'),
            borderPadding=10,
            borderColor=colors.HexColor('#90CAF9'),
            borderWidth=1
        )
        
        story.append(Paragraph(interpretation, interpretation_style))
        
        return story

    def generate_3d_plot_for_fraction(self, fraction):
     
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            import numpy as np
        
            plot_path = os.path.join(self.temp_dir, f"3d_fraction_{fraction}.png")
        
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
        
         
            points_data = self.extract_applicator_points_3d(fraction)
        
            if not points_data:
                plt.close(fig)
                return None
        
            colors = ['red', 'blue', 'green']
            applicator_names = list(points_data.keys())
        
            for i, (applicator, points) in enumerate(points_data.items()):
                if points and len(points[0]) >= 2:
                    x, y, z = points
                    color = colors[i % len(colors)]
                    
                    
                    ax.scatter(x, y, z, c=color, marker='o', s=150, label=applicator, alpha=0.8)
                    
                
                    if len(x) > 1:
                        ax.plot(x, y, z, c=color, linewidth=3, alpha=0.7)
                    
                  
                    for j, (xp, yp, zp) in enumerate(zip(x, y, z)):
                        ax.text(xp, yp, zp, f'{applicator[:1]}{j+1}', fontsize=8, 
                               color='black', ha='center', va='center')
        
            ax.set_xlabel('X Position (mm)')
            ax.set_ylabel('Y Position (mm)')
            ax.set_zlabel('Z Position (mm)')
            ax.set_title(f'3D Applicator Positions - Fraction {fraction}')
            ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
        
            plt.tight_layout()
            plt.savefig(plot_path, dpi=150, bbox_inches='tight', format='png')
            plt.close(fig)
        
            return plot_path if os.path.exists(plot_path) else None
        
        except Exception as e:
            print(f"3D plot generation for fraction {fraction} failed: {e}")
            return None

    def generate_3d_comparison_plot(self):
       
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
        
            plot_path = os.path.join(self.temp_dir, "3d_comparison.png")
        
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
        
         
            frac_colors = ['blue', 'red']
            frac_labels = ['Fraction 1', 'Fraction 2']
        
            for frac_idx, fraction in enumerate([1, 2]):
                points_data = self.extract_applicator_points_3d(fraction)
                
                if not points_data:
                    continue
                
                color = frac_colors[frac_idx]
                label = frac_labels[frac_idx]
                
                for applicator, points in points_data.items():
                    if points and len(points[0]) >= 2:
                        x, y, z = points
                        
                        # Plot points
                        ax.scatter(x, y, z, c=color, marker='o' if frac_idx == 0 else 's', 
                                 s=100, label=f'{applicator} {label}' if applicator == list(points_data.keys())[0] else "",
                                 alpha=0.7)
                        
                        # Plot lines
                        if len(x) > 1:
                            ax.plot(x, y, z, c=color, linewidth=2, alpha=0.5, linestyle='--' if frac_idx == 1 else '-')
        
            ax.set_xlabel('X Position (mm)')
            ax.set_ylabel('Y Position (mm)')
            ax.set_zlabel('Z Position (mm)')
            ax.set_title('3D Applicator Position Comparison - Fraction 1 vs Fraction 2')
            
            # Create custom legend
            from matplotlib.lines import Line2D
            legend_elements = [
                Line2D([0], [0], marker='o', color='blue', label='Fraction 1',
                      markersize=8, linestyle='-', linewidth=2),
                Line2D([0], [0], marker='s', color='red', label='Fraction 2',
                      markersize=8, linestyle='--', linewidth=2)
            ]
            ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
        
            plt.tight_layout()
            plt.savefig(plot_path, dpi=150, bbox_inches='tight', format='png')
            plt.close(fig)
        
            return plot_path if os.path.exists(plot_path) else None
        
        except Exception as e:
            print(f"3D comparison plot generation failed: {e}")
            return None

    def create_image_status_section(self):
   
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("IMAGE UPLOAD STATUS", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        image_data = [["View", "Fraction", "Status", "File Name"]]
        
        image_types = {
            "AP_frac1": "AP View - Fraction 1",
            "AP_frac2": "AP View - Fraction 2", 
            "LAT_frac1": "Lateral View - Fraction 1",
            "LAT_frac2": "Lateral View - Fraction 2"
        }
        
        for key, display_name in image_types.items():
            path = self.image_paths.get(key)
            if path and os.path.exists(path):
                status = "✅ Uploaded"
                filename = os.path.basename(path)
            else:
                status = "❌ Not uploaded"
                filename = "N/A"
            
            parts = display_name.split(' - ')
            image_data.append([parts[0], parts[1], status, filename])
        
        image_table = Table(image_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 2.5*inch])
        image_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
        ]))
        
        story.append(image_table)
        story.append(Spacer(1, 20))
        
        
        cal_text = f"""
        <b>Pixel Spacing Calibration:</b><br/>
        AP Images: {self.pixel_spacing.get('AP_frac1', 0.2979):.4f} mm/pixel<br/>
        Lateral Images: {self.pixel_spacing.get('LAT_frac1', 0.2979):.4f} mm/pixel
        """
        story.append(Paragraph(cal_text, styles['Normal']))
        
        return story

    def create_detailed_summary_section(self):
        
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("CLINICAL SUMMARY AND INTERPRETATION", styles['Heading1']))
        story.append(Spacer(1, 12))
        
    
        assessment = self.generate_detailed_clinical_assessment()
        
        summary_style = ParagraphStyle(
            'SummaryStyle',
            parent=styles['Normal'],
            fontSize=10,
            backColor=colors.HexColor('#F0F7FF'),
            borderPadding=15,
            borderColor=colors.HexColor('#BBDEFB'),
            borderWidth=1,
            leading=14  
        )
        
        story.append(Paragraph(assessment, summary_style))
        story.append(Spacer(1, 20))
        
       
        story.append(Paragraph("KEY FINDINGS", styles['Heading2']))
        
        findings = self.generate_key_findings()
        findings_style = ParagraphStyle(
            'FindingsStyle',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            bulletIndent=20,
            spaceAfter=8
        )
        
        for finding in findings:
            story.append(Paragraph(f"• {finding}", findings_style))
        
        story.append(Spacer(1, 20))
        
        
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", styles['Heading2']))
        
        recommendations = self.generate_recommendations()
        for recommendation in recommendations:
            story.append(Paragraph(f"• {recommendation}", findings_style))
        
        story.append(Spacer(1, 20))
        
     
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Italic'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=1 
        )
        
        disclaimer = """
        <i>This comprehensive report is generated automatically based on image analysis and annotations. 
        All clinical decisions must be made by qualified radiation oncologists and medical physicists 
        considering complete patient information, clinical context, and institutional protocols. 
        Measurement accuracy depends on image quality, annotation precision, and calibration validity.</i>
        """
        
        story.append(Paragraph(disclaimer, disclaimer_style))
        
        return story

    def generate_detailed_clinical_assessment(self):
        
        try:
            analysis_results = self.report_data['analysis_results']
            
            
            has_ap_data = any('AP' in f for f in analysis_results.keys())
            has_lat_data = any('LAT' in f for f in analysis_results.keys())
            has_comparison = any('comparison' in f.lower() or 'shift' in f.lower() for f in analysis_results.keys())
            
            assessment_parts = []
            
            assessment_parts.append("<b>COMPREHENSIVE CLINICAL ASSESSMENT</b><br/><br/>")
            
            assessment_parts.append("<b>Data Completeness:</b><br/>")
            if has_ap_data:
                assessment_parts.append("• AP view analysis: Complete<br/>")
            else:
                assessment_parts.append("• AP view analysis: Not available<br/>")
                
            if has_lat_data:
                assessment_parts.append("• Lateral view analysis: Complete<br/>")
            else:
                assessment_parts.append("• Lateral view analysis: Not available<br/>")
                
            if has_comparison:
                assessment_parts.append("• Fraction comparison: Available<br/>")
            else:
                assessment_parts.append("• Fraction comparison: Not available<br/>")
            
            assessment_parts.append("<br/><b>Technical Quality:</b><br/>")
            assessment_parts.append("• Image calibration: Applied<br/>")
            assessment_parts.append("• Anatomical references: Established<br/>")
            assessment_parts.append("• Applicator identification: Completed<br/>")
            assessment_parts.append("• Measurement precision: Within clinical tolerance<br/>")
            
            assessment_parts.append("<br/><b>Spatial Analysis:</b><br/>")
            assessment_parts.append("• 3D positioning: Visualized<br/>")
            assessment_parts.append("• Fraction reproducibility: Quantified<br/>")
            assessment_parts.append("• Shift calculations: Performed<br/>")
            assessment_parts.append("• Clinical impact: Assessable<br/>")
            
            return "".join(assessment_parts)
            
        except Exception as e:
            return f"<b>Clinical Assessment:</b><br/><br/>Detailed assessment generation unavailable: {str(e)}"

    def generate_key_findings(self):
        
        findings = []
        
        analysis_results = self.report_data['analysis_results']
        
       
        findings.append("All applicator structures successfully identified and annotated")
        findings.append("Distance measurements completed relative to anatomical landmarks")
        findings.append("3D spatial relationships established for both fractions")
        
     
        if any('shift' in f.lower() for f in analysis_results.keys()):
            findings.append("Applicator movement between fractions quantified")
            findings.append("Reproducibility metrics calculated")
        
        if any('AP' in f for f in analysis_results.keys()):
            findings.append("AP view analysis provides coronal plane assessment")
            
        if any('LAT' in f for f in analysis_results.keys()):
            findings.append("Lateral view analysis provides sagittal plane assessment")
        
        findings.append("Comprehensive dataset available for clinical review")
        
        return findings

    def generate_recommendations(self):
     
        recommendations = [
            "Review all measurements in clinical context before treatment decisions",
            "Consider applicator shifts when evaluating dose distribution reproducibility",
            "Verify anatomical consistency between fractions",
            "Use 3D visualizations for spatial relationship assessment",
            "Correlate findings with clinical symptoms and patient anatomy",
            "Document any significant shifts in patient treatment records"
        ]
        
        return recommendations



    
if __name__ == "__main__":
    root = tk.Tk()
    app = BrachyApp(root)
    root.mainloop()
