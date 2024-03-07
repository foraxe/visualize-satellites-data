
'''
with open("G:\OtherProject\visualize_satellites\ucsusa.org_sites_default_files_2023-06_UCS-Satellite-Database-1-1-2023.txt", 'r', encoding='utf-8', errors='ignore') as file:
    sample_data = [file.readline().strip() for _ in range(10)]

sample_data
'''

import pandas as pd

# Load the dataset into a pandas DataFrame using ISO-8859-1 encoding
df = pd.read_csv("G:\OtherProject\visualize_satellites\ucsusa.org_sites_default_files_2023-06_UCS-Satellite-Database-1-1-2023.txt", sep="\t", encoding='ISO-8859-1')

# 1. Satellites by Country
satellites_by_country = df['Country of Operator/Owner'].value_counts()

# 2. Orbit Types
orbit_types = df['Class of Orbit'].value_counts()

# 3. Operational or Non-operational
df['Launch Year'] = pd.to_datetime(df['Date of Launch'], errors='coerce').dt.year
df['Operational Status'] = (2023 - df['Launch Year'] <= df['Expected Lifetime (yrs.)']).replace({True: 'Operational', False: 'Non-operational'})
operational_status = df['Operational Status'].value_counts()

satellites_by_country, orbit_types, operational_status

