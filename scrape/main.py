# # river index tracking
# # https://www.dhm.gov.np/frontend_dhm/hydrology/getRainfallFilter

import requests
from datetime import datetime
import csv


def get_data(response, start):
    end_tag = start.split()[0]
    end_tag = end_tag.replace("<", "</")
    end_tag += ">"
    start_tag = start.split()[0]
    data_holder = []
    line = ""
    for data in response:
        if '<' in data:
            data_holder.append(line)
            line = ""
        elif '>' in data:
            line += data
            data_holder.append(line)
            line = ""
            continue
        line += data
    
    start_index = data_holder.index(start)
    data_holder = data_holder[start_index:]
    end_index = 0

    no_tag = -1
    for index, data in enumerate(data_holder):
        if data.split():
            tag = data.split()[0]
            if start_tag in tag:
                no_tag = no_tag + 1
            elif (end_tag in tag) and (no_tag == 0):
                end_index = index
                break
            elif (end_tag in tag) and (no_tag != 0):
                no_tag = no_tag - 1
                
    data_holder = data_holder[:end_index+1]
    return(data_holder)


def extract_data(list, tag=None):
    if tag:
        start_tag = tag
        end_tag = tag.replace('<', '</')
    
    with open('temp.csv', 'a', newline='') as file:
        writer = csv.writer(file)


        # STATION,MAX_TMP, MIN_TMP,AVG_TMP,PRECTOT
        data_to_save = []
        for data in list:
            if '</tr>' in data:
                if data_to_save[0] == 'Station' or data_to_save[0].startswith('*'):
                    data_to_save = []
                if data_to_save:
                    data_to_save.append(datetime.now().strftime('%Y-%m-%d'))
                    print(data_to_save)
                    writer.writerow(data_to_save)
                    data_to_save = []
                    continue
            if not data.startswith('<') and data != '':
                data_to_save.append(data)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get("http://mfd.gov.np/", headers=headers)
filtered = get_data(response.text, '<table class="table" style="margin-bottom: 0px">')

extract_data(filtered)
