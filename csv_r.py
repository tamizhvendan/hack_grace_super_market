import csv
import os

# User data keys
keys = {
    "ID": "id",
    "DISPLAY ID": "cust_showid",
    "NAME": "cust_name",
    "GROUP ID": "cust_groupid",
    "MOBILE": "cust_mobile",
    "ALTERNATE MOBILE": "cust_mobile1",
    "EMAIL": "cust_email",
    "IMAGE": "cust_img",
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

available_series = [
    '8300',
    '9003',
    '9025',
    '9042',
    '9043',
    '9240',
    '9342',
    '9442',
    '9500',
    '9600',
    '9626',
    '9629',
    '9840',
    '9842',
    '9940',
    '9941',
]

def formalize_registered_numbers():
    with open(file='registered_numbers.txt', mode='a') as f:
        f.write("phone,message,status\n")

    for series in available_series:
        print('Working on ' + series + '...')

        with open(file=series + '_series_records.txt', encoding='cp437', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            reader = list(reader)
            
            for row in reader:
                if row.get('message') != None:
                    if row['message'] == 'registered':
                        with open(file='registered_numbers.txt', mode='a') as f:
                            f.write(row['phone'] + ",registered,200\n")


def get_thousand_registered_user_details():
    header = ''
    for x in keys:
        header += x + (',' if x != 'DND STATUS SMS' else '')

    header += '\n'

    with open(file='thousand_user_data.csv', mode='a') as f:
        f.write(header)

    with open(file='AUTH/user_data.csv', encoding='cp437', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        reader = list(reader)

        required_key_lists = list(keys.keys())
        values = ''

        reader = reader[0:1000]

        for row in reader:
            for x in row:
                if x in required_key_lists:
                    values += (str(row[x]) if row.get(x) != None else '') + (',' if x != 'DND STATUS SMS' else '') 

            with open(file='thousand_user_data.csv', mode='a') as f:
                f.write(values + '\n')
            
            print('Writing...')

# formalize_registered_numbers()

get_thousand_registered_user_details()

print('Finished')
exit()