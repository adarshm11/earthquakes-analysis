import pandas as pd

df = pd.read_csv('cleaned_earthquakes_data.csv')

column1 = 'magnitude'
column2 = 'latitude'
column3 = 'longitude'

latitude_correlation = df[column1].corr(df[column2])
longitude_correlation = df[column1].corr(df[column3])

print(f'Correlation betwen magnitude and latitude: {latitude_correlation}')
print(f'Correlation between magnitude and longitude: {longitude_correlation}')