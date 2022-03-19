
from oauth2client.service_account import ServiceAccountCredentials as sac
import gspread, os, pandas as pd

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# path = './Clouix/Spreadsheets'
jfile = 'ideationology-lab-b60654e44e37.json'
# jfile = os.path.join(path, jfile)

creds = sac.from_json_keyfile_name(jfile, scope)
client = gspread.authorize(creds)

url = 'https://docs.google.com/spreadsheets/d/1aJqW6A_rVdK7bfeX2Lb8O22xztbDFZw29yLwSc3ekUE/edit#gid=0'
sheet = client.open_by_url(url)


def mark(attend, sheet_id, top = ['Purchased Date', 'Objects', 'Cost']):
    import datetime
    dt = str(datetime.datetime.now()).split()

    attend.insert(0, ' / '.join(dt))
    worksheet_up = sheet.get_worksheet_by_id(sheet_id)

    worksheet_up.update('A1', [top])
    worksheet_up.format("A1:C1", {
        "horizontalAlignment": "CENTER",
        "textFormat": {
          "foregroundColor": {
            "red": 1.0,
            "green": 0.0,
            "blue": 0.0
          },
          "fontSize": 10,
          "bold": True
        }
    })

    sz = len(worksheet_up.col_values(1))+1
    worksheet_up.update(f'A{sz}', [attend])

    if top == ['Purchased Date', 'Objects', 'Cost']:
        worksheet_up.format(f'B{sz}', {"textFormat": {"bold": False}})
        worksheet_up.format(f'C{sz}', {"textFormat": {"bold": False}})

        worksheet_up.update(f'B{sz+1}', 'Total Cost')
        worksheet_up.format(f'B{sz+1}', {"textFormat": {"bold": True}})

        worksheet_up.update(f'C{sz+1}', f"=SUM(C2:C{sz})", raw=False)
        worksheet_up.format(f'C{sz+1}', {"textFormat": {"bold": True}}) 
    
    body = {
        "requests": [
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,  # Please set the column index.
                        "endIndex": 3  # Please set the column index.
                    }
                }
            }
        ]
    }
    sheet.batch_update(body) 


def add_cust(cust):
    try:
        worksheet = sheet.add_worksheet(title = cust, rows="100", cols="20")
        attend = [cust, worksheet.id]
        top = ['Joining Date', 'Customer Name', 'Worksheet ID']
        mark(attend, 0, top)
        return worksheet.id
    
    except Exception as e:
        return e


def fetch(sheet_id):
    sheet_instance = sheet.get_worksheet_by_id(sheet_id)
    records_data = sheet_instance.get_all_records()
    df = pd.DataFrame(records_data) 
    df.index += 1
    return df


# ------------------------------------------

# cust = input('Enter Your Name : ') 
# sheet_id = add_cust(cust) 
# print(sheet_id)


# saman = input('Enter Saman : ')
# cost = float(input('Enter Cost : '))
# attend = [saman, cost] 
# sheet_id = int(input('Enter Sheet ID : '))
# mark(attend, sheet_id)


# sheet_id = int(input('Enter Sheet ID : '))
# df = fetch(sheet_id)
# print(df)