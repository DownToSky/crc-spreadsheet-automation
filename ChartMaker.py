import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import csv
import os


class ChartMaker(tk.Frame):
    help_txt = ""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = "Chart Maker"
        self.cont = controller
        self.draw()
        
    def draw(self):
        s = ttk.Style()
        s.configure('Kim.TButton', foreground='maroon')
        
        first_column_is_ID = tk.IntVar()
        first_column_is_ID.set(1)
        browse_button = ttk.Button(self, text="Browse to CSV file", command=self.browse)
        process_button = ttk.Button(self, text="Load File", command=self.load_csv)
        Menu_button = ttk.Button(self, text="Back to Menu", style='Kim.TButton', command=lambda:self.cont.show_frame("MainMenu")) 
        ID_CheckB = ttk.Checkbutton(self,text="First column in the file is an ID column", variable=first_column_is_ID)
        self.path = ttk.Entry(self)
        tooltip_box = ttk.LabelFrame(self, text="Tooltip")
        tooltip_txt = ttk.Label(tooltip_box, text=self.help_txt)
        
        tooltip_txt.grid(row=0, column=0)
        browse_button.grid(row=0, sticky="nsew",padx=20, pady=10)
        self.path.grid(row=0, column=1, columnspan=10, sticky="nsew",padx=20, pady=10)
        process_button.grid(row=1, sticky="nsew",padx=20, pady=10)
        Menu_button.grid(row=2, sticky="nsew",padx=20, pady=10)
        ID_CheckB.grid(row=1, column=1,padx=20, pady=10)
        tooltip_box.grid(row=2, column=1, columnspan=10 ,padx=20, pady=10)
        
    def load_csv(self):
        settings = self.cont.frames["ChartMakerSettings"]
        settings.draw(self.path.get())
        self.cont.show_frame("ChartMakerSettings")
        
    def browse(self):
        input_file_path = filedialog.askopenfilename(title='Choose a CSV file', filetypes = [("CSV Files",".csv")])
        self.path.delete(0, tk.END)
        self.path.insert(0, input_file_path)
        
        
class ChartMakerSettings(tk.Frame):
    help_txt = ""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.top_frame = tk.Frame(self)
        self.middle_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.top_frame.grid(row=0)
        self.middle_frame.grid(row=1)
        self.bottom_frame.grid(row=2)
        self.title = "Pre-generation Settings"
        self.cont = controller
        self.columns = None
        self.widgets = []
        self.draw()
        
    def draw(self, csv_path=None):
        s = ttk.Style()
        s.configure('Kim.TButton', foreground='maroon')
        t = ttk.Style()
        t.configure('RB.TButton', foreground='royal blue')
        
        generate_btn = ttk.Button(self.top_frame, text="Generate Charts", command=self.generate)
        Menu_button = ttk.Button(self.top_frame, text="Back to Chart Maker", style='Kim.TButton', command=self.back)
        tooltip_box = ttk.LabelFrame(self.top_frame, text="Tooltip")
        tooltip_txt = ttk.Label(tooltip_box, text=self.help_txt)
        
        tooltip_txt.grid(row=0, column=0)
        generate_btn.grid(row=0, sticky="nsew",padx=20, pady=10)
        Menu_button.grid(row=1, sticky="nsew",padx=20, pady=10)
        tooltip_box.grid(row=0, column=1 ,padx=20, pady=10)
        
        add_btn = ttk.Button(self.bottom_frame,style='RB.TButton', text="Add", command=self.add_row)
        add_btn.grid(row=0, sticky="nsew",padx=20, pady=10)
        remove_btn = ttk.Button(self.bottom_frame,style='Kim.TButton', text="Remove", command=self.remove_row)
        remove_btn.grid(row=0, column=1, sticky="nsew",padx=20, pady=10)
        
        if csv_path!=None:
            self.path = csv_path
            self.process_csv(csv_path)
            self.add_row()
    
    def add_row(self):
        labels = [col[0] for n,col in enumerate(self.columns) if n!=0]
        
        sep = ttk.Separator(self.middle_frame,orient=tk.HORIZONTAL)
        
        init_date = tk.StringVar(self.middle_frame)
        final_date = tk.StringVar(self.middle_frame)
        
        init_date_dropdown =  ttk.OptionMenu(self.middle_frame, init_date, labels[0], *labels)
        final_date_dropdown =  ttk.OptionMenu(self.middle_frame,final_date, labels[0], *labels)
        
        switchbtn = ttk.Button(self.middle_frame, text='\u2194')
        switchbtn.bind("<Button-1>", self.swap)
        switchbtn.var1 = init_date
        switchbtn.var2 = final_date
        
        r = 2*len(self.widgets)
        sep.grid(row=r, columnspan=3, sticky="nsew", pady = 10)
        init_date_dropdown.grid(row=r+1, column=0, sticky="nsew", pady=10, padx=5)
        switchbtn.grid(row=r+1, column=1, pady=10, padx=5)
        final_date_dropdown.grid(row=r+1, column=2, sticky="nsew", pady=10, padx=5)
        
        widget_group = (sep,init_date_dropdown,final_date_dropdown,switchbtn)
        self.widgets.append(widget_group)
    
    def remove_row(self):
        if len(self.widgets) is 1:
            return
        for w in self.widgets[-1]:
            w.destroy()
        del self.widgets[-1]
    
    def generate(self):
        labels = [col[0] for n,col in enumerate(self.columns)]  
        dir_path = os.path.dirname(self.path)
        basename = os.path.basename(self.path)
        chart_output_dir = os.path.splitext(basename)[0]
        chart_output_path = os.path.join(dir_path, chart_output_dir)
        
        if not os.path.exists(chart_output_path):
            os.makedirs(chart_output_path)
            
        columns = self.columns
        for widget_group in self.widgets:
            ini_col_name = widget_group[3].var1.get()
            end_col_name = widget_group[3].var2.get()
            
            ini_index = labels.index(ini_col_name)
            end_index = labels.index(end_col_name)
            x_labels = labels[ini_index:end_index+1]
            
            row_len = len(columns[ini_index])
            for r in range(1,row_len):
                y_labels = [int(dates[r]) for dates in columns[ini_index:end_index+1]]
                
                file_name = "{}_{}_{}_{}.png".format(x_labels[0], y_labels[0],ini_index,r)
                x = [i for i in range(0,len(x_labels))]
                plt.xticks(x, x_labels)
                plt.plot(x, y_labels)
                
                file_path = os.path.join(chart_output_path, file_name)
                plt.savefig(file_path)
                plt.gcf().clear()
    
    def back(self):
        for widget_group in self.widgets:
            for w in widget_group:
                w.destroy()
        self.columns = None
        self.widgets = []
        self.path = ""
        self.cont.show_frame("ChartMaker")
    
    def swap(self, event):
        v1 = event.widget.var1
        v2 = event.widget.var2
        tmp = v1.get()
        v1.set(v2.get())
        v2.set(tmp)
    
    def process_csv(self, path):
        c = list()
        csv_file = open(path)
        for rownum, row in enumerate(csv.reader(csv_file, delimiter=",")):
            for colnum, cell in enumerate(row):
                if rownum > 0:
                    c[colnum].append(cell)
                else:
                    c.append([cell])
        self.columns = c
        csv_file.close()