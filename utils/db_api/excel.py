from openpyxl import load_workbook


def send_excel(table_name, list_data):
    fn = 'table.xlsx'
    wb = load_workbook(fn)
    ws = wb[table_name]
    ws.append(list_data)
    wb.save(fn)
    wb.close()
