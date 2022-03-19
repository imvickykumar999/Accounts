# https://docs.gspread.org/en/latest/api.html#gspread.spreadsheet.Spreadsheet.share

from oauth2client.service_account import ServiceAccountCredentials as sac
import gspread, os

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

jfile = 'ideationology-lab-b60654e44e37.json'
creds = sac.from_json_keyfile_name(jfile, scope)
client = gspread.authorize(creds)

url = 'https://docs.google.com/spreadsheets/d/1sLT6ZM4IeXB7eBxKLtPsYphZSimRqGOV2rPg94JbWaM/edit#gid=0'
sheet = client.open_by_url(url)


def fetch(sheet_no):
    sheet_instance = sheet.get_worksheet(sheet_no)
    records_data = sheet_instance.get_all_records()
    return records_data


def mark(attend, sheet_no):
    import datetime
    dt = str(datetime.datetime.now()).split()

    attend.insert(0, ' / '.join(dt))
    worksheet_up = sheet.get_worksheet(sheet_no)

    sz = len(worksheet_up.col_values(1))+1
    worksheet_up.update(f'A{sz}', [attend])

    worksheet_up.format(f'B{sz}', {"textFormat": {"bold": False}})
    worksheet_up.format(f'C{sz}', {"textFormat": {"bold": False}})

    worksheet_up.update(f'B{sz+1}', 'Total Cost')
    worksheet_up.format(f'B{sz+1}', {"textFormat": {"bold": True}})

    worksheet_up.update(f'C{sz+1}', f"=SUM(C2:C{sz})", raw=False)
    worksheet_up.format(f'C{sz+1}', {"textFormat": {"bold": True}})
    

sheet_no = 0
saman = input('Enter Saman : ')
cost = float(input('Enter Cost : '))
attend = [saman, cost]

mark(attend, sheet_no)
ret = fetch(sheet_no)
print(ret)
