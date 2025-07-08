import pandas as pd

# Read the Excel file (replace 'students.xlsx' with your file name)
df = pd.read_excel('students.xlsx')

# Export to JSON
df.to_json('students.json', orient='records', force_ascii=False, indent=2)