import pandas as pd

# Read the Excel file
df = pd.read_excel('employees.xlsx')

# Delete the first and second rows, assign new column keys
df = df.drop([0, 1]).reset_index(drop=True)
new_column_names = ['u', 'first', 'last', 'a', 't', 'hire', '46', 'x', 'z', 'b']
df.columns = new_column_names[:len(df.columns)]

# De-dupe rows, keeping entries with a barcode
df = df.sort_values(by='b', na_position='last', ascending=False)
df = df.drop_duplicates(subset='u', keep='first')

# Create JSON file from DataFrame
df.to_json('employees.json', orient='records', force_ascii=False, indent=2)

import json
from collections import OrderedDict
import csv

# Set desired export key order
key_order = ['u', 'n', 'a', 't', '44', '45', '46', '47', 'x', 'z', 'b']

# Read JSON file and process
# Create new column 'n' by joining columns 'first' and 'last' then remove them
# empty 'a', add '44' and '45' columns
# Copy 'x' to '47'
with open('employees.json', mode='r', encoding='utf-8') as infile:
    reader = json.load(infile)
for row in reader:
    row['n'] = f"{row['last']}, {row['first']}"
    row.pop('first', None)
    row.pop('last', None)
    row.pop('hire', None)
    row['a'] = ''
    row['44'] = ''
    row['45'] = ''
    row['47'] = row.get('x', '')

# Change values in column '47' using a mapping file
with open('47.json', mode='r', encoding='utf-8') as mapfile_47:
    map_47 = json.load(mapfile_47)
for row in reader:
    v47 = str(row.get('47', '')).lower()
    matched = False
    for keyword, code in map_47.items():
        if keyword in v47:
            row['47'] = code
            matched = True
            break
    if not matched:
        row['47'] = '3'

# Treat 'b' as string and remove decimal and everything after
    if 'b' in row and row['b'] is not None:
        row['b'] = str(row['b']).split('.')[0]

# Pad 'u' with leading zeroes to ensure 7 characters
    if 'u' in row and row['u'] is not None:
        row['u'] = str(row['u']).zfill(7)

# Assign codes based on keywords in position title ('x')
    vx = str(row.get('x', '')).lower()
    if 'professor' in vx:
        row['44'] = 'f'
    elif 'critic' in vx:
        row['44'] = 'p'
    elif 'lecturer' in vx:
        row['44'] = 'p'  
    elif 'intern' in vx:
        row['44'] = 'i'
    elif 'temp' in vx:
        row['44'] = 'i'      
    elif 'fellow' in vx:
        row['44'] = 'r'      

        
# Map department codes in '46' using a JSON file
with open('46.json', mode='r', encoding='utf-8') as mapfile:
    map_46 = json.load(mapfile)
for row in reader:
    if '46' in row and row['46'] in map_46:
        row['46'] = map_46[row['46']]
# Reassign library users to library p type
    v46 = str(row.get('46', '')).lower()
    if '16' in v46:
        row['47'] = '26'  
        

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
with open('employees-output.json', mode='w', encoding='utf-8') as outfile:
    json.dump(ordered_reader, outfile, ensure_ascii=False, indent=2)

# Write to a new CSV file with no header row
with open('employees-output.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=key_order)
    writer.writerows(ordered_reader)
