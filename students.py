import pandas as pd

# Read the Excel file
df = pd.read_excel('students.xlsx')

# Delete the first and second rows, assign new column keys
df = df.drop([0, 1]).reset_index(drop=True)
new_column_names = ['u', 'first', 'last', 'a', 't', '44', '45', '46', '47', 'z', 'b']
df.columns = new_column_names[:len(df.columns)]

# De-dupe student rows, keeping entries with a barcode
df = df.sort_values(by='b', na_position='last', ascending=False)
df = df.drop_duplicates(subset='u', keep='first')

# Create JSON file from DataFrame
df.to_json('students.json', orient='records', force_ascii=False, indent=2)

import json
from collections import OrderedDict
import csv

# Set desired export key order
key_order = ['u', 'n', 'a', 't', '44', '45', '46', '47', 'x', 'z', 'b']

# Read JSON file
with open('students.json', mode='r', encoding='utf-8') as infile:
    reader = json.load(infile)

# Create new column 'n' by joining columns 'first' and 'last'
# remove the 'first' and 'last' columns
# empty '44', add 'x' column
for row in reader:
    row['n'] = f"{row['last']}, {row['first']}"
    row.pop('first', None)
    row.pop('last', None)
    row['44'] = '-'
    row['x'] = ''
# Pad 'u' with leading zeroes to ensure 7 characters
    if 'u' in row and row['u'] is not None:
        row['u'] = str(row['u']).zfill(7)
# Keep only the last character of '45', if it exists
    row['45'] = str(row.get('45', ''))[-1:] if row.get('45') else ''
# Change values in column '47'
    if row.get('47') == "Undergraduate":
        row['47'] = 2
    elif row.get('47') == "Graduate":
        row['47'] = 17
# Treat 'b' as string and remove decimal and everything after
    if 'b' in row and row['b'] is not None:
        row['b'] = str(row['b']).split('.')[0]
# Add PCODE1 for Brown and Exchange students
    email = row.get('z', '').lower()
    if 'brown.edu' in email:
        row['44'] = '2'
    elif email and ('risd.edu' not in email):
        row['44'] = 'e'
        
# Map department codes in '46' using a JSON file
with open('46.json', mode='r', encoding='utf-8') as mapfile:
    map_46 = json.load(mapfile)
for row in reader:
    if '46' in row and row['46'] in map_46:
        row['46'] = map_46[row['46']]
        

# Reorder keys for each row
ordered_reader = []
for row in reader:
    ordered_row = OrderedDict()
    for key in key_order:
        if key in row:
            ordered_row[key] = row[key]
    # Add any remaining keys not in key_order
    for key in row:
        if key not in ordered_row:
            ordered_row[key] = row[key]
    ordered_reader.append(ordered_row)

# Write changes back to JSON
with open('students-output.json', mode='w', encoding='utf-8') as outfile:
    json.dump(ordered_reader, outfile, ensure_ascii=False, indent=2)

# Write to a new CSV file with no header row
with open('students-output.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=key_order)
    writer.writerows(ordered_reader)
