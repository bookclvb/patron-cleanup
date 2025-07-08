# patron-cleanup
Tools for cleaning up patron data before loading into Sierra.
***Made with a lot of assistance from Copilot*** 

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
