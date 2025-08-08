# patron-cleanup
Tools for cleaning up patron data before loading into Sierra.
***Made with a lot of assistance from Copilot*** 

# How to use
- make sure you have a virtual environment with pandas and openpyxl installed
- drop in students file from workday and rename it 'students.xlsx'
- run students.py
- if that works properly, open students-output.csv and just check it against students.xslx to make sure it looks good (eg same # of entries, things in the right order...)
- import into sierra!

## What the 'students.py' script does:
- Read file 'students.xslx' and export to JSON format
- Join first and last name in new column, delete old columns
- empty column '44', add 'x' column
- Pad 'u' ID field with leading zeroes to ensure 7 characters
- Convert anticipated grad year to just the last digit
- Convert p types to codes
- Treat barcode as string and remove decimal and everything after
- Map departments to codes using '46.json'
- Reorder columns to u, n, a, t, 44, 45, 46, 47, x, z, b
- Write changes back to JSON
- Write to a new CSV file 'students-output.csv'

## Current issues: 
Mostly related to manual edits still needed:
- Removing the first row of data upon outputting - doesn't work.
- Need to find a more elegant way to rename columns and delete top 2.

## **Files containing personally identifiable data are listed in this repo's .gitignore**
```
# These files contain personal data not to be shared #
######################################################
students.xlsx
students.json
students-output.json
students-output.csv
employees.xlsx
employees.json
employees-output.json
employees-output.csv
```
