import nexmo

key = '5050719f'
sec = '1ad984bb'

client = nexmo.Client(key=key, secret=sec)

params = {
    'type': 'landline',
    # 'api_key': key,
    # 'api_secret': sec
}

result = client.get_available_numbers('US', params)
print result