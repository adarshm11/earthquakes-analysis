#!/bin/bash

# Check if correct number of arguments are provided
if [ $# -ne 4 ]; then
  echo "Usage: $0 <input_csv> <column1> <column2> <column3>"
  exit 1
fi

# Assign input arguments to variables
input_csv=$1
column1=$2
column2=$3
column3=$4

# Extract header
header=$(head -n 1 "$input_csv")

# Find column indices
header_columns=$(echo "$header" | tr ',' '\n')
column1_index=$(echo "$header_columns" | grep -n "^$column1$" | cut -d: -f1)
column2_index=$(echo "$header_columns" | grep -n "^$column2$" | cut -d: -f1)
column3_index=$(echo "$header_columns" | grep -n "^$column3$" | cut -d: -f1)

# Check if all column names were found
if [ -z "$column1_index" ] || [ -z "$column2_index" ] || [ -z "$column3_index" ]; then
  echo "Error: One or more column names not found in the header."
  exit 1
fi

# Filter rows with missing values in the specified columns
awk -F, -v col1="$column1_index" -v col2="$column2_index" -v col3="$column3_index" '
  NR == 1 { print; next }
  $col1 != "" && $col2 != "" && $col3 != "" { print }
' "$input_csv" > earthquakes_data_none_missing.csv

echo "Missing values removed, saved to earthquakes_data_none_missing.csv"
