import csv

# Read CSV file
with open('employees.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = list(csv.DictReader(infile))

# Delete the first data row
if reader:
    del reader[0]

# Create new column 'full_name' by joining columns 'Preferred_Last_Name' (C) and 'Preferred_First_Name' (B)
for row in reader:
    row['full_name'] = f"{row['Preferred_Last_Name']}, {row['Preferred_First_Name']}"

# Remove the old columns if you don't need them
for row in reader:
    row.pop('Preferred_First_Name', None)
    row.pop('Preferred_Last_Name', None)

# Define new fieldnames (replace with your actual column names)
fieldnames = [fn for fn in reader[0].keys()] if reader else []

# Write changes back to CSV
with open('employees.csv', mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)