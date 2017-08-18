import os
import csv
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
        messagebox.showinfo("Warning!","Warning: Could not match the last column with any other give colmun!")
        
    global generate_button
    generate_button =    Button(topWindow, text='Generate', font = "Verdana 12 bold", command=save_new_csv)
    generate_button.grid(row=0)
    global widget_list
    widget_list = list()
    labels = [col[0] for col in columns]
    for c in range(1, len(columns),2):
        if c==0 or c==len(columns)-1:
            continue
        curr_en_var=StringVar(topWindow)
        last_en_var=StringVar(topWindow)
        curr_en_var.set(columns[c][0])
        last_en_var.set(columns[c+1][0])
        curr_en = OptionMenu(topWindow, curr_en_var, *labels)
        last_en = OptionMenu(topWindow, last_en_var, *labels)
        switchbtn = Button(topWindow, text='switch', font = "Verdana 7", command=switch_options)
        new_en = Entry(topWindow)
        curr_en.grid(row=c,column=0, sticky="nsew")
        switchbtn.grid(row=c,column=1, sticky="nsew")
        last_en.grid(row=c,column=2, sticky="nsew")
        new_en.grid(row=c+1,column=0, columnspan=3, sticky="nsew")
        widget_list.append([curr_en,switchbtn,last_en,new_en])
    mainWindow.withdraw()
    topWindow.deiconify()
    print(columns)
    print(labels)
    #except:
    #    f.close()
    #    return

def switch_options():
    pass
    
def save_new_csv():
    closing_generate()
    
def process_csv(csv_file):
    columns = list()
    for rownum, row in enumerate(csv.reader(csv_file, delimiter=",")):
        for colnum, cell in enumerate(row):
            if rownum > 0:
                columns[colnum].append(cell)
                if not cell.isnumeric():
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
    mainWindow. resizable(width=False, height=False)
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