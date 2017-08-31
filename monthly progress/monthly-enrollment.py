import os
import csv
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def load_file():
    input_file_path = filedialog.askopenfilename(title='Choose a CSV file', filetypes = [("CSV Files",".csv")])
    path.delete(0, END)
    path.insert(0, input_file_path)

def generate():
    if first_column_is_ID.get() == False:
        messagebox.showinfo("Invalid Format", "First column needs to contain unique IDs for each study.")
        return
    try:
        f = open( path.get())
        columns = process_csv(f)
    except FileNotFoundError:
        messagebox.showinfo("File not found", "Please use the Browse button to select a valid .csv file or directly type the path in textbox before attempting to generate the sheet.")
        return
    except ValueError as e:
        messagebox.showinfo("Invalid Cell Value",str(e))
        f.close()
        return
    #try:
    if len(columns) %2 == 0:
        messagebox.showinfo("Warning!","Warning: Could not match the last column with any other given colmun!")
        
    global generate_button
    generate_button =    Button(topWindow, text='Generate', font = "Verdana 12 bold")
    generate_button.bind("<Button-1>",save_new_csv)
    generate_button.grid(row=0, sticky="nsew")
    global widget_list
    widget_list = list()
    labels = [col[0] for n,col in enumerate(columns) if n!=0]
    generate_button.widg_list = widget_list
    generate_button.columns_list = columns
    generate_button.save_path = "{}_generated.csv".format(path.get()[:-4])
    r = -3
    for c in range(1, len(columns),2):
        r+=4
        if c==len(columns)-1:
            continue
        sep = ttk.Separator(topWindow,orient=HORIZONTAL)
        L1 = Label(topWindow, text = "Current Enrollemnt Population")
        L2 = Label(topWindow, text = "Previous Enrollemnt Population")
        L3 = Label(topWindow, text = "New enrollemnt variable name:")
        curr_en_var=StringVar(topWindow)
        last_en_var=StringVar(topWindow)
        curr_en_var.set(columns[c][0])
        last_en_var.set(columns[c+1][0])
        curr_en = OptionMenu(topWindow, curr_en_var, *labels)
        curr_en.var = curr_en_var
        last_en = OptionMenu(topWindow, last_en_var, *labels)
        last_en.var = last_en_var
        switchbtn = Button(topWindow, text='switch', font = "Verdana 7",bg="grey")
        switchbtn.bind("<Button-1>", swap)
        switchbtn.var1 = curr_en_var
        switchbtn.var2 = last_en_var
        new_en = Entry(topWindow,justify=CENTER)
        sep.grid(row=r, columnspan=3, sticky="nsew",pady = 10)
        L1.grid(row=r+1,column=0, sticky="ew")
        L2.grid(row=r+1,column=2, sticky="ew")
        L3.grid(row=r+3,column=0,sticky="nsew")
        curr_en.grid(row=r+2,column=0, sticky="nsew")
        switchbtn.grid(row=r+2,column=1, sticky="nsew")
        last_en.grid(row=r+2,column=2, sticky="nsew")
        new_en.grid(row=r+3,column=1, columnspan=2, sticky="nsew")
        widget_list.append([curr_en,last_en,new_en,sep,L1,L2,L3,switchbtn])
    mainWindow.withdraw()
    topWindow.deiconify()
    print(columns)
    print(labels)
    #except:
    #    f.close()
    #    return

def swap(event):
    v1 = event.widget.var1
    v2 = event.widget.var2
    tmp = v1.get()
    v1.set(v2.get())
    v2.set(tmp)
    
def save_new_csv(event):
    w = event.widget
    cols = w.columns_list
    new_cols = list()
    new_cols.append(cols[0])
    warning_flag=False
    for group in w.widg_list:
        curr = group[0].var.get()
        prev = group[1].var.get()
        new = group[2].get()
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
            diff = to_int(curr_list[r])-to_int(prev_list[r])
            if diff<0:
                warning_flag=True
            new_list.append(diff)
        curr_list[0] = prev_list[0]
        new_cols.append(curr_list)
        new_cols.append(new_list)
    if warning_flag == True:
        messagebox.showinfo("WARNING", "WARNING: Negative population generated!")
    with open(generate_button.save_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in zip(*new_cols):
            writer.writerow(line)
    messagebox.showinfo("File Created","File created at {}".format(generate_button.save_path))
    closing_generate()

def to_int(val):
    if val == "":
        return 0
    else:
        return int(val)
    
def process_csv(csv_file):
    columns = list()
    for rownum, row in enumerate(csv.reader(csv_file, delimiter=",")):
        for colnum, cell in enumerate(row):
            if rownum > 0:
                columns[colnum].append(cell)
                if cell != "" and not cell.isnumeric():
                    raise ValueError("Invalid non numeric value in cell positioned at row {} and column {}.".format(rownum, colnum))
            else:
                columns.append([cell])
    return columns
                
def closing_generate():
    for widget_group in widget_list:
        for widget in widget_group:
            widget.destroy()
    generate_button.destroy()
    mainWindow.deiconify()
    topWindow.withdraw()
    
if __name__ == "__main__":
    mainWindow = Tk()
    mainWindow.title("CSV Monthly Progress Calculator")
    mainWindow.resizable(width=False, height=False)
    mainWindow.geometry("800x64")
    topWindow = Toplevel(mainWindow)
    topWindow.protocol("WM_DELETE_WINDOW", closing_generate)
    topWindow.title("Processing")
    topWindow.withdraw()
    
    first_column_is_ID = IntVar()
    first_column_is_ID.set(1)
    browse_button = Button(mainWindow, text="Browse", font="Verdana 12 bold", command=load_file)
    Process_button = Button(mainWindow, text="Process", font="Verdana 12 bold", command=generate)   
    ID_CheckB = Checkbutton(mainWindow,text="First column in the file is an ID column", variable=first_column_is_ID)
    path = Entry(mainWindow)
    browse_button.grid(row=0, sticky="nsew")
    path.grid(row=0, column=1, columnspan=10, sticky="nsew")
    Process_button.grid(row=1, sticky="nsew")
    ID_CheckB.grid(row=1, column=1)
    mainWindow.grid_columnconfigure(1, weight=1)
    
    
    mainWindow.mainloop()