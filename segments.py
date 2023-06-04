import pandas as pd
import datetime
import argparse
import os

def summarize_trip(df):
    sea = 'Sea', 'Sea'
    last_loc = sea
    left = None

    for _, row in df.iterrows():
        loc = row['Port'], row['Country']
        if not pd.isnull(row['Arrive']):
            if left:
                print(f'{left},{last_loc},{row["Date"]},{row["Arrive"] - left}')
            last_loc = loc
            left = row['Arrive']
        if not pd.isnull(row['Depart']):
            if left:
                print(f'{left},{last_loc},{row["Date"]},{row["Depart"] - left}')       
            last_loc = sea
            left = row['Depart']

def main(input_file):
    # Load the csv file
    df = pd.read_csv(input_file)

    # Process the data
    summarize_trip(df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a trip itinerary CSV file.')
    parser.add_argument('input_file', help='The CSV file to process.')
    args = parser.parse_args()
    main(args.input_file)
