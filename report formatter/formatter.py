import os
import sys
import csv
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill,\
                            Font, GradientFill, Alignment

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
    # format first row font
    for c in range(first_cell.col_idx, last_cell.col_idx+1):
        cell = ws.cell(row = first_cell.row, column = c)
        ft = Font(name='Calibri', bold=True)
        al = Alignment(horizontal="center", vertical="center")
        cell.font = ft
        cell.alignment = al
        
    # colouring rows after first row
    for r in range(first_cell.row, last_cell.row+1):
        for c in range(first_cell.col_idx, last_cell.col_idx+1): 
            # colour odd numbered rows
            if r % 2 == 1:
                cell = ws.cell(row = r, column = c)
                fill = PatternFill('solid', fgColor="DDDDDD")
                cell.fill = fill


                
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
    
    