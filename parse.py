def parse_row(row, ignore_headers=[]):
    message = ''
    for key in [k for k in row not in ignore_headers]:
        if row[key]:
            message += '{} : {}\n'.format(key, row[key])
    return message


def parse_calendar(wks):
    events = wks.get_all_records(empty_value=None)
    calendar_message = ''
    for event in events:
        calendar_message += '{}\n\n'.format(parse_row(event))
    return calendar_message
    

def parse_asistence(row):
    return parse_row(row, ignore_headers=['Telegram'])