import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import os
from tkinter import messagebox

class MonthlyAssessment(tk.Frame):
    help_txt = ""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = "Monthly Assessment"
        self.cont = controller
        self.draw()
        
    def draw(self):
        s = ttk.Style()
        s.configure('Kim.TButton', foreground='maroon')
        
        browse_button = ttk.Button(self, text="Browse to CSV file", command=self.browse)
        process_button = ttk.Button(self, text="Load File", command=self.load_csv)
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
        
    def load_csv(self):
        settings = self.cont.frames["MonthlyAssessSettings"]
        try:
            settings.draw(self.path.get())
            self.cont.show_frame("MonthlyAssessSettings")
        except FileNotFoundError:
            tk.messagebox.showinfo("File not found", "Please use the Browse button to select a valid .csv file or directly type the correct path in textbox before attempting to Load the sheet.")
            return
        
        
class MonthlyAssessSettings(tk.Frame):
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
        
        generate_btn = ttk.Button(self.top_frame, text="Generate CSV File")
        generate_btn.bind("<Button-1>", self.generate)
        Menu_button = ttk.Button(self.top_frame, text="Back to Monthly Assessment", style='Kim.TButton', command=self.back)
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
            labels = [col[0] for col in self.columns]
            self.id_var = tk.StringVar(self.middle_frame)
            self.study_id_col = ttk.OptionMenu(self.middle_frame, self.id_var, labels[0], *labels)
            self.study_id_col.grid(row=0, columnspan=3, sticky="nsew", pady = 20)
            
            self.add_row()
    
    def add_row(self):
        labels = [col[0] for col in self.columns]
        
        sep = ttk.Separator(self.middle_frame,orient=tk.HORIZONTAL)
        
        curr_en_var = tk.StringVar(self.middle_frame)
        last_en_var = tk.StringVar(self.middle_frame)
        
        L1 = ttk.Label(self.middle_frame, text = "Current Enrollemnt Population")
        L2 = ttk.Label(self.middle_frame, text = "Previous Enrollemnt Population")
        L3 = ttk.Label(self.middle_frame, text = "Current Month Enrollment variable name:")
        
        init_en_dropdown =  ttk.OptionMenu(self.middle_frame, curr_en_var, labels[0], *labels)
        init_en_dropdown.var = curr_en_var
        final_en_dropdown =  ttk.OptionMenu(self.middle_frame,last_en_var, labels[0], *labels)
        final_en_dropdown.var = last_en_var
        new_en = ttk.Entry(self.middle_frame, justify=tk.CENTER)
        
        switchbtn = ttk.Button(self.middle_frame, text='\u2194')
        switchbtn.bind("<Button-1>", self.swap)
        switchbtn.var1 = curr_en_var
        switchbtn.var2 = last_en_var
        
        r = 1 + 4*len(self.widgets)
        sep.grid(row=r, columnspan=3, sticky="nsew", pady = 10)
        L1.grid(row=r+1, column=0, sticky="nsew", padx=5)
        L2.grid(row=r+1, column=2, sticky="nsew", padx=5)
        init_en_dropdown.grid(row=r+2, column=0, sticky="nsew", pady=10, padx=5)
        switchbtn.grid(row=r+2, column=1, pady=10, padx=5)
        final_en_dropdown.grid(row=r+2, column=2, sticky="nsew", pady=10, padx=5)
        L3.grid(row=r+3, column=0, sticky="nsew", pady=10,padx=5)
        new_en.grid(row=r+3,column=1, columnspan=2, sticky="nsew", pady=10, padx=5)
        
        widget_group = (sep,init_en_dropdown,final_en_dropdown, new_en,switchbtn)
        self.widgets.append(widget_group)
    
    def remove_row(self):
        if len(self.widgets) is 1:
            return
        for w in self.widgets[-1]:
            w.destroy()
        del self.widgets[-1]
        
    def generate(self, event):
        cols = self.columns
        new_cols = list()
        new_cols.append(cols[0])
        warning_flag=False
        for group in self.widgets:
            curr = group[1].var.get()
            prev = group[2].var.get()
            new = group[3].get()
            if new.isspace() or new=="":
                tk.messagebox.showinfo("Empty Entry Name","All new entry name fields must be non empty")
                return
            for col in cols:
                if col[0] == curr:
                    curr_list = col[:]
                    break
            for col in cols:
                if col[0] == prev:
                    prev_list = col[:]
                    break
            new_list = [new]        
            for r in range(1,len(curr_list)):
                if curr_list[r]=="":
                    curr_list[r]=0
                if prev_list[r]=="":
                    prev_list[r]=0
                if not curr_list[r].isnumeric():
                    tk.messagebox.showinfo("Invalid Entry Error","Non numeric value exists under \"{}\" row {}".format(curr_list[0], r+1))
                    return
                if not prev_list[r].isnumeric():
                    tk.messagebox.showinfo("Invalid Entry Error","Non numeric value exists under \"{}\" row {}".format(prev_list[0], +1))
                    return
                diff = self.to_int(curr_list[r])-self.to_int(prev_list[r])
                if diff<0:
                    warning_flag=True
                new_list.append(diff)
            curr_list[0] = prev_list[0]
            new_cols.append(curr_list)
            new_cols.append(new_list)
        rm_ext_path = os.path.splitext(self.path)[0]
        save_path = "{}_generated_MA.csv".format(rm_ext_path)
        with open(save_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in zip(*new_cols):
                writer.writerow(line)
        if warning_flag == True:
            messagebox.showinfo("WARNING", "WARNING: Negative population generated! Please check the output file.")
        messagebox.showinfo("File Created","File created at {}".format(save_path))
        self.back()

    def to_int(self, val):
        return int(val)
        
        
    def back(self):
        for widget_group in self.widgets:
            for w in widget_group:
                w.destroy()
        self.study_id_col.destroy()
        self.columns = None
        self.widgets = []
        self.path = ""
        self.cont.show_frame("MonthlyAssessment")
    
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
        