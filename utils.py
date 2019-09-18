from pygsheets import authorize
import json

gc = None

def wks_to_message(wks):
    message = ''
    sep = '----------------\n'
    data = wks.get_all_records()
    for record in data:
        for key, value in record.items():
            message += '{} : {}\n'.format(key, value)
        message += sep
    return message

def wks_to_json(wks):
    print(wks.to_json())


def get_google_client():
    global gc
    if gc:
        return gc
    gc = authorize(service_account_file='creds.json')
    return gc