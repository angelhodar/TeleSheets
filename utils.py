from pygsheets import authorize

gc = None

def get_google_client():
    global gc
    gc = gc if gc else authorize(service_account_file='creds.json')
    return gc


def wks_to_message(wks):
    message = ''
    sep = '----------------\n'
    data = wks.get_all_records()
    for record in data:
        for key, value in record.items():
            message += '{} : {}\n'.format(key, value)
        message += sep
    return message


def get_wks(sheet_name='Test'):
    return get_google_client().open_(sheet_name).sheet1

