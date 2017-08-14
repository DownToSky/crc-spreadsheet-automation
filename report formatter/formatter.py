import os
import sys
import time
import csv
from tkinter import Tk, Label, Button, filedialog 
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill,\
                            Font, GradientFill, Alignment
from openpyxl.worksheet.dimensions import ColumnDimension
    


    
# this useful function taken from konrad
# at "https://gist.github.com/konrad/4154786"
def _convert_to_number(cell):
    if cell.isnumeric():
        return int(cell)
    try:
        return float(cell)
    except ValueError:
        return cell
        
        
        
        
def csv_to_xlsx(input_path):
    wb = Workbook()
    worksheet = wb.active
    with open(input_path) as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            worksheet.append([_convert_to_number(cell) for cell in row])
    #assuming it is a valid ".csv" ....    
    return (wb, worksheet)
    
    
    
    
def set_print_properties(ws, first_cell, last_cell):
    #setting up the print settings
    ws.oddHeader.center.text = "&F"
    ws.oddHeader.center.size = 14
    ws.oddHeader.center.font = "Tahoma,Bold"
    
    ws.oddFooter.right.text = "Page &[Page] of &N"
    ws.oddFooter.right.size = 12
    ws.oddFooter.right.font = "Tahoma"
    
    ws.oddFooter.left.text = "&[{}".format(time.strftime("%m/%d/%Y")) # THIS IS SOME FReAKING MAGIC JESUS BUT IT WORKS SCREW YOUR FARMATTING OPENPYXL NOR YOUR STUPID &D !!:(
    ws.oddFooter.left.size = 12
    ws.oddFooter.left.font = "Tahoma"
    
    ws.print_options.horizontalCentered = True
    ws.print_area = "{}:{}".format(first_cell.coordinate,
                                    last_cell.coordinate)

    
    
    
# Taken from documentation   
def style_range(ws, first_cell, last_cell):
    # colouring rows after first row
    for r in range(first_cell.row, last_cell.row+1):
        for c in range(first_cell.col_idx, last_cell.col_idx+1): 
            # colour odd numbered rows
            if r == first_cell.row:
                ft = Font(name='Tahoma', bold=True)
            else:
                ft = Font(name='Tahoma')
            border = Border(left=Side(border_style="thin",
                            color='FF000000'),
                    right=Side(border_style="thin",
                            color='FF000000'),
                    top=Side(border_style="thin",
                            color='FF000000'),
                    bottom=Side(border_style="thin"))
            cell = ws.cell(row = r, column = c)
            if isinstance(cell.value, str):
                al = Alignment(wrapText=True, horizontal="center", vertical="center")
            else:
                al = Alignment(wrapText=True, horizontal="right", vertical="center")
            cell.alignment = al
            cell.font = ft
            cell.border = border
            if r % 2 == 1:
                fill = PatternFill('solid', fgColor="DDDDDD")
                cell.fill = fill
                
    # fit text to column
    column_widths = []
    for row in ws:
        for i, cell in enumerate(row):
            if len(column_widths) > i:
                if len(str(cell.value)) > column_widths[i]:
                    column_widths[i] = len(str(cell.value))
            else:
                column_widths.append(len(str(cell.value)))

    for i, column_width in enumerate(column_widths):
        ws.column_dimensions[ws.cell(row=1, column=i+1).column].width = column_width

        
        
           
def format():
    # input csv file location data
    file_base_name = os.path.basename(input_file_path)
    
    # output xlsx file location data
    output_file_path = "{}_formatted.xlsx".format(input_file_path[:-4])
    
    # open and convert the csv to xlsx 
    wb, ws = csv_to_xlsx(input_file_path)
    
    # the actual formatting
    first_cell = ws.cell(row=1, column=1)
    last_cell = ws.cell(row=ws.max_row, column=ws.max_column)
    style_range(ws, first_cell, last_cell)
    
    set_print_properties(ws, first_cell, last_cell)
    
    # save formatted file
    wb.save(output_file_path)



input_file_path = None
def load_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename(title='Choose a file', filetypes = [("CSV Files",".csv")])
    pathlabel.config(text=input_file_path)
    
# tkFileDialog.askdirectory    
    
if __name__ == "__main__":
    root = Tk()
    root.title("CSV REDCap report formatter")
    label = Label(root, text=":D")
    label.pack()
    browse_button = Button(root, text="Browse", command=load_file)
    format_button = Button(root, text='Format', font = "Verdana 30 bold", width=15, command=format)
    exit_button = Button(root, text='Exit', font = "Verdana 20", width=15, command=root.destroy)
    pathlabel = Label(root)
    pathlabel.pack()
    browse_button.pack()
    format_button.pack()
    exit_button.pack()
    root.mainloop()