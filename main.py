import pygsheets

gc = pygsheets.authorize(service_file='creds.json')

sheet = gc.open('AngelHacker').sheet1

data = sheet.get_all_records()
print(data)

