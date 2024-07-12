# # river index tracking
# # https://www.dhm.gov.np/frontend_dhm/hydrology/getRainfallFilter

import requests
from datetime import datetime
import csv
import os
from django.conf import settings


def scraper():
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

        static_dir = settings.STATIC_ROOT
        
        with open(os.path.join(static_dir, 'temp.csv'), 'w', newline='') as file:
            writer = csv.writer(file)

            # STATION,MAX_TMP, MIN_TMP,AVG_TMP,PRECTOT
            data_to_save = []
            for data in list:
                if '</tr>' in data:
                    if data_to_save[0] == 'Station' or data_to_save[0].startswith('*'):
                        data_to_save = []
                    if data_to_save:
                        data_to_save.append(datetime.now().strftime('%Y-%m-%d'))
                        writer.writerow(data_to_save)
                        data_to_save = []
                        continue
                if not data.startswith('<') and data != '':
                    data_to_save.append(data)

            return "ok"  

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get("http://mfd.gov.np/", headers=headers)
    filtered = get_data(response.text, '<table class="table" style="margin-bottom: 0px">')

    extract_data(filtered)

miss = 0

def getFrom(location):
    global miss
    try:
        static_dir = settings.STATIC_ROOT

        today = datetime.now().strftime('%Y-%m-%d')
        print(today)
        latest_row = None
        with open(os.path.join(static_dir, 'temp.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == location and row[4] == today:
                    latest_row = row
                    break
        

        if latest_row:
            return latest_row
        else:
            scraper()
            getAll()

    except:
        scraper()
        getAll()


def getAll():
    global miss
    try:
        static_dir = settings.STATIC_ROOT
        today = datetime.now().strftime('%Y-%m-%d')
        data = []
        with open(os.path.join(static_dir, 'temp.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[4] == today:
                    data.append(row)
        if data:
            return data
        else:
            scraper()
            getAll()

    except:
        scraper()
        getAll()