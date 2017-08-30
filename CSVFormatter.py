import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class CSVFormatter(tk.Frame):
    help_txt = ""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = "CSV Formatter"
        self.cont = controller
        self.draw()
        
    def draw(self):
        s = ttk.Style()
        s.configure('Kim.TButton', foreground='maroon')
        
        browse_button = ttk.Button(self, text="Browse to CSV file", command=self.browse)
        process_button = ttk.Button(self, text="Load")
        Menu_button = ttk.Button(self, text="Back to Menu", style='Kim.TButton', command=lambda:self.cont.show_frame("MainMenu")) 
        self.path = ttk.Entry(self)
        tooltip_box = ttk.LabelFrame(self, text="Tooltip")
        tooltip_txt = ttk.Label(tooltip_box, text=self.help_txt)
        
        tooltip_txt.grid(row=0, column=0)
        browse_button.grid(row=0, sticky="nsew",padx=20, pady=10)
        self.path.grid(row=0, column=1, columnspan=10, sticky="nsew",padx=20, pady=10)
        process_button.grid(row=1, sticky="nsew",padx=20, pady=10)
        Menu_button.grid(row=2, sticky="nsew",padx=20, pady=10)
        tooltip_box.grid(row=2, column=1, columnspan=10 ,padx=20, pady=10)
        
    def browse(self):
        input_file_path = filedialog.askopenfilename(title='Choose a CSV file', filetypes = [("CSV Files",".csv")])
        self.path.delete(0, tk.END)
        self.path.insert(0, input_file_path)