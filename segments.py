import pandas as pd
import argparse
import os
import numpy as np

def summarize_trip(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    summarized_data = []
    last_depart = None
    ongoing_port = None
    ongoing_country = None
    extra_days = 0

    for index, row in df.iterrows():
        if ongoing_port is None:
            ongoing_port = row['Port']
            ongoing_country = row['Country']
            last_depart = row['Depart']
        elif ongoing_port == row['Port'] and ongoing_country == row['Country']:
            extra_days += 24
        else:
            hours = (row['Arrive'] - last_depart) + extra_days
            last_depart = row['Depart']
            extra_days = 0
            port_row = {'Date': row['Date'], 'Day': row['Day'], 'Port': ongoing_port, 
                        'Country': ongoing_country, 'Time': last_depart, 'Hours': hours}
            summarized_data.append(port_row)
            ongoing_port = row['Port']
            ongoing_country = row['Country']
            
    summarized_df = pd.DataFrame(summarized_data)
    return summarized_df

def main(input_file):
    # Load the csv file
    df = pd.read_csv(input_file)

    # Process the data
    summarized_df = summarize_trip(df)
    
    # Create output filename and save the dataframe
    base, ext = os.path.splitext(input_file)
    output_file = base + "_segments" + ext
    summarized_df.to_csv(output_file, index=False)
    print(f"Saved the processed data to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a trip itinerary CSV file.')
    parser.add_argument('input_file', help='The CSV file to process.')
    args = parser.parse_args()
    main(args.input_file)
