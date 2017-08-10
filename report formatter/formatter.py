import os
import sys
import csv
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

    
# Taken from documentation   
def style_range(ws, first_cell, last_cell):
    # colouring rows after first row
    for r in range(first_cell.row, last_cell.row+1):
        for c in range(first_cell.col_idx, last_cell.col_idx+1): 
            # colour odd numbered rows
            if r == first_cell.row:
                ft = Font(name='Courier', bold=True)
            else:
                ft = Font(name='Courier')
            cell = ws.cell(row = r, column = c)
            al = Alignment(horizontal="center", vertical="center")
            cell.alignment = al
            cell.font = ft
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

                
if __name__ == "__main__":
    # input csv file location data
    tmp_path = os.path.abspath("../tmp")
    unformatted_file = "Report for open studies.csv"
    input_path = os.path.join(tmp_path, unformatted_file)
    
    # output xlsx file location data
    output_path = "{}_formatted.xlsx".format(input_path[:-4])
    
    # open and convert the csv to xlsx 
    wb, ws = csv_to_xlsx(input_path)
    
    # the actual formatting
    first_cell = ws.cell(row=1, column=1)
    last_cell = ws.cell(row=ws.max_row, column=ws.max_column)
    style_range(ws, first_cell, last_cell)
    
    # save formatted file
    wb.save(output_path)
    
    