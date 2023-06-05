import pandas as pd
import datetime
import argparse
import os

def summarize_trip(df):
    sea = 'Sea', 'Sea'
    last_loc = sea
    left = None

    print('Date,Day,Port,Country,Time,Hours')  # Print the csv header

    for _, row in df.iterrows():
        loc = f'"{row["Port"]}"', f'"{row["Country"]}"'
        if not pd.isnull(row['Arrive']):
            if left is not None:
                duration = datetime.datetime.combine(pd.to_datetime(row['Date']), datetime.time(hour=int(row['Arrive']))) - datetime.datetime.combine(pd.to_datetime(left[0]), datetime.time(hour=int(left[1])))
                print(f'{left[0]},{row["Day"]},{last_loc[0]},{last_loc[1]},{left[1]},{duration.total_seconds() / 3600}')
            last_loc = loc
            left = row['Date'], row['Arrive']
        if not pd.isnull(row['Depart']):
            if left is not None:
                duration = datetime.datetime.combine(pd.to_datetime(row['Date']), datetime.time(hour=int(row['Depart']))) - datetime.datetime.combine(pd.to_datetime(left[0]), datetime.time(hour=int(left[1])))
                print(f'{left[0]},{row["Day"]},{last_loc[0]},{last_loc[1]},{left[1]},{duration.total_seconds() / 3600}')       
            last_loc = sea
            left = row['Date'], row['Depart']

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
