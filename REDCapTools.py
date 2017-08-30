import tkinter as tk
from ChartMaker import ChartMaker
from MonthlyAssessment import MonthlyAssessment
from CSVFormatter import CSVFormatter
from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedStyle
import sys

class REDCapTools(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack()
        
        self.title('REDCapTools Menu')
        self.resizable(width=False, height=False)
        self.set_styles()
        self.frames = {
            "MainMenu": MainMenu(container, self),
            "ChartMaker": ChartMaker(container, self),
            "MonthlyAssessment": MonthlyAssessment(container, self),
            "CSVFormatter": CSVFormatter(container, self),
        }
        for name, ins in self.frames.items():
            ins.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        self.title(frame.title)
        frame.tkraise()
    
    def set_styles(self):
        self.style = ThemedStyle(self)
        self.style.theme_use("arc")
        
    def quit(self, event=None):
        sys.exit()


        
class MainMenu(tk.Frame):
    welcome_txt = "Welcome to Clinical Research Center REDCap tools program. Hover over a tool button to see its description.\n"
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = 'REDCapTools Menu'
        self.cont = controller
        self.parent = parent
        self.draw()
    
    def draw(self):
        # drawing the buttons
        charts_btn = ttk.Button(self, text="Chart Maker", command=lambda:self.cont.show_frame("ChartMaker"))
        charts_btn.bind('<Enter>', self.mouseover_charts)
        charts_btn.bind('<Leave>', self.leave_button)
        
        format_btn = ttk.Button(self, text="CSV Formatter",command=lambda:self.cont.show_frame("CSVFormatter"))
        format_btn.bind('<Enter>', self.mouseover_formatter)
        format_btn.bind('<Leave>', self.leave_button)
        
        monthly_btn = ttk.Button(self, text="Monthly Assessment", command=lambda:self.cont.show_frame("MonthlyAssessment"))
        monthly_btn.bind('<Enter>', self.mouseover_monthly)
        monthly_btn.bind('<Leave>', self.leave_button)
        
        btn_padding = {
            "padx": 20,
            "pady": 10,
            "sticky": "ew"
            }
        charts_btn.grid(row=0, **btn_padding)
        format_btn.grid(row=1, **btn_padding)
        monthly_btn.grid(row=2, **btn_padding)
        
        # drawing the tooltip box
        sep = ttk.Separator(self,orient=tk.VERTICAL)
        grid_row_size = self.grid_size()[1]
        sep.grid(row=0, column=1, rowspan=grid_row_size, sticky="ns",padx=5, pady=10)
        
        tooltip_box = ttk.LabelFrame(self, text="Tooltip")
        canvas = tk.Canvas(tooltip_box)
        tooltip_txt = ttk.Label(canvas, text=self.welcome_txt)
        scroller = ttk.Scrollbar(canvas, orient=tk.VERTICAL,command=canvas.yview)
        canvas.configure(yscrollcommand=scroller.set)
        txtframe = ttk.Frame(canvas)

        
        tooltip_box.grid(row=0, column=2, rowspan=grid_row_size, sticky="nsew", padx=10, pady=10)
        self.grid_columnconfigure(2, weight=9)
        canvas.pack(fill="both", expand=False)
        tooltip_txt.pack(side=tk.LEFT, anchor="nw")
        scroller.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tt_text = tooltip_txt
    
    def mouseover_charts(self,event):
        txt = "charts"
        self.tt_text.configure(text=txt)
        
    def mouseover_formatter(self,event):
        txt = "formatter"
        self.tt_text.configure(text=txt)
        
    def mouseover_monthly(self,event):
        txt = "monthly"
        self.tt_text.configure(text=txt)
    
    def leave_button(self,event):
        txt = "charts"
        self.tt_text.configure(text=self.welcome_txt)
        
    
        
if __name__ == "__main__":
    app = REDCapTools()
    app.mainloop()