import pandas as pd
import numpy as np

def calculate_z_scores(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    z_scores = [(x - mean) / std_dev for x in data]
    return z_scores

def replace_outliers_with_median(csv_file, column1, column2, column3, output_file):

    df = pd.read_csv(csv_file)
    df_cleaned = df.copy().drop_duplicates()

    if column1 not in df.columns or column2 not in df.columns or column3 not in df.columns:
        print(f'Error: One or more columns of "{column1}", "{column2}", or "{column3}" not found in the CSV file.')
        return

    median1 = df_cleaned[column1].median()
    median2 = df_cleaned[column2].median()
    median3 = df_cleaned[column3].median()

    z_scores_col1 = calculate_z_scores(df_cleaned[column1])
    z_scores_col2 = calculate_z_scores(df_cleaned[column2])
    z_scores_col3 = calculate_z_scores(df_cleaned[column3])


    # Replace outliers (z-score >= 3 or <= -3) with the median in the cleaned DataFrame
    df_cleaned[column1] = [median1 if abs(z) >= 3 else val for val, z in zip(df[column1], z_scores_col1)]
    df_cleaned[column2] = [median2 if abs(z) >= 3 else val for val, z in zip(df[column2], z_scores_col2)]
    df_cleaned[column3] = [median3 if abs(z) >= 3 else val for val, z in zip(df[column3], z_scores_col3)]


    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file, index=False)
    print(f'Outliers have been replaced and saved to "{output_file}".')

replace_outliers_with_median('earthquakes_data_none_missing.csv', 'magnitude', 
                             'latitude', 'longitude', 'cleaned_earthquakes_data.csv')