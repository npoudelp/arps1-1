# extract unique Label from csv file
import csv

def extract_label(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        labels = []
        for row in reader:
            labels.append(row[7])
    return list(set(labels))

print(extract_label('Crop_recommendation.csv'))