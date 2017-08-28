import tkinter as tk
from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedStyle
import sys

class REDCapTools(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('REDCapTools')
        self.resizable(width=False, height=False)
        self.set_styles()
        menu = MainMenuFrame(self)

    def set_styles(self):
        self.style = ThemedStyle(self)
        self.style.theme_use("arc")
        
    def quit(self, event=None):
        sys.exit()


        
class MainMenuFrame():
    def __init__(self, parent):
        self.parent = parent
        self.btn_frame = ttk.Frame(parent)
        self.tooltip_frame = ttk.Frame(parent)
        self.btn_frame.pack(side=tk.LEFT)
        self.tooltip_frame.pack(side=tk.RIGHT)
        self.draw()
    
    def draw(self):
        # drawing the buttons
        charts_btn = ttk.Button(self.btn_frame, text="Charts", command = self.p)
        format_btn = ttk.Button(self.btn_frame, text="Formatter",command = self.p)
        monthly_btn = ttk.Button(self.btn_frame, text="Monthly Enrollment", command = self.p)
        
        btn_padding = {
            "padx": 20,
            "pady": 10,
            "sticky": "ew"
            }
        charts_btn.grid(row=0, **btn_padding)
        format_btn.grid(row=1, **btn_padding)
        monthly_btn.grid(row=2, **btn_padding)
        
        # drawing the tooltip box
        app_txt = ""
        sep = ttk.Separator(self.btn_frame,orient=tk.VERTICAL)
        grid_row_size = self.btn_frame.grid_size()[1]
        sep.grid(row=0, column=1, rowspan=grid_row_size, sticky="ns",padx=5, pady=10)
        
        tooltip_box = ttk.LabelFrame(self.tooltip_frame, text="Tooltip")
        self.tooltip_frame.grid_columnconfigure(0, weight=3)
        self.tooltip_frame.rowconfigure(0, weight=30)
        tooltip_box.grid(row=0, rowspan=grid_row_size, sticky="nsew", padx=5, pady=10)
        tooltip_txt = ttk.Label(tooltip_box, text=app_txt)
        tooltip_txt.grid(row=0, column=0)
    
    def p(self):
        pass
        
if __name__ == "__main__":
    app = REDCapTools()
    app.mainloop()